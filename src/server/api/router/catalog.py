"""路由目录只读 API。

作用：暴露已登记 HTTP 域清单供运维/文档生成。
业务关联：check_router_registry 对齐真源。
上游：router/v1/registry API_ROUTER_DOMAINS。
下游：GET 路由元数据响应。
"""
from __future__ import annotations

from server.api.router.v1.registry import ROUTER_PROVIDERS

ROUTE_DOMAINS = tuple(
  provider.__module__.rsplit(".", 1)[-1] for provider in ROUTER_PROVIDERS
)
