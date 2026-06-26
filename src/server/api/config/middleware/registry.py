"""Middleware 注册顺序唯一真源。"""
from __future__ import annotations

from fastapi import FastAPI
from server.api.config.auth.middleware import AuthMiddleware
from server.api.config.metrics.middleware import MetricsMiddleware
from server.api.config.quota.middleware import QuotaMiddleware
from server.api.config.tenant.middleware import TenantMiddleware
from server.api.config.traces.middleware import TracesMiddleware
from starlette.middleware.base import BaseHTTPMiddleware


def _add(app: FastAPI, mw: type[BaseHTTPMiddleware]) -> None:
  app.add_middleware(mw)


def register(app: FastAPI) -> None:
  """S0 顺序：traces → auth → tenant → quota → metrics（Starlette 后加先执行）。"""
  _add(app, MetricsMiddleware)
  _add(app, QuotaMiddleware)
  _add(app, TenantMiddleware)
  _add(app, AuthMiddleware)
  _add(app, TracesMiddleware)
