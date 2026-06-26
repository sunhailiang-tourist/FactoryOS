"""域 router 聚合 export。"""
from __future__ import annotations

from fastapi import APIRouter
from server.api.modules.execution.controllers.execute import router as execute_router
from server.api.modules.execution.controllers.executions import router as executions_router


def get_routers() -> list[APIRouter]:
  return [execute_router, executions_router]
