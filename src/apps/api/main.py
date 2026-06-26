"""apps/api HTTP 入口工厂。

作用：FastAPI 应用装配与进程级探针路由。
业务关联：W1 工程底座；生产唯一 deployable。
上游：Uvicorn / ASGI 宿主、pytest ASGITransport
下游：后续 os_core 路由模块（W2+）
关联文档：contracts/openapi/工厂操作系统-v1.1.yaml · apps/api/README.md
"""
from __future__ import annotations

from fastapi import FastAPI

from apps.api.error_handlers import platform_error_handler
from apps.api.routes.audit import router as audit_router
from apps.api.routes.connectors import router as connectors_router
from apps.api.routes.dsl import router as dsl_router
from apps.api.routes.execute import router as execute_router
from apps.api.routes.executions import router as executions_router
from apps.api.routes.graphs import router as graphs_router
from apps.api.routes.rulesets import router as rulesets_router
from os_core.shared_contracts.exceptions import PlatformError


def create_app() -> FastAPI:
  """创建 FastAPI 应用实例。

  功能：注册基础探针路由；W1 Step4 挂载 /v1/connectors health。
  业务含义：Control Plane 与 CI 须能探测进程存活后再扩展 /v1/*。
  上游调用方：uvicorn、单元/工作流测试
  下游被调方：routes 子模块（graph、execute 等 W2+）
  返回：已配置的 FastAPI 实例（未绑定监听端口）
  """
  application = FastAPI(
    title="FactoryOS API",
    version="0.1.0-w3",
    description="Manufacturing AI execution platform — Modular Monolith entry",
  )
  application.add_exception_handler(PlatformError, platform_error_handler)  # type: ignore[arg-type]

  application.include_router(connectors_router)
  application.include_router(graphs_router)
  application.include_router(rulesets_router)
  application.include_router(dsl_router)
  application.include_router(audit_router)
  application.include_router(execute_router)
  application.include_router(executions_router)

  @application.get("/health")
  def health() -> dict[str, str]:
    """进程存活探针（非 OpenAPI 正式域）。

    功能：返回服务存活状态 JSON。
    业务含义：K8s/CI 健康检查；W1 不含租户鉴权。
    上游调用方：负载均衡、gate workflow 测试
    下游被调方：无
    返回：{"status": "ok"}
    """
    return {"status": "ok"}

  return application


# Uvicorn 默认入口：uv run uvicorn apps.api.main:app --reload
app = create_app()
