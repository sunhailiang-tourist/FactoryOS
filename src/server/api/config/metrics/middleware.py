"""指标 middleware（S0 pass-through）。"""
from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


class MetricsMiddleware(BaseHTTPMiddleware):
  async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
    return await call_next(request)
