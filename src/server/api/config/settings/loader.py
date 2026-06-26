"""pydantic-settings 加载（S0 最小实现）。"""
from __future__ import annotations

import os


def init() -> None:
  """初始化 settings（S0：读取 ENV 占位）。"""
  _ = os.environ.get("FACTORYOS_ENV", "dev")
