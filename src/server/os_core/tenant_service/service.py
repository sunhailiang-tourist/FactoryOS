"""租户设置内核服务（T-01 · MCP 对外预留共用真源）。

作用：shadow_mode / write_approved 读写；execution 与 MCP 均调 resolve_shadow_mode。
业务关联：TenantSettings OpenAPI · Shadow-Mode 规格。
上游：platform_registry.tenant_config_store
下游：execution_service · mcp_gateway（W7 Step5）
关联文档：contracts/openapi/工厂操作系统-v1.1.yaml · TenantSettings
"""
from __future__ import annotations

from typing import Any

from sqlalchemy.orm import Session

from os_core.platform_registry import tenant_config_store
from os_core.shared_contracts.errors import ErrorCode
from os_core.shared_contracts.exceptions import PlatformError


def _profile_to_settings(profile: dict[str, Any]) -> dict[str, Any]:
  """DB tenant_profiles → OpenAPI TenantSettings 子集 + write_approved（内部）。"""
  return {
    "tenant_id": profile["tenant_id"],
    "shadow_mode": bool(profile.get("shadow_mode")),
    "write_approved": bool(profile.get("write_approved")),
    "default_ruleset_id": None,
    "im_connector": None,
  }


def get_tenant_settings(session: Session, *, tenant_id: str) -> dict[str, Any]:
  """读取租户设置；无行时 404。

  功能：GET /v1/tenants/{id}/settings 业务真源。
  业务含义：MCP tools/call 与 REST execute 须读同一 shadow 开关。
  """
  profile = tenant_config_store.get_tenant_profile(session, tenant_id=tenant_id)
  if profile is None:
    raise PlatformError(
      ErrorCode.TENANT_FORBIDDEN,
      f"Tenant not found: {tenant_id}",
      http_status=404,
    )
  return _profile_to_settings(profile)


def update_tenant_settings(
  session: Session,
  *,
  tenant_id: str,
  shadow_mode: bool | None = None,
  write_approved: bool | None = None,
  connector_overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
  """更新 shadow_mode / write_approved / connector_overrides（upsert）。

  功能：PUT /v1/tenants/{id}/settings。
  业务含义：Studio / API / 未来 MCP admin 工具均经此入口，禁止散落写 DB。
  参数 connector_overrides：P-03 Pack 级 Override（如 base_url）。
  """
  profile = tenant_config_store.upsert_tenant_settings(
    session,
    tenant_id=tenant_id,
    shadow_mode=shadow_mode,
    write_approved=write_approved,
    connector_overrides=connector_overrides,
  )
  session.commit()
  return _profile_to_settings(profile)


def resolve_shadow_mode(session: Session, *, tenant_id: str) -> bool:
  """execution / MCP 用：租户是否处于 Shadow（不写 Legacy）。

  功能：L2 写前门禁；与 dry_run 合并为 effective_shadow。
  业务含义：MCP tools/call 与 POST /v1/execute 语义一致，均读此函数。
  """
  profile = tenant_config_store.get_tenant_profile(session, tenant_id=tenant_id)
  if profile is None:
    return False
  return bool(profile.get("shadow_mode"))
