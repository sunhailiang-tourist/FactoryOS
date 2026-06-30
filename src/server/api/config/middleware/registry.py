"""Middleware 注册顺序唯一真源。

作用：集中登记 Starlette 中间件栈；每条须 summary/problem/usage。
业务关联：request 链 traces→auth→tenant→quota→metrics（后加先执行）。
上游：config/registry.py register_config
下游：各 config/*/middleware.py
"""
from __future__ import annotations

from dataclasses import dataclass

from fastapi import FastAPI
from server.api.config.auth.middleware import AuthMiddleware
from server.api.config.metrics.middleware import MetricsMiddleware
from server.api.config.quota.middleware import QuotaMiddleware
from server.api.config.tenant.middleware import TenantMiddleware
from server.api.config.traces.middleware import TracesMiddleware
from starlette.middleware.base import BaseHTTPMiddleware


@dataclass(frozen=True, slots=True)
class MiddlewareEntry:
  """中间件注册项（打开本文件即可见职责与顺序）。"""

  name: str
  summary: str
  problem: str
  usage: str
  middleware_cls: type[BaseHTTPMiddleware]


# Starlette：后 add_middleware 的请求链路上更靠外（先执行）
MIDDLEWARE_STACK: tuple[MiddlewareEntry, ...] = (
  MiddlewareEntry(
    name="MetricsMiddleware",
    summary="请求计数与延迟 histogram",
    problem="可观测性须统一埋点，避免各路由重复 instrumentation",
    usage="自动包裹全部 HTTP；Prometheus scrape /metrics（若启用）",
    middleware_cls=MetricsMiddleware,
  ),
  MiddlewareEntry(
    name="QuotaMiddleware",
    summary="租户/API 配额限流",
    problem="多租户须防止单 tenant 打满资源",
    usage="按 tenant_id 扣减配额；超限 429",
    middleware_cls=QuotaMiddleware,
  ),
  MiddlewareEntry(
    name="TenantMiddleware",
    summary="解析 X-Tenant-Id 注入 request.state",
    problem="下游 os_core 须一致 tenant 上下文",
    usage="请求头 X-Tenant-Id；缺省 default tenant",
    middleware_cls=TenantMiddleware,
  ),
  MiddlewareEntry(
    name="AuthMiddleware",
    summary="认证（JWT/API Key stub）",
    problem="业务 API 须统一鉴权入口",
    usage="Authorization header；探针路径可跳过",
    middleware_cls=AuthMiddleware,
  ),
  MiddlewareEntry(
    name="TracesMiddleware",
    summary="分布式 trace id 注入与传递",
    problem="跨服务排障须 correlation_id / traceparent",
    usage="响应头回传 trace-id；日志 MDC 关联",
    middleware_cls=TracesMiddleware,
  ),
)


def _add(app: FastAPI, mw: type[BaseHTTPMiddleware]) -> None:
  app.add_middleware(mw)


def register(app: FastAPI) -> None:
  """按 MIDDLEWARE_STACK 顺序注册（见各 entry.usage）。"""
  for entry in MIDDLEWARE_STACK:
    _add(app, entry.middleware_cls)
