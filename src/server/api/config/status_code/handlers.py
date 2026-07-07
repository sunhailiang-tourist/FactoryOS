"""FastAPI 异常 → 统一 JSON（code + message + detail 兼容）。

作用：PlatformError · HTTPException · 422 · 500 唯一出口。
业务关联：AC 负向断言 · STU-09 AUTH_STUDIO_FORBIDDEN。
上游：os_core.PlatformError · contracts/error-registry.yaml
下游：config/registry.register_config
关联文档：docs/文档/规格说明/状态码与错误约定.md
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
  """PlatformError → 标准错误体。"""
  return JSONResponse(
    status_code=exc.http_status,
    content=build_error_payload(
      exc.code.value,
      exc.message,
      trace_id=_trace_id(request),
    ),
  )


def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
  """HTTPException → 尽量保留 code；否则按状态映射。"""
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
  """Pydantic/FastAPI 422 → VAL_SCHEMA_FAILED + details 数组。"""
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
  """未捕获异常 → INTERNAL_ERROR（不泄露栈）。"""
  _ = exc
  return JSONResponse(
    status_code=500,
    content=build_error_payload(
      ErrorCode.INTERNAL_ERROR.value,
      default_message(ErrorCode.INTERNAL_ERROR),
      trace_id=_trace_id(request),
    ),
  )
