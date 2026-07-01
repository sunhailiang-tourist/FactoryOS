"""package 域 router 聚合。"""
from __future__ import annotations

from fastapi import APIRouter
from server.api.modules.package.controllers.package import router as package_router


def get_routers() -> list[APIRouter]:
  return [package_router]
