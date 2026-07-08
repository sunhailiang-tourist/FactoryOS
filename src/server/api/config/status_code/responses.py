"""错误响应体构建。

作用：build_error_payload 组装标准错误 JSON。
业务关联：OpenAPI ErrorResponse 契约。
上游：status_code/handlers。
下游：HTTP 响应 body。
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
  """组装标准错误 JSON 载荷。

  功能：合并 error_code · message · details。
  业务含义：OpenAPI ErrorResponse 契约真源。
  上游：status_code/handlers。
  返回：dict 可 JSON 序列化。
  """
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
