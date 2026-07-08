"""Metrics 中间件。

作用：HTTP 请求计数与延迟 histogram。
业务关联：全路由自动埋点。
上游：middleware/registry MIDDLEWARE_STACK。
下游：Prometheus client。
"""
from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


class MetricsMiddleware(BaseHTTPMiddleware):
  async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
    """Metrics 请求链埋点（S0 stub · 透传）。

    功能：包裹 call_next 并预留请求计数/延迟 histogram 钩子。
    业务含义：Prometheus 全路由自动 instrumentation 入口。
    上游：MetricsMiddleware · MIDDLEWARE_STACK 最外层。
    下游：call_next · quota/tenant/auth/traces 内层。
    """
    return await call_next(request)
