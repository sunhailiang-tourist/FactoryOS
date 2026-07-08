"""Quota 中间件。

作用：请求前检查租户配额，超限返回 429。
业务关联：防止单 tenant 打满资源。
上游：middleware/registry · quota/checker。
下游：HTTP 429 · metrics 计数。
"""
from __future__ import annotations

from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response


class QuotaMiddleware(BaseHTTPMiddleware):
  async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
    """Quota 租户配额检查（S0 stub · 透传）。

    功能：包裹 call_next 并预留 quota/checker 扣减与 429 拦截。
    业务含义：多租户公平使用 · 防单 tenant 打满资源。
    上游：QuotaMiddleware · tenant_id 已注入后。
    下游：call_next · 超限 HTTP 429 · metrics 计数。
    """
    return await call_next(request)
