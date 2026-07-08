"""Auth 中间件。

作用：认证并注入 request.state.actor。
业务关联：业务 API 鉴权链；探针路径可跳过。
上游：middleware/registry · Authorization header。
下游：auth/dependencies · modules controllers。
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
    """Auth 鉴权与 Studio RBAC（解析 X-Actor-* 头）。

    功能：注入 actor_role/user_id；Studio 路径校验 integrator 等角色。
    业务含义：STU-09 统一鉴权链；operator 禁止 /v1/studio/*。
    上游：Authorization · X-Actor-Role · X-Actor-User-Id。
    下游：call_next · 403 AUTH_STUDIO_FORBIDDEN · auth/dependencies。
    """
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
