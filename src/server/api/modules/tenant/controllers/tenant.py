"""Tenant 域 HTTP 路由（OpenAPI /v1/tenants/{tenantId}/settings）。

作用：薄路由；业务在 os_core.tenant_service（MCP Step5 复用同一内核）。
业务关联：T-01 shadow_mode。
上游：modules/tenant/routers
下游：os_core.tenant_service
"""
from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from pydantic import BaseModel, ConfigDict, Field
from server.api.config.dependencies.db import get_db_session
from sqlalchemy.orm import Session

from os_core.tenant_service import get_tenant_settings, update_tenant_settings

router = APIRouter(tags=["Tenant"])


class TenantSettingsBody(BaseModel):
  """OpenAPI TenantSettings + 内部 write_approved。"""

  model_config = ConfigDict(extra="forbid")

  shadow_mode: bool | None = Field(default=None, description="租户 Shadow 开关")
  write_approved: bool | None = Field(default=None, description="Harness 生产写批准")
  default_ruleset_id: str | None = Field(default=None, description="默认 RuleSet（预留）")
  im_connector: str | None = Field(default=None, description="默认 IM Connector（预留）")
  connector_overrides: dict[str, dict[str, Any]] | None = Field(
    default=None,
    description="Pack 级 Override（P-03 base_url 等）",
  )


def _response_payload(settings: dict[str, Any]) -> dict[str, Any]:
  """HTTP 响应：OpenAPI TenantSettings 字段。"""
  out: dict[str, Any] = {
    "shadow_mode": settings.get("shadow_mode", False),
  }
  if settings.get("default_ruleset_id") is not None:
    out["default_ruleset_id"] = settings["default_ruleset_id"]
  if settings.get("im_connector") is not None:
    out["im_connector"] = settings["im_connector"]
  return out


@router.get("/v1/tenants/{tenant_id}/settings")
def get_tenant_settings_http(
  tenant_id: str,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """GET /v1/tenants/{tenantId}/settings。"""
  settings = get_tenant_settings(session, tenant_id=tenant_id)
  return _response_payload(settings)


@router.put("/v1/tenants/{tenant_id}/settings")
def put_tenant_settings_http(
  tenant_id: str,
  body: TenantSettingsBody,
  session: Session = Depends(get_db_session),
) -> dict[str, Any]:
  """PUT /v1/tenants/{tenantId}/settings（含 shadow_mode）。"""
  settings = update_tenant_settings(
    session,
    tenant_id=tenant_id,
    shadow_mode=body.shadow_mode,
    write_approved=body.write_approved,
    connector_overrides=body.connector_overrides,
  )
  return _response_payload(settings)
