"""Traces 中间件。

作用：注入 correlation_id/traceparent 到 request/response。
业务关联：跨服务排障与 MCP 追踪。
上游：middleware/registry。
下游：logs/context · 响应头 trace-id。
"""
from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


class TracesMiddleware(BaseHTTPMiddleware):
  async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
    """Traces 请求链关联（S0 stub · 透传）。

    功能：包裹 call_next 并预留 trace-id/traceparent 注入与回传。
    业务含义：M-03 SEP-414 分布式追踪中间件入口。
    上游：TracesMiddleware · Authorization 内侧。
    下游：call_next · logs/context MDC · 响应头 trace-id。
    """
    return await call_next(request)
