"""应用装配：config → router。"""
from __future__ import annotations

from fastapi import FastAPI
from server.api.config.registry import register_config
from server.api.router.registry import register_routers


def assemble(app: FastAPI) -> None:
  register_config(app)
  register_routers(app)
