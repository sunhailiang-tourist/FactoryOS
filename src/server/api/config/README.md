# config · 服务端配置与横切能力

> **定位**：deployable 侧 **配置平面**（settings · 日志 · 状态码 · 鉴权 · 租户 · 配额 · 中间件）  
> **不叫 core**：与 `os_core/` 领域内核严格区分

## 是什么

`config/` 承载 HTTP 服务运行时横切能力；**不含路由、不含业务规则**。  
统一入口：`registry.py` → `register_config(app)`。

## 子模块一览

| 目录 | 核心功能 | S0 行为 | 承载业务 |
|------|----------|---------|----------|
| `settings/` | pydantic-settings · env · profile | 读 `FACTORYOS_ENV` | 环境隔离 |
| `logs/` | structlog 初始化 · request 上下文 | no-op 占位 | 可观测 · 排障 |
| `status_code/` | PlatformError → HTTP JSON | 已生效 | 统一错误面 |
| `lifespan/` | startup/shutdown · `init_kernel()` | 调 os_core registry | 内核 bootstrap |
| `auth/` | JWT/API Key 身份（middleware） | pass-through | 谁在用 API |
| `tenant/` | `X-Tenant-Id` → contextvars | 默认 `default` | 多厂隔离 MT-01 |
| `quota/` | `tenant_quotas` 限流 | pass-through | 百级租户 S1 |
| `traces/` | OpenTelemetry | pass-through | 链路追踪 |
| `metrics/` | Prometheus 指标 | pass-through | SLA 监控 |
| `middleware/` | **中间件注册顺序唯一真源** | 见下 | 请求链治理 |
| `dependencies/` | FastAPI Depends（DB Session 等） | 已生效 | 请求级资源 |

## Middleware 顺序（`middleware/registry.py`）

```text
traces → auth → tenant → quota → metrics
（Starlette 后注册先执行；最外层 traces）
```

## 怎么用

**Controller 取 DB：**

```python
from server.api.config.dependencies.db import get_db_session
```

**Controller 取 tenant（S0）：**

```python
from server.api.config.tenant.dependencies import get_tenant_id
```

**扩展横切能力：**

1. 在对应子目录加实现  
2. 在 `config/registry.py` 或 `middleware/registry.py` 登记  
3. 补 workflow/harness 测试

## 上下游

- **上游**：`application/assemble.py` 最先调 `register_config`  
- **下游**：`os_core/`（via dependencies · lifespan · status_code handlers）  
- **规格**：[多租户与隔离](../../../docs/文档/规格说明/多租户与隔离.md) · ADR-007

## 门禁

```bash
uv run pytest src/tests/workflow/test_api_health.py -q
./scripts/harness --tier full
```

## 关联文档

- [ADR-007 百级千级演进策略](../../../docs/文档/架构/架构决策记录-007-百级千级演进策略.md)  
- [application/README.md](../application/README.md)
