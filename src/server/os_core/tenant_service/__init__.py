"""tenant_service 公开 API（REST · MCP 共用）。"""
from os_core.tenant_service.service import (
  get_tenant_settings,
  resolve_shadow_mode,
  update_tenant_settings,
)

__all__ = [
  "get_tenant_settings",
  "update_tenant_settings",
  "resolve_shadow_mode",
]
