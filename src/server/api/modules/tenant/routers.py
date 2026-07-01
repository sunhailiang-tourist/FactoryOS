"""tenant 域 router 聚合。"""
from __future__ import annotations

from fastapi import APIRouter
from server.api.modules.tenant.controllers.tenant import router as tenant_router


def get_routers() -> list[APIRouter]:
  return [tenant_router]
