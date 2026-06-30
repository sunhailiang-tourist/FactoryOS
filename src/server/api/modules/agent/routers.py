"""域 router 聚合 export。"""
from __future__ import annotations

from fastapi import APIRouter
from server.api.modules.agent.controllers.agent import router as agent_router


def get_routers() -> list[APIRouter]:
  return [agent_router]
