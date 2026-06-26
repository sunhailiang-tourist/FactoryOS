"""租户 middleware（S0：解析 X-Tenant-Id，默认 default）。"""
from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from os_core.shared_contracts.context import reset_tenant_id, set_tenant_id


class TenantMiddleware(BaseHTTPMiddleware):
  async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
    tenant_id = request.headers.get("X-Tenant-Id", "default")
    request.state.tenant_id = tenant_id
    token = set_tenant_id(tenant_id)
    try:
      return await call_next(request)
    finally:
      reset_tenant_id(token)
