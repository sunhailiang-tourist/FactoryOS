# os_core · 平台内核

## 是什么

FactoryOS **L0/L1/L2 引擎域**：Graph、Rule、Execution、Audit、Agent、Connector、Tenant、Package、Reconcile、License、MCP、Registry。单仓 monorepo 内核根，**禁止** 承载具体工厂业务 Graph。

## 主要功能

- **13** 个 Python 包（见 `registry.py` · 各子目录 README）
- 唯一 **写 Legacy** 路径：`execution_service` → `connector_sdk.runtime`
- **Gate 0**（W1～W8）：AC-BASE-001 P0 + M-03 全绿 · tag `core-v1.0.0`
- Core 冻结后变更须 ADR + 全量 AC 回归

## 模块一览

| # | 模块 | 一句话 |
|---|------|--------|
| 1 | `shared_contracts` | 契约 DTO · CMV · trace_context |
| 2 | `platform_registry` | ADR-008 配置/契约 DB 真源 |
| 3 | `graph_service` | Graph freeze · checksum |
| 4 | `rule_engine` | 默认 deny · evaluate |
| 5 | `execution_service` | **唯一写 Legacy** · revert · evidence |
| 6 | `audit_service` | append-only 审计 |
| 7 | `agent_orchestrator` | intent → DslPlan（S0 无 LLM） |
| 8 | `connector_sdk` | mock/Blueprint Runtime |
| 9 | `tenant_service` | shadow_mode 真源 |
| 10 | `license_service` | Pack 授权 |
| 11 | `package_service` | Implementation Package 快照 |
| 12 | `reconciliation_service` | 对账 Job（S0 mock read-back） |
| 13 | `mcp_gateway` | MCP tools/list · call → DslPlan + audit |

## 不负责什么

- HTTP 路由与 UI（`server/api` · `apps/`）
- 租户 Pack 业务定义（`integration/packs` · `integration/tenants`）
- 具体 MES/ERP 厂商协议（Connector Pack · `docs/文档/连接器/`）

## 上下游

- **上游**：`server/api` 薄路由 · 依赖注入调用各模块 public API
- **下游**：PostgreSQL · Legacy 经 `connector_sdk` · LiteLLM（P1+ agent）

## 关键文件

| 路径 | 作用 |
|------|------|
| `registry.py` | **内核第一站** · KERNEL_MODULES（13） |
| `shared_contracts/` | Pydantic / Schema（Contract Registry · ADR-008） |
| `execution_service/` | 写路径编排 |
| 各 `*/README.md` | 子模块说明 |

## 相关文档

- [MODULE-MAP](../../../.cursor/factoryos/MODULE-MAP.md) · [PATH-SNAPSHOT](../../../.cursor/factoryos/PATH-SNAPSHOT.md)
- [命名约定](../../docs/文档/架构/命名约定.md) · [contracts/](../../contracts/)
- [SH-步步流](../../../.cursor/factoryos/SH-步步流.md)

## 本地开发

```bash
uv sync --extra dev
uv run pytest src/tests/ -q          # Gate 0：116 passed · pending 0
python scripts/check_import_boundaries.py
```
