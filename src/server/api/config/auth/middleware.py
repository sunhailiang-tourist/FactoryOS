"""鉴权 middleware — Studio RBAC（STU-09）。

作用：解析 X-Actor-Role / X-Actor-User-Id；/v1/studio/* 仅 integrator 等角色可访问。
业务关联：Integration Studio 规格 §4 · AUTH_STUDIO_FORBIDDEN。
上游：config/middleware/registry.py · contracts/error-registry.yaml
下游：request.state.actor_role · Studio 路由
"""
from __future__ import annotations

from server.api.config.status_code.responses import build_error_payload
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from os_core.shared_contracts.errors import ErrorCode, default_message

STUDIO_PATH_PREFIX = "/v1/studio/"
STUDIO_ALLOWED_ROLES = frozenset(
  {
    "integrator",
    "admin",
    "platform",
    "business_owner",
    "customer_it",
  }
)


class AuthMiddleware(BaseHTTPMiddleware):
  """解析 actor 头；Studio 路径 RBAC 守门。"""

  async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
    role = (request.headers.get("X-Actor-Role") or "operator").strip().lower()
    user_id = (request.headers.get("X-Actor-User-Id") or "").strip()
    request.state.actor_role = role
    request.state.actor_user_id = user_id

    if request.url.path.startswith(STUDIO_PATH_PREFIX):
      if role not in STUDIO_ALLOWED_ROLES:
        trace_id = request.headers.get("X-Request-Id") or request.headers.get("X-Request-ID")
        return JSONResponse(
          status_code=403,
          content=build_error_payload(
            ErrorCode.AUTH_STUDIO_FORBIDDEN.value,
            default_message(ErrorCode.AUTH_STUDIO_FORBIDDEN),
            details={"role": role, "path": request.url.path},
            trace_id=trace_id,
          ),
        )

    return await call_next(request)
