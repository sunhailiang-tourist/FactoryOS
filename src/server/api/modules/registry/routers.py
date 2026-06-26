"""域 router 聚合 export。"""
from __future__ import annotations

from fastapi import APIRouter
from server.api.modules.registry.controllers.registry import router as registry_router
from server.api.modules.registry.controllers.registry_changes import (
  router as registry_changes_router,
)


def get_routers() -> list[APIRouter]:
  return [registry_router, registry_changes_router]
