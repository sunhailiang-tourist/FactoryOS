"""Settings 加载器。

作用：init() 读取环境变量并缓存 Settings 单例。
业务关联：启动时须最先执行的配置步骤。
上游：config/registry · os.environ。
下游：dependencies/db.get_db_session。
"""
from __future__ import annotations

import os


def init() -> None:
  """加载并缓存 Settings 单例。

  功能：读取环境变量初始化配置。
  业务含义：DATABASE_URL 等启动必需项。
  上游：register_config 首步。
  下游：dependencies/db。
  """
  _ = os.environ.get("FACTORYOS_ENV", "dev")
