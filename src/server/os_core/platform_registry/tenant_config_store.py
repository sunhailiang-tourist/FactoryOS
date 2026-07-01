"""Tenant 配置 Registry（tenant_profiles · system_relations · overrides）。

作用：租户级配置与系统关系只读/写入（Studio 主路径）。
业务关联：配置枢纽 Layer B · connector_instances 激活 · P-02 import · P-03 override。
上游：Studio · import/export · tenant_service
下游：connector runtime · execution gates · connect/test
"""
from __future__ import annotations

import json
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import Session


def get_tenant_profile(session: Session, *, tenant_id: str) -> dict[str, Any] | None:
  """tenant_profiles 单行。"""
  row = (
    session.execute(
      text(
        """
        SELECT tenant_id, display_name, path, shadow_mode, write_approved, profile_json
        FROM tenant_profiles WHERE tenant_id = :tenant_id LIMIT 1
        """
      ),
      {"tenant_id": tenant_id},
    )
    .mappings()
    .first()
  )
  return dict(row) if row else None


def list_system_relations(session: Session, *, tenant_id: str) -> list[dict[str, Any]]:
  """租户 system_relations 列表。"""
  rows = session.execute(
    text(
      """
      SELECT relation_id, tenant_id, pack_id, environment, path, body, lifecycle
      FROM system_relations WHERE tenant_id = :tenant_id
      """
    ),
    {"tenant_id": tenant_id},
  ).mappings()
  return [dict(r) for r in rows]


def is_pack_entitled(
  session: Session,
  *,
  tenant_id: str,
  pack_id: str,
) -> bool:
  """tenant_pack_entitlements 是否授权 pack_id。

  功能：license_service 真源（W7 Step2）。
  业务含义：有 Connector 绑定但未购 Pack → MODULE_NOT_LICENSED。
  """
  row = session.execute(
    text(
      """
      SELECT 1 FROM tenant_pack_entitlements
      WHERE tenant_id = :tenant_id AND pack_id = :pack_id AND licensed = 1
      LIMIT 1
      """
    ),
    {"tenant_id": tenant_id, "pack_id": pack_id},
  ).first()
  return row is not None


def has_system_relation_for_pack(
  session: Session,
  *,
  tenant_id: str,
  pack_id: str,
) -> bool:
  """租户是否已注册 Connector Pack（system_relations）。

  功能：T-03 CONNECTOR_NOT_CONFIGURED 真源。
  业务含义：无 relation → 403，禁止 silent no-op。
  """
  row = session.execute(
    text(
      """
      SELECT 1 FROM system_relations
      WHERE tenant_id = :tenant_id AND pack_id = :pack_id
      LIMIT 1
      """
    ),
    {"tenant_id": tenant_id, "pack_id": pack_id},
  ).first()
  return row is not None


def get_connector_overrides(session: Session, *, tenant_id: str) -> dict[str, Any]:
  """profile_json.connector_overrides（P-03 Override 差量）。"""
  profile = get_tenant_profile(session, tenant_id=tenant_id)
  if profile is None:
    return {}
  raw = profile.get("profile_json")
  if not raw:
    return {}
  try:
    data = json.loads(raw) if isinstance(raw, str) else raw
  except (json.JSONDecodeError, TypeError):
    return {}
  if not isinstance(data, dict):
    return {}
  overrides = data.get("connector_overrides")
  return overrides if isinstance(overrides, dict) else {}


def ensure_system_relation(
  session: Session,
  *,
  tenant_id: str,
  pack_id: str,
  registry_key: str | None = None,
) -> None:
  """幂等创建 system_relations 行（P-02 import）。"""
  if has_system_relation_for_pack(session, tenant_id=tenant_id, pack_id=pack_id):
    return
  relation_id = f"rel-{tenant_id}-{pack_id}"[:128]
  session.execute(
    text(
      """
      INSERT INTO system_relations (
        relation_id, tenant_id, pack_id, environment, path, body, lifecycle
      ) VALUES (
        :relation_id, :tenant_id, :pack_id, 'prod', :path, :body, 'active'
      )
      """
    ),
    {
      "relation_id": relation_id,
      "tenant_id": tenant_id,
      "pack_id": pack_id,
      "path": registry_key,
      "body": f"imported: {pack_id} for {tenant_id}",
    },
  )


def ensure_pack_entitlement(
  session: Session,
  *,
  tenant_id: str,
  pack_id: str,
) -> None:
  """幂等授权 tenant_pack_entitlements（P-02 import）。"""
  session.execute(
    text(
      """
      DELETE FROM tenant_pack_entitlements
      WHERE tenant_id = :tenant_id AND pack_id = :pack_id
      """
    ),
    {"tenant_id": tenant_id, "pack_id": pack_id},
  )
  session.execute(
    text(
      """
      INSERT INTO tenant_pack_entitlements (tenant_id, pack_id, licensed)
      VALUES (:tenant_id, :pack_id, 1)
      """
    ),
    {"tenant_id": tenant_id, "pack_id": pack_id},
  )


def list_licensed_pack_ids(session: Session, *, tenant_id: str) -> list[str]:
  """tenant_pack_entitlements 已授权 Pack ID 列表（M-01 tools/list）。"""
  rows = session.execute(
    text(
      """
      SELECT pack_id FROM tenant_pack_entitlements
      WHERE tenant_id = :tenant_id AND licensed = 1
      ORDER BY pack_id
      """
    ),
    {"tenant_id": tenant_id},
  ).mappings()
  return [str(r["pack_id"]) for r in rows]


def upsert_tenant_settings(
  session: Session,
  *,
  tenant_id: str,
  shadow_mode: bool | None = None,
  write_approved: bool | None = None,
  connector_overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
  """创建或更新 tenant_profiles 中 Shadow / 写批准字段。

  功能：tenant_service 持久化真源。
  业务含义：T-01 租户级 shadow_mode；无行时 insert 默认 tenant。
  参数 shadow_mode：true 时 L2 仅 simulated。
  参数 write_approved：Harness 生产写批准（W7+）。
  返回：更新后 profile 行 dict。
  """
  existing = get_tenant_profile(session, tenant_id=tenant_id)
  profile_data: dict[str, Any] = {}
  if existing and existing.get("profile_json"):
    try:
      parsed = json.loads(existing["profile_json"])
      if isinstance(parsed, dict):
        profile_data = parsed
    except (json.JSONDecodeError, TypeError):
      profile_data = {}

  if connector_overrides is not None:
    profile_data["connector_overrides"] = connector_overrides

  profile_json_str = json.dumps(profile_data, ensure_ascii=False) if profile_data else None

  if existing is None:
    sm = False if shadow_mode is None else shadow_mode
    wa = False if write_approved is None else write_approved
    session.execute(
      text(
        """
        INSERT INTO tenant_profiles (
          tenant_id, display_name, path, shadow_mode, write_approved, profile_json
        ) VALUES (
          :tenant_id, :display_name, :path, :shadow_mode, :write_approved, :profile_json
        )
        """
      ),
      {
        "tenant_id": tenant_id,
        "display_name": tenant_id,
        "path": None,
        "shadow_mode": sm,
        "write_approved": wa,
        "profile_json": profile_json_str,
      },
    )
  else:
    sets: list[str] = []
    params: dict[str, Any] = {"tenant_id": tenant_id}
    if shadow_mode is not None:
      sets.append("shadow_mode = :shadow_mode")
      params["shadow_mode"] = shadow_mode
    if write_approved is not None:
      sets.append("write_approved = :write_approved")
      params["write_approved"] = write_approved
    if connector_overrides is not None:
      sets.append("profile_json = :profile_json")
      params["profile_json"] = profile_json_str
    if sets:
      session.execute(
        text(
          f"UPDATE tenant_profiles SET {', '.join(sets)} WHERE tenant_id = :tenant_id"
        ),
        params,
      )
  updated = get_tenant_profile(session, tenant_id=tenant_id)
  assert updated is not None
  return updated
