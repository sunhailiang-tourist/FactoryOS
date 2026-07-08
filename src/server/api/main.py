"""Uvicorn 入口（api/main.py）。

作用：导出 app/create_app 供 uvicorn 与测试加载。
业务关联：Modular Monolith HTTP 进程入口。
上游：uvicorn · pytest TestClient。
下游：application/factory · router · config。
"""
from __future__ import annotations

from server.api.application.factory import app, create_app

__all__ = ["app", "create_app"]
