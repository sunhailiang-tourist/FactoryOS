# PATH-SNAPSHOT · 项目结构快照

> **AUTO-GENERATED — 勿手改**
> 真源：`contracts/repo-structure.yaml` · 生成：`uv run python scripts/gen_path_snapshot.py`
> version: 1 · updated: 2026-06-29 · decision_ref: D14

## import 前缀

| 层 | import | 物理根 |
|----|--------|--------|
| HTTP API | `server.api` | `src/server/api/` |
| 内核 | `os_core.*` | `src/server/os_core/` |

## 现行路径（canonical）

- `src/server/api/`
- `src/server/os_core/`
- `src/server/db/migrations/`
- `src/server/db/migrations/versions/`
- `src/server/edge-agent/`
- `src/integration/`
- `src/tests/`
- `src/apps/web-admin/`
- `src/apps/h5-worker/`
- `alembic.ini`

## 废止路径（禁止作为操作路径）

### 目录不得存在

- `src/apps/api/`
- `src/os_core/`
- `src/db/`
- `src/apps/edge-agent/`
- `src/server/api/routes/`
- `alembic/`

### 文件不得存在

- `src/server/api/deps.py`
- `src/server/api/error_handlers.py`

### 文本不得误导引用

- `src/apps/api`
- `src/os_core`
- `src/db`
- `src/apps/edge-agent`
- `apps.api`
- `src/server/api/routes`
- `src/server/api/deps.py`
- `src/server/api/error_handlers.py`
- `alembic/versions`
- `alembic/README`
- regex: `(?<![./])alembic/(?!ini)`

## 内核模块（13）

1. `shared_contracts` → `src/server/os_core/shared_contracts/`
2. `graph_service` → `src/server/os_core/graph_service/`
3. `rule_engine` → `src/server/os_core/rule_engine/`
4. `execution_service` → `src/server/os_core/execution_service/`
5. `audit_service` → `src/server/os_core/audit_service/`
6. `agent_orchestrator` → `src/server/os_core/agent_orchestrator/`
7. `connector_sdk` → `src/server/os_core/connector_sdk/`
8. `tenant_service` → `src/server/os_core/tenant_service/`
9. `license_service` → `src/server/os_core/license_service/`
10. `package_service` → `src/server/os_core/package_service/`
11. `reconciliation_service` → `src/server/os_core/reconciliation_service/`
12. `mcp_gateway` → `src/server/os_core/mcp_gateway/`
13. `platform_registry` → `src/server/os_core/platform_registry/`

## 结构变更纪律

1. 先改 `contracts/repo-structure.yaml`
2. 跑 `uv run python scripts/gen_path_snapshot.py`
3. 更新 `18-一致性矩阵` D 行 · `命名约定.md`
4. `./scripts/gate pr` 全绿
5. **git commit** 时 pre-commit 自动跑 `check_structure_change.py`（漂移则拦截并打印步骤）
