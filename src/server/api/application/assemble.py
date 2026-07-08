"""应用装配（config → router）。

作用：按固定顺序注册横切 config 与业务 router。
业务关联：FastAPI 启动装配真源。
上游：factory.create_app。
下游：config/registry · router/registry。
"""
from __future__ import annotations

from fastapi import FastAPI
from server.api.config.registry import register_config
from server.api.router.registry import register_routers


def assemble(app: FastAPI) -> None:
  """装配 FastAPI：先 config 后 router。

  功能：调用 register_config 与 register_routers。
  业务含义：应用启动装配顺序锁死。
  上游：factory.create_app。
  下游：config/registry · router/registry。
  """
  register_config(app)
  register_routers(app)
