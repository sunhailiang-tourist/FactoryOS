"""Execution 域 router 聚合。

作用：导出 get_routers 供 router/v1/registry 登记。
业务关联：E-02 L2 执行 · E-04/E-05 revert。
上游：router/v1/registry · ROUTER_PROVIDERS。
下游：modules/execution/controllers/*。
"""
from __future__ import annotations

from fastapi import APIRouter
from server.api.modules.execution.controllers.execute import router as execute_router
from server.api.modules.execution.controllers.executions import router as executions_router


def get_routers() -> list[APIRouter]:
  """返回本域 APIRouter 列表供 v1 登记。

  功能：聚合 controllers 下子 router。
  业务含义：Execution 域 ROUTER_PROVIDERS 调用入口。
  上游：router/v1/registry。
  下游：modules/execution/controllers/*。
  """
  return [execute_router, executions_router]
