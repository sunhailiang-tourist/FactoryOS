"""audit_events 持久化（append-only · 无 UPDATE/DELETE）。

作用：审计写入与按 tenant/exec_id 查询。
业务关联：R-06 append-only；E-03 审计产生。
上游：execution_service、server.api.modules.audit.controllers
下游：audit_events 表
关联文档：contracts/schemas/AuditEvent.schema.json
"""
from __future__ import annotations

import json
from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import text
from sqlalchemy.orm import Session

from os_core.shared_contracts.models.audit import AuditEvent, AuditEventType
from os_core.shared_contracts.models.common import Actor


def _parse_exec_id(exec_id: str | UUID | None) -> UUID | None:
  """将 exec_id 规范为 UUID 或 None。"""
  if exec_id is None:
    return None
  if isinstance(exec_id, UUID):
    return exec_id
  return UUID(str(exec_id))


def append_audit_event(
  *,
  session: Session,
  tenant_id: str,
  event_type: str | AuditEventType,
  actor: dict[str, str] | Actor,
  exec_id: str | UUID | None = None,
  graph_id: str | None = None,
  graph_version: str | None = None,
  pack_id: str | None = None,
  plan_id: str | UUID | None = None,
  payload: dict | None = None,
  correlation_id: str | None = None,
  occurred_at: datetime | None = None,
) -> AuditEvent:
  """追加一条审计事件（仅 INSERT）。

  功能：写入 audit_events 单行。
  业务含义：写路径与门禁拒绝均须可追溯；禁止更新历史。
  上游调用方：execution_service、未来 rule/graph 钩子
  下游被调方：audit_events 表
  参数 tenant_id：租户隔离键
  参数 event_type：Schema enum 字符串
  返回：对齐 AuditEvent.schema 的 Pydantic 模型
  """
  event_id = uuid4()
  when = occurred_at or datetime.now(UTC)
  exec_uuid = _parse_exec_id(exec_id)
  plan_uuid = _parse_exec_id(plan_id) if plan_id is not None else None

  if isinstance(actor, dict):
    actor_model = Actor.model_validate(actor)
  else:
    actor_model = actor

  if isinstance(event_type, AuditEventType):
    event_type_str = event_type.value
  else:
    event_type_str = str(event_type)
    AuditEventType(event_type_str)

  actor_json = actor_model.model_dump(mode="json", exclude_none=True)
  payload_json = json.dumps(payload, ensure_ascii=False) if payload is not None else None

  session.execute(
    text(
      """
      INSERT INTO audit_events (
        event_id, tenant_id, event_type, actor_json, occurred_at,
        exec_id, graph_id, graph_version, pack_id, plan_id,
        payload_json, correlation_id
      ) VALUES (
        :event_id, :tenant_id, :event_type, :actor_json, :occurred_at,
        :exec_id, :graph_id, :graph_version, :pack_id, :plan_id,
        :payload_json, :correlation_id
      )
      """
    ),
    {
      "event_id": str(event_id),
      "tenant_id": tenant_id,
      "event_type": event_type_str,
      "actor_json": json.dumps(actor_json, ensure_ascii=False),
      "occurred_at": when.isoformat(),
      "exec_id": str(exec_uuid) if exec_uuid else None,
      "graph_id": graph_id,
      "graph_version": graph_version,
      "pack_id": pack_id,
      "plan_id": str(plan_uuid) if plan_uuid else None,
      "payload_json": payload_json,
      "correlation_id": correlation_id,
    },
  )

  return AuditEvent(
    event_id=event_id,
    tenant_id=tenant_id,
    event_type=AuditEventType(event_type_str),
    actor=actor_model,
    occurred_at=when,
    exec_id=exec_uuid,
    graph_id=graph_id,
    graph_version=graph_version,
    pack_id=pack_id,
    plan_id=plan_uuid,
    payload=payload,
    correlation_id=correlation_id,
  )


def list_audit_events(
  *,
  session: Session,
  tenant_id: str,
  exec_id: str | UUID | None = None,
  event_type: str | None = None,
  since: datetime | None = None,
  limit: int = 100,
) -> list[AuditEvent]:
  """按 tenant 查询审计事件（只读）。

  功能：SELECT audit_events，默认按 occurred_at 升序。
  业务含义：E-03 验收、ExecutionEvidence 组装。
  上游调用方：server/api GET /v1/audit/events、execution_service
  下游被调方：audit_events 表
  参数 exec_id：可选，过滤单次执行
  返回：AuditEvent 列表
  """
  exec_uuid = _parse_exec_id(exec_id)
  clauses = ["tenant_id = :tenant_id"]
  params: dict[str, object] = {"tenant_id": tenant_id, "limit": min(limit, 500)}

  if exec_uuid is not None:
    clauses.append("exec_id = :exec_id")
    params["exec_id"] = str(exec_uuid)
  if event_type is not None:
    clauses.append("event_type = :event_type")
    params["event_type"] = event_type
  if since is not None:
    clauses.append("occurred_at >= :since")
    params["since"] = since.isoformat()

  where = " AND ".join(clauses)
  rows = (
    session.execute(
      text(
        f"""
        SELECT event_id, tenant_id, event_type, actor_json, occurred_at,
               exec_id, graph_id, graph_version, pack_id, plan_id,
               payload_json, correlation_id
        FROM audit_events
        WHERE {where}
        ORDER BY occurred_at ASC
        LIMIT :limit
        """
      ),
      params,
    )
    .mappings()
    .all()
  )

  out: list[AuditEvent] = []
  for row in rows:
    actor_data = json.loads(row["actor_json"])
    payload = json.loads(row["payload_json"]) if row["payload_json"] else None
    out.append(
      AuditEvent(
        event_id=UUID(row["event_id"]),
        tenant_id=row["tenant_id"],
        event_type=AuditEventType(row["event_type"]),
        actor=Actor.model_validate(actor_data),
        occurred_at=datetime.fromisoformat(row["occurred_at"]),
        exec_id=UUID(row["exec_id"]) if row["exec_id"] else None,
        graph_id=row["graph_id"],
        graph_version=row["graph_version"],
        pack_id=row["pack_id"],
        plan_id=UUID(row["plan_id"]) if row["plan_id"] else None,
        payload=payload,
        correlation_id=row["correlation_id"],
      )
    )
  return out
