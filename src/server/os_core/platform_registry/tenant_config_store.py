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

from os_core.shared_contracts.errors import ErrorCode
from os_core.shared_contracts.exceptions import PlatformError


def get_tenant_profile(session: Session, *, tenant_id: str) -> dict[str, Any] | None:
  """读取 tenant_profiles 单行。

  功能：按 tenant_id 查询租户配置真源。
  业务含义：Registry profile · Studio Prove shadow_mode · pack_mappings 载体。
  参数 tenant_id：多厂隔离键。
  返回：行 dict 或 None（未开通）。
  """
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
  """列出租户 system_relations。

  功能：查询 Connector Pack 与租户绑定关系。
  业务含义：Studio Connect/Registry 读真源 · T-03 配置门禁输入。
  参数 tenant_id：租户 ID。
  返回：relation 行列表（body 为原始文本）。
  """
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
  参数 tenant_id · pack_id：授权键。
  返回：True 表示已授权。
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
  参数 tenant_id · pack_id：绑定键。
  返回：True 表示已配置。
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
  """读取 profile_json.connector_overrides（P-03 Override 差量）。

  功能：解析 tenant_profiles.profile_json 中的 Pack 级覆盖。
  业务含义：Connect 步 base_url 等差量配置，不写死仓库。
  返回：pack_id → override dict；无配置时 {}。
  """
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
  """幂等创建 system_relations 行（P-02 import）。

  功能：无则 INSERT，有则跳过。
  业务含义：Path 模板开通 · Studio Connect 落库共用写入路径。
  参数 registry_key：可选 path 模板或 studio 注册来源标记。
  """
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
  """幂等授权 tenant_pack_entitlements（P-02 import）。

  功能：DELETE+INSERT 保证 licensed=1。
  业务含义：Pack 绑定后须同步授权，否则 execution 报 MODULE_NOT_LICENSED。
  参数 tenant_id · pack_id：授权键。
  """
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
  """tenant_pack_entitlements 已授权 Pack ID 列表（M-01 tools/list）。

  功能：按 tenant_id 列出 licensed=1 的 pack_id。
  业务含义：Agent/MCP 工具枚举可用 Connector Pack。
  返回：排序后的 pack_id 字符串列表。
  """
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


def save_pack_mapping_config(
  session: Session,
  *,
  tenant_id: str,
  pack_id: str,
  mappings: dict[str, Any],
  secrets_ref: str | None = None,
) -> dict[str, Any]:
  """Studio Map 步：pack_mappings 写入 profile_json。

  功能：按 pack_id 存储映射与 secrets_ref。
  业务含义：STU-11 凭证引用落库 · 禁止明文 secret 字段。
  参数 mappings · secrets_ref：映射树与 Vault 引用。
  返回：落库后的 stored dict。
  """
  # 业务：合并 pack_mappings 到 profile_json 后 INSERT 或 UPDATE tenant_profiles
  existing = get_tenant_profile(session, tenant_id=tenant_id)
  profile_data: dict[str, Any] = {}
  if existing and existing.get("profile_json"):
    try:
      parsed = json.loads(existing["profile_json"])
      if isinstance(parsed, dict):
        profile_data = parsed
    except (json.JSONDecodeError, TypeError):
      profile_data = {}
  pack_mappings = profile_data.setdefault("pack_mappings", {})
  stored: dict[str, Any] = {"mappings": mappings}
  if secrets_ref:
    stored["secrets_ref"] = secrets_ref
  pack_mappings[pack_id] = stored
  profile_json_str = json.dumps(profile_data, ensure_ascii=False)
  if existing is None:
    session.execute(
      text(
        """
        INSERT INTO tenant_profiles (
          tenant_id, display_name, path, shadow_mode, write_approved, profile_json
        ) VALUES (
          :tenant_id, :display_name, NULL, 0, 0, :profile_json
        )
        """
      ),
      {
        "tenant_id": tenant_id,
        "display_name": tenant_id,
        "profile_json": profile_json_str,
      },
    )
  else:
    session.execute(
      text(
        "UPDATE tenant_profiles SET profile_json = :profile_json WHERE tenant_id = :tenant_id"
      ),
      {"tenant_id": tenant_id, "profile_json": profile_json_str},
    )
  return stored


def assert_pack_configured_for_tenant(
  session: Session,
  *,
  tenant_id: str,
  pack_id: str,
) -> None:
  """Prove 前置：租户须已注册 Connector Pack。

  功能：存在任意 system_relations 行即视为已配置。
  业务含义：T-03 CONNECTOR_NOT_CONFIGURED 门禁。
  异常：未配置时 PlatformError 403。
  """
  if has_system_relation_for_pack(session, tenant_id=tenant_id, pack_id=pack_id):
    return
  raise PlatformError(
    ErrorCode.CONNECTOR_NOT_CONFIGURED,
    f"Connector pack {pack_id} not configured for tenant {tenant_id}",
    http_status=403,
  )
