"""全局异常处理器。

作用：PlatformError/HTTPException/ValidationError 统一 JSON 响应。
业务关联：客户端可解析 error_code · message。
上游：config/registry add_exception_handler。
下游：HTTP JSON ProblemDetails。
"""
from __future__ import annotations

from fastapi import HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from server.api.config.status_code.responses import build_error_payload

from os_core.shared_contracts.errors import ErrorCode, default_message
from os_core.shared_contracts.exceptions import PlatformError


def _trace_id(request: Request) -> str | None:
  """与 X-Request-Id 对齐（若存在）。"""
  return request.headers.get("X-Request-Id") or request.headers.get("X-Request-ID")


def platform_error_handler(request: Request, exc: PlatformError) -> JSONResponse:
  """PlatformError → JSON ProblemDetails。

  功能：映射 error_code 到 HTTP status 并序列化。
  业务含义：os_core 业务异常统一 HTTP 出口。
  上游：os_core PlatformError raise。
  下游：JSONResponse · build_error_payload。
  """
  return JSONResponse(
    status_code=exc.http_status,
    content=build_error_payload(
      exc.code.value,
      exc.message,
      trace_id=_trace_id(request),
    ),
  )


def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
  """HTTPException → JSON 响应。

  功能：包装 Starlette HTTPException 为标准 JSON。
  业务含义：FastAPI 内置异常对齐契约。
  上游：FastAPI route raise HTTPException。
  下游：JSONResponse。
  """
  detail = exc.detail
  code = ErrorCode.UNKNOWN_ERROR.value
  message = str(detail)
  details = None

  if isinstance(detail, dict):
    raw_code = detail.get("code")
    if isinstance(raw_code, str) and raw_code:
      code = raw_code
    message = str(detail.get("message") or detail.get("detail") or detail)
    details = detail.get("details")
  elif exc.status_code == 404:
    code = ErrorCode.REG_RESOURCE_NOT_FOUND.value
  elif exc.status_code == 422:
    code = ErrorCode.VAL_SCHEMA_FAILED.value
  elif exc.status_code == 400:
    code = ErrorCode.VAL_BAD_REQUEST.value

  return JSONResponse(
    status_code=exc.status_code,
    content=build_error_payload(
      code,
      message,
      details=details,
      trace_id=_trace_id(request),
    ),
  )


def validation_exception_handler(
  request: Request,
  exc: RequestValidationError,
) -> JSONResponse:
  """RequestValidationError → 422 JSON。

  功能：Pydantic 校验失败转 ProblemDetails。
  业务含义：OpenAPI 请求体验证错误统一格式。
  上游：FastAPI/Pydantic 校验。
  下游：422 JSONResponse。
  """
  return JSONResponse(
    status_code=422,
    content=build_error_payload(
      ErrorCode.VAL_SCHEMA_FAILED.value,
      default_message(ErrorCode.VAL_SCHEMA_FAILED),
      details=exc.errors(),
      trace_id=_trace_id(request),
    ),
  )


def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
  """未捕获异常 → 500 JSON。

  功能：兜底异常处理并记录日志。
  业务含义：防止堆栈泄露；返回通用 500。
  上游：未预期 Exception。
  下游：500 JSONResponse · logs。
  """
  _ = exc
  return JSONResponse(
    status_code=500,
    content=build_error_payload(
      ErrorCode.INTERNAL_ERROR.value,
      default_message(ErrorCode.INTERNAL_ERROR),
      trace_id=_trace_id(request),
    ),
  )
