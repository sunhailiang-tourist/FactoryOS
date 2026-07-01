"""mcp 域 router 聚合。"""
from __future__ import annotations

from fastapi import APIRouter
from server.api.modules.mcp.controllers.mcp import router as mcp_router


def get_routers() -> list[APIRouter]:
  return [mcp_router]
