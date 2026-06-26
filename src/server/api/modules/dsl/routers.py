"""域 router 聚合 export。"""
from __future__ import annotations

from fastapi import APIRouter
from server.api.modules.dsl.controllers.dsl import router


def get_routers() -> list[APIRouter]:
  return [router]
