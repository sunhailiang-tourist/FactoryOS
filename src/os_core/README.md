# os_core · 平台内核

## 是什么

FactoryOS **L0/L1/L2 引擎域**：Graph、Rule、Execution、Audit、Agent、Connector、License、MCP。单仓 monorepo 内核根，**禁止** 承载具体工厂业务 Graph。

## 主要功能

- 9 个 Python 包（见子目录 README）：契约、图、规则、执行、审计、编排、连接器 SDK、授权、MCP
- 唯一 **写 Legacy** 路径：`execution_service`
- Core v1.0 冻结后变更须 ADR + 全量 AC

## 不负责什么

- HTTP 路由与 UI（`apps/`）
- 租户 Pack / Blueprint / SystemRelation（`integration/`）
- 具体 MES/ERP 厂商逻辑（`src/integration/packs` · `docs/文档/连接器/`）

## 上下游

- **上游**：`apps/api` 依赖注入调用各模块 public API
- **下游**：PostgreSQL、Redis、Legacy 经 `connector_sdk`、LiteLLM（仅 agent）

## 关键文件

| 路径 | 作用 |
|------|------|
| `shared_contracts/` | Pydantic / Schema 真源 |
| `execution_service/` | DSL 执行与写门禁 |
| 各 `*/README.md` | 子模块说明 |

## 相关文档

- [命名约定](../../docs/文档/架构/命名约定.md) · 契约 [contracts/](../../contracts/)
- [SH-步步流](../../.cursor/factoryos/SH-步步流.md) · [PRE-DEV-CHAIN](../../.cursor/factoryos/PRE-DEV-CHAIN.md)

## 本地开发

`uv sync --extra dev` 后 `uv run pytest src/tests/ -v`（pending AC 预期红）。
