"""MCP 域 router 聚合。

作用：导出 get_routers 供 router/v1/registry 登记。
业务关联：W7 MCP JSON-RPC 网关。
上游：router/v1/registry · ROUTER_PROVIDERS。
下游：modules/mcp/controllers/*。
"""
from __future__ import annotations

from fastapi import APIRouter
from server.api.modules.mcp.controllers.mcp import router as mcp_router


def get_routers() -> list[APIRouter]:
  """返回本域 APIRouter 列表供 v1 登记。

  功能：聚合 controllers 下子 router。
  业务含义：MCP 域 ROUTER_PROVIDERS 调用入口。
  上游：router/v1/registry。
  下游：modules/mcp/controllers/*。
  """
  return [mcp_router]
