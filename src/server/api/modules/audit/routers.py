"""域 router 聚合 export。"""
from __future__ import annotations

from fastapi import APIRouter
from server.api.modules.audit.controllers.audit import router


def get_routers() -> list[APIRouter]:
  return [router]
