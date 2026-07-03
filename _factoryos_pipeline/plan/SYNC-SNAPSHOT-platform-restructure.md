# 平台化整改 · 同步修改快照（确认方案后一次性执行）

> **用途**：用户确认 `plan-platform-restructure-db-first.md` 后，按本清单 **无遗漏** 同步修改。  
> **禁止**：确认前执行任何代码/目录变更。

---

## A. 目录 / 物理搬迁

| 现路径 | 目标路径 | 连带修改 |
|--------|----------|----------|
| `src/server/os_core/` | `server/core/` 或 `server/os_core/` | pyproject packages · imports 保持 `os_core.*` 或统一重命名 |
| `src/server/api/` | `server/api/` | `server.api` → `server.api` 全局 |
| `src/server/edge-agent/` | `server/edge-agent/` | README |
| `src/apps/web-admin/` | `apps/web-admin/` | 仅移动 |
| `src/apps/h5-worker/` | `apps/h5-worker/` | 仅移动 |
| `alembic/`（已移除） | `src/server/db/` | `alembic.ini` script_location |
| `src/integration/` | **删除编辑真源** | fixture → `tests/fixtures/integration/` |
| `contracts/` | **废止编辑** | 可选 `artifacts/contracts-export/` CI 生成 |
| `src/tests/` | `tests/` 或保留 | conftest paths |

---

## B. 源码 — 必须改（Tier 1）

### B.1 文件加载 → DB

- `src/server/os_core/shared_contracts/cmv_registry.py`
- `src/server/os_core/shared_contracts/schema_loader.py`
- `src/server/os_core/connector_sdk/registry.py`

### B.2 API / 部署

- `src/server/api/main.py`
- `src/server/api/config/dependencies/db.py`（alembic.ini 路径）
- `src/server/api/modules/*/controllers/*.py`（package rename）
- `src/server/api/config/status_code/handlers.py`

### B.3 测试

- `src/tests/conftest.py`
- `src/tests/workflow/test_api_health.py`
- `src/tests/integration/test_connector_c01.py`
- `src/tests/integration/test_graph_w3.py`
- `src/tests/integration/test_connector_blueprint_w4.py`
- `src/tests/integration/test_connector_runtime_w4.py`
- `src/tests/integration/test_scale_s01_s04.py`
- `src/tests/contract/test_openapi_contract.py`
- `src/tests/contract/test_shared_contracts.py`
- `src/tests/ac_registry.py`

### B.4 新增（尚无）

- `server/core/platform_registry/contract_store.py`
- `server/core/platform_registry/pack_store.py`
- `server/core/platform_registry/tenant_config_store.py`
- `server/core/platform_registry/snapshot_store.py`
- `server/db/migrations/004_platform_registry.py`
- `server/db/seeds/bootstrap_contract_set.sql` 或 data migration

---

## C. scripts/ — 必须改

- `scripts/check_openapi_schema_refs.py`
- `scripts/check_cmv_sync.py`
- `scripts/check_plan_spec.py`
- `scripts/docs_baseline.py`（Tier-C policy）
- `scripts/check_import_boundaries.py`
- `scripts/check_harness.py`
- `scripts/check_code_redundancy.py`
- `scripts/check_static_quality.py`
- `scripts/check_deptry.py`
- `scripts/check_pr_diff.py`
- `scripts/gate_cli.py`（pytest roots）
- `scripts/factoryos_cli.py`（flows.json 路径）
- `scripts/pytest_contract_workflow.sh`
- `scripts/README.md`

---

## D. .cursor/ — 必须改

### D.1 factoryos/

- `INDEX.md`
- `PRE-DEV-CHAIN.md`
- `UI-FIRST-CONFIG-PRINCIPLE.md`
- `INTEGRATION-CHAIN.md`
- `MODULE-MAP.md`
- `STEP0.md`
- `DEV-GATES.md`
- `TEST-GATES.md`
- `HARNESS-SCRIPTS.md`
- `ORM-MIGRATION-PRINCIPLE.md`
- `README.md`
- `templates/*`（8 个模板）

### D.2 rules/

- `SH-步步流.mdc`
- `编码绝对门禁.mdc`
- `项目结构变更门禁.mdc`
- `factoryos-dev-workflow.mdc`
- `factoryos-test-workflow.mdc`
- `工厂操作系统.md`

### D.3 hooks & baseline

- `hooks/protect-paths.py`
- `hooks/post-edit-harness-hint.py`
- `docs-baseline/BASELINE.md`
- `docs-baseline/policy/WORKFLOW_MAP.json`
- `docs-baseline/manifest/MANIFEST.json`（refresh）

### D.4 根

- `.cursor/README.md`

---

## E. docs/ — 必须改（P0–P2）

### P0

- `docs/文档/架构/配置枢纽与关系模型.md`
- `docs/文档/架构/FactoryOS完整架构设计.md`
- `docs/文档/数据结构/SystemRelation.schema.json`
- **新建** `docs/文档/架构/架构决策记录-008-配置与契约平面DB化.md`

### P1

- `docs/文档/规格说明/Integration-Studio规格.md`
- `docs/文档/规格说明/factoryos-guide规格.md`
- `docs/文档/规格说明/人工决策Playbook.md`
- `docs/文档/规格说明/Connector-Blueprint规格.md`
- `docs/文档/数据结构/CMV同步规则.md`
- `docs/文档/规格说明/模块包.md`
- `docs/README.md`
- `docs/文档/索引.md`

### P2

- `docs/文档/架构/命名约定.md`
- `docs/文档/架构/架构闭合清单.md`
- `docs/文档/架构/ADR-004` · `ADR-007` 修订节
- `docs/准备/2026-06-16/03-锁定实施策略.md`
- `docs/准备/2026-06-16/16-OS核心基座架构设计方案.md`
- `docs/准备/2026-06-16/17-集成平台化战略(GIP).md`
- `docs/准备/2026-06-16/18-基座文档一致性矩阵.md`
- `docs/文档/验收/验收用例-BASE-001-平台底座.md`
- `docs/文档/接口/工厂操作系统-v1.1.yaml`（新 Registry API）
- 架构 SVG/PNG 生成脚本产出（5 图）

### 废止双轨说明

- `docs/文档/数据结构/*.schema.json` → 描述改为「Registry artifact 格式」非 Git 真源
- `docs/文档/接口/工厂操作系统-v1.1.yaml` → 与 `contracts/openapi` 合并策略或 export-only

---

## F. 根目录 & 工程配置

- `pyproject.toml`（packages · pythonpath · ruff · pyright）
- `alembic.ini`
- `README.md`（若存在）
- `.github/workflows/*`（若有 CI path）
- `contracts/README.md` → deprecated 指向 ADR-008

---

## G. integration 数据文件处置

| 文件 | 处置 |
|------|------|
| `src/integration/catalog/conn-mock.yaml` | seed → `pack_registry`；保留 copy 于 `tests/fixtures/` |
| `src/integration/tenants/hasen/**` | seed SQL 或 export 样例；移 `tests/fixtures/tenants/` |
| `src/integration/tools/guide/flows.json` | 迁 `server/api/` 或 DB `studio_flows` 表 |
| `src/integration/packs/.gitkeep` | 删除或改 fixtures |

---

## H. contracts 数据文件处置

| 路径 | 处置 |
|------|------|
| `contracts/openapi/` | bootstrap import → `contract_artifacts`；CI export 镜像 |
| `contracts/schemas/` | 同上 |
| `contracts/cmv/` | 同上 |
| `contracts/acceptance/` | 迁 DB 或保留 AC 文本供 gate 至 P4 |
| `contracts/fixtures/` | → `tests/fixtures/` |

---

## I. _factoryos_pipeline 模板更新

- `workflow_state.md`（W5 goal 指向 platform restructure）
- 新 plan/test-plan 引用 ADR-008 AC ID
- step-stop / verify 模板中 contracts/integration 路径描述

---

## J. 验收命令（整改后必须全绿）

```bash
uv run alembic upgrade head
uv run pytest src/tests/ -m 'not pending' -q
./scripts/harness --tier full
./scripts/gate plan
./scripts/gate pr
```

---

## K. 当前代码与文档冲突点（整改动机快照）

1. `integration/README.md` 说 PG 真源 · `registry.py` 仍读 catalog YAML  
2. `UI-FIRST` 说 DB 真源 · `配置枢纽` 说 Git 草案真源  
3. `connector_instances` 表已建 · Python 零读写  
4. `contracts/` L0 gate · 无 Contract Registry 表  
5. `server/api` 与 `os_core` 平级 · 无 `server/` 语义  

---

**确认口令**：用户回复「确认规划」+ 可选「确认编码门禁，开始 W5」后，按本快照 **单次 PR 系列** 执行（建议 P1→P3 分 PR）。
