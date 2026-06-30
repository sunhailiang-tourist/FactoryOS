"""v1 HTTP 路由注册表 — 开发者第一站。"""
from __future__ import annotations

from collections.abc import Callable

from fastapi import APIRouter, FastAPI
from server.api.modules import (
  agent,
  audit,
  connectors,
  dsl,
  execution,
  graphs,
  harness,
  probes,
  reconciliation,
  registry,
  rulesets,
)

RouteProvider = Callable[[], list[APIRouter]]

ROUTER_PROVIDERS: tuple[RouteProvider, ...] = (
  probes.get_routers,
  graphs.get_routers,
  agent.get_routers,
  harness.get_routers,
  reconciliation.get_routers,
  execution.get_routers,
  registry.get_routers,
  connectors.get_routers,
  rulesets.get_routers,
  dsl.get_routers,
  audit.get_routers,
)


def register_v1(app: FastAPI) -> None:
  for provider in ROUTER_PROVIDERS:
    for router in provider():
      app.include_router(router)
