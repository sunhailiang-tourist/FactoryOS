"""Audit 域 router 聚合。

作用：导出 get_routers 供 router/v1/registry 登记。
业务关联：E-03 append-only 审计查询。
上游：router/v1/registry · ROUTER_PROVIDERS。
下游：modules/audit/controllers/*。
"""
from __future__ import annotations

from fastapi import APIRouter
from server.api.modules.audit.controllers.audit import router


def get_routers() -> list[APIRouter]:
  """返回本域 APIRouter 列表供 v1 登记。

  功能：聚合 controllers 下子 router。
  业务含义：Audit 域 ROUTER_PROVIDERS 调用入口。
  上游：router/v1/registry。
  下游：modules/audit/controllers/*。
  """
  return [router]
