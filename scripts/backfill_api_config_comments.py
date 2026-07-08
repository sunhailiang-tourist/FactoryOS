#!/usr/bin/env python3
"""一次性回填 api 工程底座中文注释（CMNT-04 Step 5 · 零逻辑 diff）。

作用：补齐 config/application/router/main 与 os_core 残留注释债。
业务关联：plan 1a.5 · B3 终轮 · CMNT-05 全量 0 违规。
上游：check_python_comments.py 违规清单
下游：src/server/api/config · application · router · main

Usage:
  uv run python scripts/backfill_api_config_comments.py
"""
from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# 相对 src/server/ 的路径 → 文件头（含四标签）
HEADERS: dict[str, str] = {
  "api/main.py": (
    '"""Uvicorn 入口（api/main.py）。\n\n'
    "作用：导出 app/create_app 供 uvicorn 与测试加载。\n"
    "业务关联：Modular Monolith HTTP 进程入口。\n"
    "上游：uvicorn · pytest TestClient。\n"
    "下游：application/factory · router · config。\n"
    '"""'
  ),
  "api/application/factory.py": (
    '"""FastAPI 应用工厂。\n\n'
    "作用：create_app 构建 FastAPI 实例并触发 assemble。\n"
    "业务关联：api 进程唯一应用入口。\n"
    "上游：main.py · pytest fixtures。\n"
    "下游：application/assemble · config/lifespan。\n"
    '"""'
  ),
  "api/application/assemble.py": (
    '"""应用装配（config → router）。\n\n'
    "作用：按固定顺序注册横切 config 与业务 router。\n"
    "业务关联：FastAPI 启动装配真源。\n"
    "上游：factory.create_app。\n"
    "下游：config/registry · router/registry。\n"
    '"""'
  ),
  "api/config/registry.py": (
    '"""config 横切注册唯一入口。\n\n'
    "作用：settings · logs · status_code · middleware 统一注册。\n"
    "业务关联：register_config 须在 router 之前调用。\n"
    "上游：application/assemble。\n"
    "下游：config 各子包 · FastAPI exception_handler。\n"
    '"""'
  ),
  "api/config/settings/__init__.py": (
    '"""config/settings 包。\n\n'
    "作用：环境变量与 Settings 加载命名空间。\n"
    "业务关联：DATABASE_URL · 特性开关真源。\n"
    "上游：config/registry register_config。\n"
    "下游：dependencies/db · platform_registry。\n"
    '"""'
  ),
  "api/config/settings/loader.py": (
    '"""Settings 加载器。\n\n'
    "作用：init() 读取环境变量并缓存 Settings 单例。\n"
    "业务关联：启动时须最先执行的配置步骤。\n"
    "上游：config/registry · os.environ。\n"
    "下游：dependencies/db.get_db_session。\n"
    '"""'
  ),
  "api/config/lifespan/__init__.py": (
    '"""config/lifespan 包。\n\n'
    "作用：FastAPI lifespan 上下文管理命名空间。\n"
    "业务关联：启动 bootstrap · 关停清理。\n"
    "上游：application/factory lifespan 参数。\n"
    "下游：platform_registry.bootstrap · os_core.registry.init_kernel。\n"
    '"""'
  ),
  "api/config/lifespan/hooks.py": (
    '"""FastAPI lifespan hooks。\n\n'
    "作用：startup/shutdown 编排内核与 Registry 初始化。\n"
    "业务关联：进程生命周期与 DB 连接池。\n"
    "上游：factory.create_app lifespan。\n"
    "下游：platform_registry · os_core.registry.init_kernel。\n"
    '"""'
  ),
  "api/config/logs/__init__.py": (
    '"""config/logs 包。\n\n'
    "作用：结构化日志配置命名空间。\n"
    "业务关联：request_id · tenant_id MDC 注入。\n"
    "上游：config/registry。\n"
    "下游：logs/configure · logs/context。\n"
    '"""'
  ),
  "api/config/logs/configure.py": (
    '"""日志配置。\n\n'
    "作用：init() 配置 root logger 格式与级别。\n"
    "业务关联：全链路可观测性基础。\n"
    "上游：config/registry register_config。\n"
    "下游：logs/context · middleware traces。\n"
    '"""'
  ),
  "api/config/logs/context.py": (
    '"""日志上下文（MDC）。\n\n'
    "作用：bind/clear request 级日志字段。\n"
    "业务关联：trace_id · tenant_id 关联排障。\n"
    "上游：traces/auth/tenant middleware。\n"
    "下游：structlog/logging 输出。\n"
    '"""'
  ),
  "api/config/metrics/configure.py": (
    '"""Metrics 配置。\n\n'
    "作用：Prometheus 指标注册与 /metrics 路由（若启用）。\n"
    "业务关联：SRE 可观测性。\n"
    "上游：config/registry。\n"
    "下游：metrics/middleware。\n"
    '"""'
  ),
  "api/config/metrics/middleware.py": (
    '"""Metrics 中间件。\n\n'
    "作用：HTTP 请求计数与延迟 histogram。\n"
    "业务关联：全路由自动埋点。\n"
    "上游：middleware/registry MIDDLEWARE_STACK。\n"
    "下游：Prometheus client。\n"
    '"""'
  ),
  "api/config/traces/configure.py": (
    '"""Traces 配置。\n\n'
    "作用：OpenTelemetry / trace id 生成策略。\n"
    "业务关联：M-03 traceparent · SEP-414。\n"
    "上游：config/registry。\n"
    "下游：traces/middleware。\n"
    '"""'
  ),
  "api/config/traces/middleware.py": (
    '"""Traces 中间件。\n\n'
    "作用：注入 correlation_id/traceparent 到 request/response。\n"
    "业务关联：跨服务排障与 MCP 追踪。\n"
    "上游：middleware/registry。\n"
    "下游：logs/context · 响应头 trace-id。\n"
    '"""'
  ),
  "api/config/auth/dependencies.py": (
    '"""Auth FastAPI Depends。\n\n'
    "作用：get_current_actor 等依赖注入。\n"
    "业务关联：RBAC · Actor 上下文。\n"
    "上游：auth/middleware request.state。\n"
    "下游：modules/*/controllers Depends。\n"
    '"""'
  ),
  "api/config/auth/identity.py": (
    '"""身份解析（JWT/API Key stub）。\n\n'
    "作用：从 Authorization 解析 Actor 身份。\n"
    "业务关联：统一鉴权入口。\n"
    "上游：HTTP Authorization header。\n"
    "下游：auth/middleware · audit actor 字段。\n"
    '"""'
  ),
  "api/config/auth/middleware.py": (
    '"""Auth 中间件。\n\n'
    "作用：认证并注入 request.state.actor。\n"
    "业务关联：业务 API 鉴权链；探针路径可跳过。\n"
    "上游：middleware/registry · Authorization header。\n"
    "下游：auth/dependencies · modules controllers。\n"
    '"""'
  ),
  "api/config/tenant/middleware.py": (
    '"""租户 middleware（X-Tenant-Id）。\n\n'
    "作用：解析 X-Tenant-Id 注入 request.state 与 contextvar。\n"
    "业务关联：多租户上下文真源；缺省 default。\n"
    "上游：middleware/registry · HTTP 请求头。\n"
    "下游：tenant/dependencies · os_core tenant 上下文。\n"
    '"""'
  ),
  "api/config/tenant/dependencies.py": (
    '"""Tenant FastAPI Depends。\n\n'
    "作用：get_tenant_id 从 request.state 读取租户 ID。\n"
    "业务关联：controllers 与 os_core 共用 tenant 上下文。\n"
    "上游：tenant/middleware。\n"
    "下游：modules/*/controllers · quota checker。\n"
    '"""'
  ),
  "api/config/tenant/resolver.py": (
    '"""租户 ID 解析辅助。\n\n'
    "作用：从 Request 提取 tenant_id（与 middleware 对齐）。\n"
    "业务关联：非 Depends 场景复用。\n"
    "上游：tenant/middleware request.state。\n"
    "下游：quota · audit 过滤。\n"
    '"""'
  ),
  "api/config/quota/checker.py": (
    '"""配额检查器。\n\n'
    "作用：按 tenant 扣减/校验 API 配额。\n"
    "业务关联：多租户公平使用。\n"
    "上游：quota/middleware · tenant_id。\n"
    "下游：429 Too Many Requests。\n"
    '"""'
  ),
  "api/config/quota/middleware.py": (
    '"""Quota 中间件。\n\n'
    "作用：请求前检查租户配额，超限返回 429。\n"
    "业务关联：防止单 tenant 打满资源。\n"
    "上游：middleware/registry · quota/checker。\n"
    "下游：HTTP 429 · metrics 计数。\n"
    '"""'
  ),
  "api/config/dependencies/__init__.py": (
    '"""config/dependencies 包。\n\n'
    "作用：FastAPI Depends 注入集合（DB · Registry session）。\n"
    "业务关联：controllers 禁止自建 Session。\n"
    "上游：settings/loader · platform_registry。\n"
    "下游：modules/*/controllers Depends(get_db_session)。\n"
    '"""'
  ),
  "api/config/dependencies/db.py": (
    '"""PostgreSQL Session Depends。\n\n'
    "作用：get_db_session 提供请求级 SQLAlchemy Session。\n"
    "业务关联：ADR-002 写路径须经 os_core service。\n"
    "上游：settings DATABASE_URL · lifespan 连接池。\n"
    "下游：os_core/*/service · store。\n"
    '"""'
  ),
  "api/config/dependencies/registry_session.py": (
    '"""Platform Registry Session Depends。\n\n'
    "作用：只读 Registry 查询专用 session 注入。\n"
    "业务关联：ADR-008 契约平面读路径。\n"
    "上游：platform_registry.session。\n"
    "下游：registry controllers · connector_sdk。\n"
    '"""'
  ),
  "api/config/status_code/__init__.py": (
    '"""config/status_code 包。\n\n'
    "作用：PlatformError → HTTP 响应映射命名空间。\n"
    "业务关联：统一错误 JSON 契约。\n"
    "上游：config/registry exception_handler 注册。\n"
    "下游：status_code/handlers · mapping。\n"
    '"""'
  ),
  "api/config/status_code/mapping.py": (
    '"""ErrorCode → HTTP status 映射。\n\n'
    "作用：PlatformError.error_code 转 HTTP 状态码。\n"
    "业务关联：OpenAPI ProblemDetails 对齐。\n"
    "上游：shared_contracts.errors ErrorCode。\n"
    "下游：status_code/handlers。\n"
    '"""'
  ),
  "api/config/status_code/handlers.py": (
    '"""全局异常处理器。\n\n'
    "作用：PlatformError/HTTPException/ValidationError 统一 JSON 响应。\n"
    "业务关联：客户端可解析 error_code · message。\n"
    "上游：config/registry add_exception_handler。\n"
    "下游：HTTP JSON ProblemDetails。\n"
    '"""'
  ),
  "api/config/status_code/responses.py": (
    '"""错误响应体构建。\n\n'
    "作用：build_error_payload 组装标准错误 JSON。\n"
    "业务关联：OpenAPI ErrorResponse 契约。\n"
    "上游：status_code/handlers。\n"
    "下游：HTTP 响应 body。\n"
    '"""'
  ),
  "api/router/registry.py": (
    '"""HTTP 路由注册总入口。\n\n'
    "作用：register_routers 挂载 v1 与 catalog 路由。\n"
    "业务关联：业务域路由须在 config 之后注册。\n"
    "上游：application/assemble。\n"
    "下游：router/v1/registry · router/catalog。\n"
    '"""'
  ),
  "api/router/catalog.py": (
    '"""路由目录只读 API。\n\n'
    "作用：暴露已登记 HTTP 域清单供运维/文档生成。\n"
    "业务关联：check_router_registry 对齐真源。\n"
    "上游：router/v1/registry API_ROUTER_DOMAINS。\n"
    "下游：GET 路由元数据响应。\n"
    '"""'
  ),
  "api/router/v1/__init__.py": (
    '"""router/v1 包。\n\n'
    "作用：OpenAPI /v1/* 路由注册命名空间。\n"
    "业务关联：modules/*/routers 聚合挂载。\n"
    "上游：router/registry register_routers。\n"
    "下游：router/v1/registry · mount。\n"
    '"""'
  ),
  "api/router/v1/mount.py": (
    '"""v1 路由挂载辅助。\n\n'
    "作用：include_router 封装与前缀策略。\n"
    "业务关联：保持 v1 路径一致性。\n"
    "上游：router/v1/registry。\n"
    "下游：FastAPI app.include_router。\n"
    '"""'
  ),
  "os_core/__init__.py": (
    '"""FactoryOS 内核包根。\n\n'
    "作用：标记 os_core 为可安装 Python 包。\n"
    "业务关联：W1～W8 内核模块按 MODULE-MAP 落地。\n"
    "上游：pytest · import 边界检查。\n"
    "下游：os_core/*/service · shared_contracts。\n"
    '"""'
  ),
}

FUNC_DOC_PATCHES: dict[str, dict[str, str]] = {
  "api/application/assemble.py": {
    "assemble": (
      '  """装配 FastAPI：先 config 后 router。\n\n'
      "  功能：调用 register_config 与 register_routers。\n"
      "  业务含义：应用启动装配顺序锁死。\n"
      "  上游：factory.create_app。\n"
      "  下游：config/registry · router/registry。\n"
      '  """'
    ),
  },
  "api/application/factory.py": {
    "create_app": (
      '  """创建并装配 FastAPI 实例。\n\n'
      "  功能：构建 FastAPI 并调用 assemble。\n"
      "  业务含义：HTTP 进程唯一应用工厂。\n"
      "  上游：main.py · pytest。\n"
      "  下游：assemble · lifespan hooks。\n"
      '  """'
    ),
  },
  "api/config/registry.py": {
    "register_config": (
      '  """注册 settings · logs · status_code · middleware。\n\n'
      "  功能：横切能力统一挂载到 FastAPI app。\n"
      "  业务含义：config 子系统启动真源。\n"
      "  上游：assemble(app)。\n"
      "  下游：middleware/registry · exception handlers。\n"
      '  """'
    ),
  },
  "api/config/settings/loader.py": {
    "init": (
      '  """加载并缓存 Settings 单例。\n\n'
      "  功能：读取环境变量初始化配置。\n"
      "  业务含义：DATABASE_URL 等启动必需项。\n"
      "  上游：register_config 首步。\n"
      "  下游：dependencies/db。\n"
      '  """'
    ),
  },
  "api/config/lifespan/hooks.py": {
    "lifespan": (
      '  """FastAPI lifespan 上下文（startup/shutdown）。\n\n'
      "  功能：启动时 bootstrap Registry 与内核 hook。\n"
      "  业务含义：进程生命周期与连接池管理。\n"
      "  上游：factory.create_app lifespan 参数。\n"
      "  下游：platform_registry.bootstrap · init_kernel。\n"
      '  """'
    ),
  },
  "api/config/logs/configure.py": {
    "init": (
      '  """初始化 root logger 格式与级别。\n\n'
      "  功能：配置结构化日志输出。\n"
      "  业务含义：全服务统一日志契约。\n"
      "  上游：register_config。\n"
      "  下游：logs/context MDC。\n"
      '  """'
    ),
  },
  "api/config/middleware/registry.py": {
    "register": (
      '  """按 MIDDLEWARE_STACK 顺序注册中间件。\n\n'
      "  功能：遍历 MIDDLEWARE_STACK 调用 add_middleware。\n"
      "  业务含义：请求链 traces→auth→tenant→quota→metrics。\n"
      "  上游：register_config。\n"
      "  下游：各 config/*/middleware 类。\n"
      '  """'
    ),
  },
  "api/config/dependencies/db.py": {
    "get_db_session": (
      '  """请求级 SQLAlchemy Session Depends。\n\n'
      "  功能：yield Session 并在请求结束 commit/rollback。\n"
      "  业务含义：controllers 唯一 DB 注入入口。\n"
      "  上游：settings DATABASE_URL。\n"
      "  下游：os_core/*/service。\n"
      '  """'
    ),
  },
  "api/config/tenant/dependencies.py": {
    "get_tenant_id": (
      '  """从 request.state 读取 tenant_id。\n\n'
      "  功能：FastAPI Depends 注入当前租户 ID。\n"
      "  业务含义：与 TenantMiddleware 上下文一致。\n"
      "  上游：tenant/middleware。\n"
      "  返回：str tenant_id。\n"
      '  """'
    ),
  },
  "api/router/registry.py": {
    "register_routers": (
      '  """挂载 v1 业务路由与 catalog。\n\n'
      "  功能：调用 register_v1 与 catalog 路由。\n"
      "  业务含义：业务 HTTP 面注册入口。\n"
      "  上游：assemble(app)。\n"
      "  下游：router/v1/registry。\n"
      '  """'
    ),
  },
  "api/router/v1/registry.py": {
    "register_v1": (
      '  """按 API_ROUTER_DOMAINS 顺序挂载全部 v1 路由。\n\n'
      "  功能：遍历 ROUTER_PROVIDERS 调用 include_router。\n"
      "  业务含义：OpenAPI /v1/* 域登记真源。\n"
      "  上游：register_routers。\n"
      "  下游：modules/*/get_routers。\n"
      '  """'
    ),
  },
  "os_core/registry.py": {
    "kernel_module_names": (
      '  """已登记内核包名（harness / 文档生成）。\n\n'
      "  功能：返回 KERNEL_MODULES 包名元组。\n"
      "  业务含义：治理与 import 边界检查。\n"
      "  上游：KERNEL_MODULES 常量。\n"
      "  返回：tuple[str, ...] 包名列表。\n"
      '  """'
    ),
    "init_kernel": (
      '  """按注册表执行各模块 startup hook。\n\n'
      "  功能：遍历 KERNEL_MODULES 调用 init_hook。\n"
      "  业务含义：lifespan startup 内核初始化。\n"
      "  上游：config/lifespan hooks。\n"
      "  下游：platform_registry.bootstrap 等。\n"
      '  """'
    ),
  },
}

# middleware dispatch 须模块差异化叙事（避免 check_code_redundancy 撞 hash）
DISPATCH_DOCS: dict[str, str] = {
  "api/config/metrics/middleware.py": (
    '    """Metrics 请求链埋点（S0 stub · 透传）。\n\n'
    "    功能：包裹 call_next 并预留请求计数/延迟 histogram 钩子。\n"
    "    业务含义：Prometheus 全路由自动 instrumentation 入口。\n"
    "    上游：MetricsMiddleware · MIDDLEWARE_STACK 最外层。\n"
    "    下游：call_next · quota/tenant/auth/traces 内层。\n"
    '    """'
  ),
  "api/config/traces/middleware.py": (
    '    """Traces 请求链关联（S0 stub · 透传）。\n\n'
    "    功能：包裹 call_next 并预留 trace-id/traceparent 注入与回传。\n"
    "    业务含义：M-03 SEP-414 分布式追踪中间件入口。\n"
    "    上游：TracesMiddleware · Authorization 内侧。\n"
    "    下游：call_next · logs/context MDC · 响应头 trace-id。\n"
    '    """'
  ),
  "api/config/quota/middleware.py": (
    '    """Quota 租户配额检查（S0 stub · 透传）。\n\n'
    "    功能：包裹 call_next 并预留 quota/checker 扣减与 429 拦截。\n"
    "    业务含义：多租户公平使用 · 防单 tenant 打满资源。\n"
    "    上游：QuotaMiddleware · tenant_id 已注入后。\n"
    "    下游：call_next · 超限 HTTP 429 · metrics 计数。\n"
    '    """'
  ),
}

HANDLER_DOCS = {
  "platform_error_handler": (
    '  """PlatformError → JSON ProblemDetails。\n\n'
    "  功能：映射 error_code 到 HTTP status 并序列化。\n"
    "  业务含义：os_core 业务异常统一 HTTP 出口。\n"
    "  上游：os_core PlatformError raise。\n"
    "  下游：JSONResponse · build_error_payload。\n"
    '  """'
  ),
  "http_exception_handler": (
    '  """HTTPException → JSON 响应。\n\n'
    "  功能：包装 Starlette HTTPException 为标准 JSON。\n"
    "  业务含义：FastAPI 内置异常对齐契约。\n"
    "  上游：FastAPI route raise HTTPException。\n"
    "  下游：JSONResponse。\n"
    '  """'
  ),
  "validation_exception_handler": (
    '  """RequestValidationError → 422 JSON。\n\n'
    "  功能：Pydantic 校验失败转 ProblemDetails。\n"
    "  业务含义：OpenAPI 请求体验证错误统一格式。\n"
    "  上游：FastAPI/Pydantic 校验。\n"
    "  下游：422 JSONResponse。\n"
    '  """'
  ),
  "unhandled_exception_handler": (
    '  """未捕获异常 → 500 JSON。\n\n'
    "  功能：兜底异常处理并记录日志。\n"
    "  业务含义：防止堆栈泄露；返回通用 500。\n"
    "  上游：未预期 Exception。\n"
    "  下游：500 JSONResponse · logs。\n"
    '  """'
  ),
  "build_error_payload": (
    '  """组装标准错误 JSON 载荷。\n\n'
    "  功能：合并 error_code · message · details。\n"
    "  业务含义：OpenAPI ErrorResponse 契约真源。\n"
    "  上游：status_code/handlers。\n"
    "  返回：dict 可 JSON 序列化。\n"
    '  """'
  ),
}


def _replace_module_doc(text: str, new_doc: str) -> str:
  pattern = re.compile(r'^("""|\'\'\')(.*?)\1', re.DOTALL | re.MULTILINE)
  m = pattern.search(text)
  if m:
    return text[: m.start()] + new_doc + text[m.end() :]
  lines = text.splitlines(keepends=True)
  insert_at = 0
  for i, ln in enumerate(lines):
    if ln.startswith("from __future__"):
      insert_at = i + 1
      break
  return "".join(lines[:insert_at]) + new_doc + "\n" + "".join(lines[insert_at:])


def _patch_func_by_name(text: str, func_name: str, new_doc: str) -> str:
  pat = rf"(def {re.escape(func_name)}\([^)]*\)[^:]*:)\n"
  if re.search(rf"{pat}\s+\"\"\"", text):
    text = re.sub(rf"(def {re.escape(func_name)}\([^)]*\)[^:]*:\n)\s+\"\"\".*?\"\"\"", rf"\1{new_doc}", text, count=1, flags=re.DOTALL)
  else:
    text = re.sub(pat, rf"\1\n{new_doc}\n", text, count=1)
  return text


def _patch_dispatch(text: str, rel: str) -> str:
  doc = DISPATCH_DOCS.get(rel)
  if not doc or 'async def dispatch' not in text:
    return text
  if re.search(r"async def dispatch\([^)]*\)[^:]*:\n\s+\"\"\"", text):
    return text
  return re.sub(
    r"(async def dispatch\([^)]*\)[^:]*:)\n(\s+)",
    rf"\1\n{doc}\n\2",
    text,
    count=1,
  )


def patch_file(path: Path) -> bool:
  rel = str(path.relative_to(ROOT / "src" / "server")).replace("\\", "/")
  text = path.read_text(encoding="utf-8")
  original = text

  if rel in HEADERS:
    text = _replace_module_doc(text, HEADERS[rel])

  if rel in FUNC_DOC_PATCHES:
    for fname, doc in FUNC_DOC_PATCHES[rel].items():
      text = _patch_func_by_name(text, fname, doc)

  if rel == "api/config/status_code/handlers.py":
    for fname, doc in HANDLER_DOCS.items():
      if fname != "build_error_payload":
        text = _patch_func_by_name(text, fname, doc)

  if rel == "api/config/status_code/responses.py":
    text = _patch_func_by_name(text, "build_error_payload", HANDLER_DOCS["build_error_payload"])

  text = _patch_dispatch(text, rel)

  if text != original:
    path.write_text(text, encoding="utf-8")
    return True
  return False


def main() -> int:
  p = argparse.ArgumentParser()
  p.add_argument("--dry-run", action="store_true")
  args = p.parse_args()

  targets: list[Path] = []
  for rel in HEADERS:
    targets.append(ROOT / "src" / "server" / rel)
  for rel in FUNC_DOC_PATCHES:
    pth = ROOT / "src" / "server" / rel
    if pth not in targets:
      targets.append(pth)
  for extra in (
    "api/config/status_code/handlers.py",
    "api/config/status_code/responses.py",
    "api/config/dependencies/db.py",
    "api/config/tenant/dependencies.py",
    "api/config/tenant/middleware.py",
    "api/config/auth/middleware.py",
    "api/config/metrics/middleware.py",
    "api/config/quota/middleware.py",
    "api/config/traces/middleware.py",
  ):
    pth = ROOT / "src" / "server" / extra
    if pth not in targets:
      targets.append(pth)

  changed = 0
  for path in sorted(set(targets)):
    if not path.is_file():
      continue
    if args.dry_run:
      print("would patch:", path.relative_to(ROOT))
    elif patch_file(path):
      changed += 1
      print("patched:", path.relative_to(ROOT))

  print(f"\n{'Would patch' if args.dry_run else 'Patched'} {len(targets)} target(s), {changed} changed")
  return 0


if __name__ == "__main__":
  sys.exit(main())
