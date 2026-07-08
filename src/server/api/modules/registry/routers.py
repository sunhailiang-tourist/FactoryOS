"""Registry 域 router 聚合。

作用：导出 get_routers 供 router/v1/registry 登记。
业务关联：Platform Registry 读 + 变更请求人审。
上游：router/v1/registry · ROUTER_PROVIDERS。
下游：modules/registry/controllers/*。
"""
from __future__ import annotations

from fastapi import APIRouter
from server.api.modules.registry.controllers.registry import router as registry_router
from server.api.modules.registry.controllers.registry_changes import (
  router as registry_changes_router,
)


def get_routers() -> list[APIRouter]:
  """返回本域 APIRouter 列表供 v1 登记。

  功能：聚合 controllers 下子 router。
  业务含义：Registry 域 ROUTER_PROVIDERS 调用入口。
  上游：router/v1/registry。
  下游：modules/registry/controllers/*。
  """
  return [registry_router, registry_changes_router]
