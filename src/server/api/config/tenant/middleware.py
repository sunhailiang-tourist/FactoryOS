"""租户 middleware（X-Tenant-Id）。

作用：解析 X-Tenant-Id 注入 request.state 与 contextvar。
业务关联：多租户上下文真源；缺省 default。
上游：middleware/registry · HTTP 请求头。
下游：tenant/dependencies · os_core tenant 上下文。
"""
from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from os_core.shared_contracts.context import reset_tenant_id, set_tenant_id


class TenantMiddleware(BaseHTTPMiddleware):
  async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
    """Tenant 上下文注入（解析 X-Tenant-Id）。

    功能：写入 request.state.tenant_id 与 contextvar；请求结束 reset。
    业务含义：T-01 多租户真源；缺省 default tenant。
    上游：X-Tenant-Id header · middleware/registry 顺序。
    下游：tenant/dependencies · quota checker · os_core 读上下文。
    """
    tenant_id = request.headers.get("X-Tenant-Id", "default")
    request.state.tenant_id = tenant_id
    token = set_tenant_id(tenant_id)
    try:
      return await call_next(request)
    finally:
      reset_tenant_id(token)
