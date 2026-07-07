# os_core 模块（见名知意）

代码根：`src/server/os_core/` · import 前缀 `os_core.<module>` · **13 模块**（Gate 0 · W8）

| 模块 | 职责 | 禁止 |
|------|------|------|
| `shared_contracts` | Pydantic · Schema · 错误码 · trace_context | 业务逻辑 |
| `platform_registry` | Contract/Pack/Tenant DB 真源（ADR-008） | 写 Legacy |
| `graph_service` | Graph 版本 · freeze · checksum | 写 Legacy |
| `rule_engine` | 授权 · 默认 deny | 写 Legacy |
| `execution_service` | **唯一写 Legacy** · DSL · Revert · Evidence | 业务 UI |
| `audit_service` | append-only 审计 | 改历史 |
| `agent_orchestrator` | intent → DslPlan（S0 stub · 无 LLM） | 写 Legacy · 绕过 Rule |
| `connector_sdk` | httpx 读写 · Blueprint Runtime · mock_legacy | 业务规则 |
| `tenant_service` | shadow_mode · tenant settings 真源 | 写 Legacy |
| `license_service` | Pack 授权 · CONNECTOR 门禁 | 执行 DSL |
| `package_service` | Implementation Package export/import | 写 Legacy |
| `reconciliation_service` | 对账 Job · drift（S0 mock read-back） | 写 Legacy |
| `mcp_gateway` | MCP tools/list · call → DslPlan · SEP-414 audit | 直写 Legacy |

## 写路径（不可变）

```text
Agent/MCP → DslPlan → harness/confirm → rule → execution_service → connector_sdk → audit
```

## 应用层

| 路径 | 职责 |
|------|------|
| `src/server/api` | FastAPI · `modules/`（**无业务规则**） |
| `src/server/api/router/v1/registry.py` | HTTP 路由第一站 · ROUTER_PROVIDERS |
| `src/server/os_core/registry.py` | 内核第一站 · KERNEL_MODULES |
| `src/integration/registry.py` | GIP 挂载清单 |
| `src/integration` | Pack/tenant 镜像（**禁 import os_core 私有 API**） |
| `src/apps/web-admin` · `src/apps/h5-worker` | 前端壳 |

## 公开 API

integration 仅可调 OpenAPI `/v1/*` 与 `connector_sdk` 公开面；详见 `docs/文档/架构/os_core-public-api.md`。

## Gate 0 后 intentionally stub（P1 前）

| 模块 | S0 口径 |
|------|---------|
| `agent_orchestrator` | 正则 intent · plan 内存 store |
| `reconciliation_service` | mock_legacy read-back |
| `connector_sdk` | conn-mock Pack |
| `mcp_gateway` | 内部 GA · 无 OAuth 对外 |
