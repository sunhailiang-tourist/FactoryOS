"""Studio 域 router 聚合。

作用：导出 get_routers 供 router/v1/registry 登记。
业务关联：Studio RBAC · 平台管理 API。
上游：router/v1/registry · ROUTER_PROVIDERS。
下游：modules/studio/controllers/*。
"""
from __future__ import annotations

from fastapi import APIRouter
from server.api.modules.studio.controllers.studio import router as studio_router


def get_routers() -> list[APIRouter]:
  """返回本域 APIRouter 列表供 v1 登记。

  功能：聚合 controllers 下子 router。
  业务含义：Studio 域 ROUTER_PROVIDERS 调用入口。
  上游：router/v1/registry。
  下游：modules/studio/controllers/*。
  """
  return [studio_router]
