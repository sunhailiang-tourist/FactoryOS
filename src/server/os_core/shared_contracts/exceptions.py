"""平台业务异常（带 ErrorCode · HTTP 状态）。

作用：os_core 各 service 抛出；server/api 统一映射 JSON 响应。
业务关联：G-03 GRAPH_NOT_FROZEN · R-01 RULE_DENIED · D-02 DSL_UNKNOWN。
上游：shared_contracts.errors
下游：execution_service · graph_service · rule_engine · FastAPI handler
"""
from __future__ import annotations

from os_core.shared_contracts.errors import ErrorCode, default_message


class PlatformError(Exception):
  """可预期的平台拒绝（非 500）。

  功能：携带机器可读 code 与建议 HTTP 状态。
  业务含义：execute/freeze 等负向 AC 断言真源。
  """

  def __init__(
    self,
    code: ErrorCode,
    message: str | None = None,
    *,
    http_status: int = 400,
  ) -> None:
    """构造可预期业务异常。

    功能：绑定 ErrorCode · 文案 · 建议 HTTP 状态。
    业务含义：负向 AC 与 Gate 拒绝的统一抛出类型。
    参数 code：机器可读错误码；message 默认取 SSOT 中文。
    参数 http_status：API 层映射用（如 403 RULE_DENIED）。
    """
    msg = default_message(code) if message is None else message
    super().__init__(msg)
    self.code = code
    self.message = msg
    self.http_status = http_status
