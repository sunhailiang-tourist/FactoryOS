"""integration 域 router 聚合。"""
from __future__ import annotations

from fastapi import APIRouter
from server.api.modules.integration.controllers.integration import (
  router as integration_router,
)


def get_routers() -> list[APIRouter]:
  return [integration_router]
