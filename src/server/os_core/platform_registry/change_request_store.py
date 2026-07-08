"""config_change_requests 持久化与人审落库（ADR-008 · Studio 写路径）。

作用：AI/人提案 → pending → approve/reject → Registry 变更。
业务关联：U2 界面确认 · R-09 禁止 AI 自动 publish。
上游：server.api.modules.registry.controllers.registry_changes
下游：pack_registry · system_relations · contract_publish_records
"""
from __future__ import annotations

import hashlib
import json
import uuid
from typing import Any

import yaml
from sqlalchemy import text
from sqlalchemy.orm import Session


def _checksum(body: str) -> str:
  digest = hashlib.sha256(body.encode("utf-8")).hexdigest()
  return f"sha256:{digest}"


def create_change_request(
  session: Session,
  *,
  tenant_id: str | None,
  kind: str,
  proposed_by: str,
  proposal_body: dict[str, Any],
  ai_model_id: str | None = None,
) -> dict[str, Any]:
  """创建 pending 变更请求。

  功能：INSERT config_change_requests 并 commit。
  业务含义：Studio AI/人提案入口；R-09 禁止自动 publish。
  参数 kind：pack_upsert 或 system_relation_upsert。
  返回：新建请求 dict（含 proposal_body 已解析）。
  """
  request_id = f"ccr-{uuid.uuid4().hex[:12]}"
  session.execute(
    text(
      """
      INSERT INTO config_change_requests (
        request_id, tenant_id, kind, status, proposed_by, proposal_body, ai_model_id
      ) VALUES (
        :request_id, :tenant_id, :kind, 'pending', :proposed_by, :proposal_body, :ai_model_id
      )
      """
    ),
    {
      "request_id": request_id,
      "tenant_id": tenant_id,
      "kind": kind,
      "proposed_by": proposed_by,
      "proposal_body": json.dumps(proposal_body, ensure_ascii=False),
      "ai_model_id": ai_model_id,
    },
  )
  session.commit()
  row = get_change_request(session, request_id=request_id)
  assert row is not None
  return row


def get_change_request(session: Session, *, request_id: str) -> dict[str, Any] | None:
  """按 ID 查变更请求。

  功能：SELECT config_change_requests 单行。
  业务含义：人审详情页与 approve/reject 前置查询。
  参数 request_id：变更请求主键。
  返回：请求 dict 或 None。
  """
  row = (
    session.execute(
      text(
        """
        SELECT request_id, tenant_id, kind, status, proposed_by, proposal_body,
               ai_model_id, created_at
        FROM config_change_requests WHERE request_id = :request_id LIMIT 1
        """
      ),
      {"request_id": request_id},
    )
    .mappings()
    .first()
  )
  if not row:
    return None
  out = dict(row)
  out["proposal_body"] = json.loads(out["proposal_body"])
  return out


def list_change_requests(
  session: Session,
  *,
  tenant_id: str | None = None,
  status: str | None = None,
) -> list[dict[str, Any]]:
  """列出变更请求（可选过滤）。

  功能：按 tenant_id/status 过滤并倒序返回。
  业务含义：Studio 变更队列与人审工作台列表。
  参数 tenant_id/status：可选过滤键。
  返回：变更请求 dict 列表。
  """
  clauses = ["1=1"]
  params: dict[str, Any] = {}
  if tenant_id is not None:
    clauses.append("tenant_id = :tenant_id")
    params["tenant_id"] = tenant_id
  if status is not None:
    clauses.append("status = :status")
    params["status"] = status
  sql = f"""
    SELECT request_id, tenant_id, kind, status, proposed_by, proposal_body,
           ai_model_id, created_at
    FROM config_change_requests
    WHERE {' AND '.join(clauses)}
    ORDER BY created_at DESC
  """
  rows = session.execute(text(sql), params).mappings()
  out: list[dict[str, Any]] = []
  for row in rows:
    item = dict(row)
    item["proposal_body"] = json.loads(item["proposal_body"])
    out.append(item)
  return out


def _apply_pack_upsert(session: Session, proposal: dict[str, Any]) -> None:
  """将 pack_upsert proposal 写入 pack_registry（ON CONFLICT 更新）。"""
  pack_id = str(proposal["pack_id"])
  body = proposal.get("body") or proposal.get("body_yaml") or ""
  if isinstance(body, dict):
    body = yaml.dump(body, allow_unicode=True, sort_keys=False)
  registry_key = str(proposal.get("registry_key") or f"catalog/{pack_id}.yaml")
  session.execute(
    text(
      """
      INSERT INTO pack_registry (
        pack_id, registry_key, certification_level, body, checksum, status
      ) VALUES (
        :pack_id, :registry_key, :certification_level, :body, :checksum, :status
      )
      ON CONFLICT(pack_id) DO UPDATE SET
        registry_key = excluded.registry_key,
        body = excluded.body,
        checksum = excluded.checksum,
        status = excluded.status
      """
    ),
    {
      "pack_id": pack_id,
      "registry_key": registry_key,
      "certification_level": proposal.get("certification_level") or "bronze",
      "body": body,
      "checksum": _checksum(body),
      "status": proposal.get("status") or "published",
    },
  )


def _apply_system_relation_upsert(session: Session, proposal: dict[str, Any]) -> None:
  """将 system_relation_upsert proposal 写入 system_relations（ON CONFLICT 更新）。"""
  relation_id = str(proposal["relation_id"])
  tenant_id = str(proposal["tenant_id"])
  pack_id = str(proposal["pack_id"])
  body = proposal.get("body") or proposal.get("body_yaml") or ""
  if isinstance(body, dict):
    body = yaml.dump(body, allow_unicode=True, sort_keys=False)
  session.execute(
    text(
      """
      INSERT INTO system_relations (
        relation_id, tenant_id, pack_id, environment, path, body, lifecycle
      ) VALUES (
        :relation_id, :tenant_id, :pack_id, :environment, :path, :body, :lifecycle
      )
      ON CONFLICT(relation_id) DO UPDATE SET
        pack_id = excluded.pack_id,
        environment = excluded.environment,
        path = excluded.path,
        body = excluded.body,
        lifecycle = excluded.lifecycle
      """
    ),
    {
      "relation_id": relation_id,
      "tenant_id": tenant_id,
      "pack_id": pack_id,
      "environment": proposal.get("environment") or "prod",
      "path": proposal.get("path"),
      "body": body,
      "lifecycle": proposal.get("lifecycle") or "active",
    },
  )


def approve_change_request(
  session: Session,
  *,
  request_id: str,
  approved_by: str,
) -> dict[str, Any]:
  """人审批准：应用 proposal 并标记 approved。

  功能：按 kind 调用 _apply_* 后 UPDATE status=approved。
  业务含义：U2 界面确认后 Registry 正式变更。
  参数 request_id/approved_by：请求 ID 与审批人。
  返回：更新后的请求 dict。
  异常：请求不存在或非 pending 时 ValueError。
  """
  # 业务：pending 请求按 kind 应用 proposal 后 UPDATE status=approved
  row = get_change_request(session, request_id=request_id)
  if row is None:
    raise ValueError(f"Change request not found: {request_id}")
  if row["status"] != "pending":
    raise ValueError(f"Change request not pending: {row['status']}")

  kind = row["kind"]
  proposal = row["proposal_body"]
  if kind == "pack_upsert":
    _apply_pack_upsert(session, proposal)
  elif kind == "system_relation_upsert":
    _apply_system_relation_upsert(session, proposal)
  else:
    raise ValueError(f"Unsupported change kind: {kind}")

  session.execute(
    text(
      """
      UPDATE config_change_requests
      SET status = 'approved'
      WHERE request_id = :request_id
      """
    ),
    {"request_id": request_id},
  )
  session.commit()
  updated = get_change_request(session, request_id=request_id)
  assert updated is not None
  return updated


def reject_change_request(
  session: Session,
  *,
  request_id: str,
  rejected_by: str,
  reason: str | None = None,
) -> dict[str, Any]:
  """人审拒绝变更请求。

  功能：UPDATE status=rejected 并可选写入 _reject_reason。
  业务含义：拒绝后 proposal 不落 Registry 表。
  参数 request_id：变更请求主键；reason：可选拒绝原因。
  返回：更新后的请求 dict。
  异常：请求不存在或非 pending 时 ValueError。
  """
  # 业务：pending 请求写入拒绝原因后 UPDATE status=rejected
  row = get_change_request(session, request_id=request_id)
  if row is None:
    raise ValueError(f"Change request not found: {request_id}")
  if row["status"] != "pending":
    raise ValueError(f"Change request not pending: {row['status']}")

  proposal = dict(row["proposal_body"])
  if reason:
    proposal["_reject_reason"] = reason
  session.execute(
    text(
      """
      UPDATE config_change_requests
      SET status = 'rejected', proposal_body = :proposal_body
      WHERE request_id = :request_id
      """
    ),
    {
      "request_id": request_id,
      "proposal_body": json.dumps(proposal, ensure_ascii=False),
    },
  )
  session.commit()
  updated = get_change_request(session, request_id=request_id)
  assert updated is not None
  return updated
