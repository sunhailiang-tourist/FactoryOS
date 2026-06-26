# os_core 模块（见名知意）

代码根：`src/server/os_core/` · import 前缀 `os_core.<module>`

| 模块 | 职责 | 禁止 |
|------|------|------|
| `shared_contracts` | Pydantic · Schema · 错误码 | 业务逻辑 |
| `platform_registry` | Contract/Pack/Tenant DB 真源（ADR-008） | 写 Legacy |
| `graph_service` | Graph 版本 · freeze · checksum | 写 Legacy |
| `rule_engine` | 授权 · 默认 deny | 写 Legacy |
| `execution_service` | **唯一写 Legacy** · DSL · Revert | 业务 UI |
| `audit_service` | append-only 审计 | 改历史 |
| `agent_orchestrator` | LangGraph → DslPlan | 写 Legacy · 绕过 Rule |
| `connector_sdk` | httpx 读写 · Blueprint Runtime | 业务规则 |
| `license_service` | Pack 授权 | 执行 DSL |
| `mcp_gateway` | MCP → DslPlan | 直写 Legacy |

## 应用层

| 路径 | 职责 |
|------|------|
| `src/server/api` | FastAPI · `application/` · `router/` · `config/` · `modules/`（**无业务规则**） |
| `src/server/api/router/v1/registry.py` | HTTP 路由第一站 · ROUTER_PROVIDERS |
| `src/server/os_core/registry.py` | 内核模块第一站 · KERNEL_MODULES |
| `src/integration/registry.py` | GIP 挂载清单 |
| `src/integration` | export/fixture 镜像（**禁 import os_core 私有 API**） |
| `src/apps/web-admin` · `src/apps/h5-worker` | 前端壳 |

## 公开 API

integration 仅可调 OpenAPI `/v1/*` 与 `connector_sdk` 公开面；详见 `docs/文档/架构/os_core-public-api.md`。
