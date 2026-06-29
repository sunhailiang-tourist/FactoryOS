# 终轮全量回归 · Test 兜底验收报告

- **对照 plan**：`_factoryos_pipeline/2026-06-25/plan/plan-0116-w1-base.md`（Step 1～4 全量）
- **命名**：`test-1657-final-regression.md`（HHmm=1657 落盘当下本地时间）
- **口令**：`【Test·终轮回归】`（2026-06-25 · W1 交付前）

## 1. 本轮 git diff 全量改动面

对照 plan §5 模块与文件；实现已合入工作区（含已 commit + 未提交治理文档）。

| 路径 | 变更 | plan Step | 落位合理 | 备注 |
|------|------|-----------|----------|------|
| `pyproject.toml` · `uv.lock` | 修改 | 1 | ✅ | FastAPI · SQLAlchemy · Alembic · asyncpg |
| `src/server/api/main.py` | 新增 | 1 | ✅ | app 工厂 + `/health` |
| `src/server/api/modules/*/controllers/connectors.py` | 新增 | 4 | ✅ | 薄路由，无业务规则 |
| `src/server/os_core/shared_contracts/` | 新增 | 2–3 | ✅ | Pydantic · TenantRegistry · OutboxPort |
| `src/server/db/migrations/` · `alembic.ini` | 新增 | 3 | ✅ | `001_scale_s01_s04` |
| `src/server/os_core/connector_sdk/health.py` | 新增 | 4 | ✅ | mock C-01，无 write |
| `src/integration/catalog/conn-mock.yaml` | 新增 | 4 | ✅ | mock Pack 占位 |
| `src/tests/workflow/` · `contract/` · `integration/` | 新增/改 | Test | ✅ | W1 AC 子集 |
| `.cursor/rules/项目结构变更门禁.mdc` | 新增 | 治理 | ✅ | 新建目录须 README |

**未触及（符合 plan）**：`graph_service` · `rule_engine` · `execution_service` · `agent_orchestrator` 业务实现。

## 2. 新增功能正确性（本轮 AC 全量）

| AC ID | Step | 业务验收 | pytest 证据 | 结果 |
|-------|------|----------|-------------|------|
| workflow | 1 | import_boundaries 绿 + `/health` 200 | `test_import_boundaries_script_passes` · `test_health_endpoint_returns_200` | **PASS** |
| contract | 2 | 7 Schema required 字段对齐 | `test_shared_contract_model_required_fields_match_schema[contract-*]` ×7 | **PASS** |
| S-01 | 3 | upgrade head 后四表 + tenants 列 | `test_S01_scale_tables_after_migration[S-01]` | **PASS** |
| S-02 | 3 | 默认 tenant seed | `test_S02_default_tenant_seed_values[S-02]` | **PASS** |
| S-03 | 3 | TenantRegistry.get_cell | `test_S03_tenant_registry_get_cell[S-03]` | **PASS** |
| S-04 | 3 | OutboxPort 持久化 | `test_S04_outbox_port_persists_event[S-04]` | **PASS** |
| C-01 | 4 | connector health mock | `test_C01_connector_health_returns_ok[C-01]` | **PASS** |

**52 P0 其余**：51 项 `@pytest.mark.pending` 仍红（plan 预期，W8 Gate 0）。

## 3. 存量功能回归（不影响原功能）

| 域 | 回归范围 | 命令 | 结果 |
|----|----------|------|------|
| workflow | 红线/门禁/健康检查 | `uv run pytest src/tests/workflow/ -m 'not pending'` | **4 passed** |
| contract | OpenAPI/Schema/CMV | `uv run pytest src/tests/contract/ -m 'not pending'` | **11 passed** |
| integration | W1 S-* / C-01 | `uv run pytest src/tests/integration/ -m 'not pending'` | **5 passed** |
| harness full | L0–L2 静态四门 | `uv run python scripts/gate_cli.py pr` | **绿** |
| 全量 W1 | contract+workflow+integration | `uv run pytest … -m 'not pending'` | **19 passed** |

```bash
uv run python scripts/gate_cli.py delivery   # 终轮验收盘（本报告落盘后）
```

## 4. 代码落位与优雅性（终轮）

| 维度 | 结论 | 说明 |
|------|------|------|
| 模块边界 | **通过** | `server/api` 薄路由；业务在 `os_core`；integration 无 os_core 私有 import |
| 重复逻辑 | **通过** | health 逻辑单点在 `connector_sdk.health`；路由仅 model_dump |
| 注释可读性 | **通过** | 文件头 + 函数 docstring 四要素齐全 |
| 与 plan 一致 | **通过** | 无 G/R/E 业务闭环；无超 scope Legacy 写 |

**需改进（非阻断）**：
1. `StarletteDeprecationWarning`：httpx ASGITransport → 建议 W2 统一 `TestClient` 或升级 httpx2。
2. 单步 `gate step` 现依赖 `test-*-stepN-regression.md` 落盘；本轮回补终轮报告，单步报告可后续补档。

## 5. 接口分区（终轮交付）

### 📦 本次新增接口

#### `GET /health`（Step1 · 非 OpenAPI 正式域）

入参：无

出参：

```json
{
  "status": "ok"
}
```

结构依据：server/api/main.py 内联返回；workflow 测试断言。

#### `GET /v1/connectors/{packId}/health`（Step4 · C-01）

入参（query）：

```json
{
  "tenant_id": "default"
}
```

路径参数：`pack_id` = `conn-mock`

出参：

```json
{
  "status": "ok",
  "pack_id": "conn-mock",
  "latency_ms": 0
}
```

结构依据：`contracts/openapi/工厂操作系统-v1.1.yaml` `/v1/connectors/{packId}/health` · `ConnectorHealthResponse`

### 🔁 本次需求涉及到的接口（字段调整）

**无字段调整**。

依据：W1 仅新增上述两路由；未修改既有 OpenAPI `/v1/*` 响应组装；`shared_contracts` 为新建 Pydantic，非存量 API 字段变更。

## 6. 文件 ↔ 接口对账表

| 文件 | 接口/AC | 说明 |
|------|---------|------|
| `src/server/api/main.py` | `GET /health` | workflow |
| `src/server/api/modules/*/controllers/connectors.py` | `GET /v1/connectors/{packId}/health` | C-01 |
| `src/server/os_core/connector_sdk/health.py` | C-01 响应体 | mock health 实现 |
| `src/server/os_core/shared_contracts/models/*.py` | contract | 7 Schema Pydantic |
| `src/server/db/migrations/versions/001_scale_s01_s04.py` | S-01 | 规模表 migration |
| `src/server/os_core/shared_contracts/tenant_registry.py` | S-03 | get_cell |
| `src/server/os_core/shared_contracts/outbox.py` | S-04 | OutboxPort.publish |
| `scripts/check_import_boundaries.py` | workflow | 静态边界 |
| `src/tests/integration/test_scale_s01_s04.py` | S-01～S-04 | 集成断言 |
| `src/tests/integration/test_connector_c01.py` | C-01 | HTTP 集成 |

## 7. 结论

**结论：通过**

- W1 plan AC 子集（workflow · contract · S-01～S-04 · C-01）**19/19 pytest 绿**
- harness full · static quality · deptry **绿**
- 52 P0 pending **符合 plan**（非 W1 范围）
- 无 Legacy 写 · 无超 scope · 无字段调整
- 允许 `./scripts/gate delivery` 绿后提示 **可以 commit**
