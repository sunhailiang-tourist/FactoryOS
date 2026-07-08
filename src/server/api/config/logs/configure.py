"""日志配置。

作用：init() 配置 root logger 格式与级别。
业务关联：全链路可观测性基础。
上游：config/registry register_config。
下游：logs/context · middleware traces。
"""
from __future__ import annotations


def init() -> None:
  """初始化 root logger 格式与级别。

  功能：配置结构化日志输出。
  业务含义：全服务统一日志契约。
  上游：register_config。
  下游：logs/context MDC。
  """
