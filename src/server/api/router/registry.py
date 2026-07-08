"""HTTP 路由注册总入口。

作用：register_routers 挂载 v1 与 catalog 路由。
业务关联：业务域路由须在 config 之后注册。
上游：application/assemble。
下游：router/v1/registry · router/catalog。
"""
from __future__ import annotations

from fastapi import FastAPI
from server.api.router.v1.registry import register_v1


def register_routers(app: FastAPI) -> None:
  """挂载 v1 业务路由与 catalog。

  功能：调用 register_v1 与 catalog 路由。
  业务含义：业务 HTTP 面注册入口。
  上游：assemble(app)。
  下游：router/v1/registry。
  """
  register_v1(app)
