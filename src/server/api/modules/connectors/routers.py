"""Connectors 域 router 聚合。

作用：导出 get_routers 供 router/v1/registry 登记。
业务关联：Connector Pack 健康检查。
上游：router/v1/registry · ROUTER_PROVIDERS。
下游：modules/connectors/controllers/*。
"""
from __future__ import annotations

from fastapi import APIRouter
from server.api.modules.connectors.controllers.connectors import router


def get_routers() -> list[APIRouter]:
  """返回本域 APIRouter 列表供 v1 登记。

  功能：聚合 controllers 下子 router。
  业务含义：Connectors 域 ROUTER_PROVIDERS 调用入口。
  上游：router/v1/registry。
  下游：modules/connectors/controllers/*。
  """
  return [router]
