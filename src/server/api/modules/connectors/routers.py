"""域 router 聚合 export。"""
from __future__ import annotations

from fastapi import APIRouter
from server.api.modules.connectors.controllers.connectors import router


def get_routers() -> list[APIRouter]:
  return [router]
