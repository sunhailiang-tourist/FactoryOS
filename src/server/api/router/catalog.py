"""路由清单（治理 / harness 扩展点）。"""
from __future__ import annotations

from server.api.router.v1.registry import ROUTER_PROVIDERS

ROUTE_DOMAINS = tuple(
  provider.__module__.rsplit(".", 1)[-1] for provider in ROUTER_PROVIDERS
)
