"""全站路由注册唯一入口。"""
from __future__ import annotations

from fastapi import FastAPI
from server.api.router.v1.registry import register_v1


def register_routers(app: FastAPI) -> None:
  register_v1(app)
