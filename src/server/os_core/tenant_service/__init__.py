"""tenant_service 包导出（REST · MCP 共用内核）。

作用：重导出 get/update/resolve_shadow_mode 公开 API。
业务关联：T-01 shadow_mode · MCP Step5 与 REST 同真源。
上游：api/modules/tenant · mcp_gateway
下游：os_core.tenant_service.service
"""
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
