"""统一错误 JSON 形状。

作用：所有 API 失败响应共用的 body 构造。
业务关联：contracts/error-registry.yaml · FactoryOSError schema。
上游：handlers.py · auth middleware
下游：FastAPI JSONResponse
关联文档：docs/文档/规格说明/状态码与错误约定.md
"""
from __future__ import annotations

from typing import Any


def build_error_payload(
  code: str,
  message: str,
  *,
  details: Any | None = None,
  trace_id: str | None = None,
  upstream: dict[str, str] | None = None,
) -> dict[str, Any]:
  """构造标准错误体；过渡期双写 detail=message。"""
  body: dict[str, Any] = {
    "code": code,
    "message": message,
    "detail": message,
  }
  if details is not None:
    body["details"] = details
  if trace_id:
    body["trace_id"] = trace_id
  if upstream is not None:
    body["upstream"] = upstream
  return body
