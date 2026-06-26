"""FastAPI PlatformError → JSON（code + detail）。

作用：对齐 AC 负向断言 GRAPH_NOT_FROZEN · RULE_DENIED 等。
上游：os_core.*.PlatformError
下游：apps/api/main 注册
"""
from __future__ import annotations

from fastapi import Request
from fastapi.responses import JSONResponse

from os_core.shared_contracts.exceptions import PlatformError


def platform_error_handler(_request: Request, exc: PlatformError) -> JSONResponse:
  """将 PlatformError 映射为统一 JSON 错误体。"""
  return JSONResponse(
    status_code=exc.http_status,
    content={"detail": exc.message, "code": exc.code.value},
  )
