"""Agent 域 router 聚合。

作用：导出 get_routers 供 router/v1/registry 登记。
业务关联：H-01 意图→DslPlan（不写 Legacy）。
上游：router/v1/registry · ROUTER_PROVIDERS。
下游：modules/agent/controllers/*。
"""
from __future__ import annotations

from fastapi import APIRouter
from server.api.modules.agent.controllers.agent import router as agent_router


def get_routers() -> list[APIRouter]:
  """返回本域 APIRouter 列表供 v1 登记。

  功能：聚合 controllers 下子 router。
  业务含义：Agent 域 ROUTER_PROVIDERS 调用入口。
  上游：router/v1/registry。
  下游：modules/agent/controllers/*。
  """
  return [agent_router]
