"""域 router 聚合 export。"""
from __future__ import annotations

from fastapi import APIRouter
from server.api.modules.harness.controllers.harness import router as harness_router


def get_routers() -> list[APIRouter]:
  return [harness_router]
