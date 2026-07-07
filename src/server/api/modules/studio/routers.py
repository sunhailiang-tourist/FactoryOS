"""studio 域 router 聚合。"""
from __future__ import annotations

from fastapi import APIRouter
from server.api.modules.studio.controllers.studio import router as studio_router


def get_routers() -> list[APIRouter]:
  return [studio_router]
