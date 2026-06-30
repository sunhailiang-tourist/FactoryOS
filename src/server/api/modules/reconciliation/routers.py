"""reconciliation 域 router 聚合。"""
from __future__ import annotations

from fastapi import APIRouter
from server.api.modules.reconciliation.controllers.reconciliation import (
  router as reconciliation_router,
)


def get_routers() -> list[APIRouter]:
  return [reconciliation_router]
