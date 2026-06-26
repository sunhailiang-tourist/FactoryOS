"""Uvicorn 入口。装配：application/；路由：router/；配置：config/。"""
from __future__ import annotations

from server.api.application.factory import app, create_app

__all__ = ["app", "create_app"]
