# 测试用例与改动面：W1 Step1～4 failing tests

- **对照 plan**：`_factoryos_pipeline/2026-06-25/plan/plan-0116-w1-base.md`
- **命名**：`test-1443-w1-step1-4.md`（HHmm=1443 落盘当下本地时间）
- **目的**：新增 · W1 Step1～4 failing tests（S-01～S-04 · C-01 · workflow · contract）

## 1. 改动文件（Test Agent 本轮）

| 路径 | 变更 | 职责 |
|------|------|------|
| `src/tests/workflow/test_api_health.py` | 新增 | Step1 `GET /health` |
| `src/tests/contract/test_shared_contracts.py` | 新增 | Step2 Schema↔Pydantic 对齐 |
| `src/tests/integration/test_scale_s01_s04.py` | 新增 | Step3 S-01～S-04 |
| `src/tests/integration/test_connector_c01.py` | 新增 | Step4 C-01 mock health |
| `src/tests/ac/test_base001_registry.py` | 修改 | W1 目标 AC 移出 pending 池 |
| `src/tests/conftest.py` | 修改 | integration marker · schema fixture |
| `pyproject.toml` | 修改 | `integration` marker |

## 2. AC 用例

| ID | 标题 | 类型 | 期望 |
|----|------|------|------|
| workflow | import_boundaries + `/health` | workflow | boundaries 脚本绿 · health 200 |
| contract | shared_contracts 7 Schema | contract | Pydantic 模型存在且 required 字段对齐 |
| S-01 | 规模表 migration | integration | `alembic upgrade head` 后四表存在 |
| S-02 | tenant 默认值 | integration | seed `cell-default` / `pool` |
| S-03 | TenantRegistry | integration | `get_cell(default)` → `cell-default` |
| S-04 | Queue/outbox 接口 | integration | in-process outbox 可 insert |
| C-01 | connector healthCheck | integration | `GET /v1/connectors/{packId}/health` → `status=ok` |

## 3. Harness（Step 停机验收盘）

```bash
./scripts/gate step --step 1 -k 'workflow'
./scripts/gate step --step 2 -k 'contract'
./scripts/gate step --step 3 -k 'S-01'
./scripts/gate step --step 4 -k 'C-01'
```

## 4. 标准测试用例

| ID | 标题 | 类型 | 前置 | 步骤摘要 | 期望 |
|----|------|------|------|----------|------|
| workflow | health 存活 | workflow | FastAPI app | GET `/health` | 200 + JSON body |
| contract | DslPlan 对齐 | contract | `shared_contracts.models` | 比对 required 字段 | 与 `DslPlan.schema.json` 一致 |
| S-01 | 规模表 | integration | alembic.ini | upgrade head · inspect metadata | tenants/connector_instances/tenant_quotas/outbox_events |
| S-02 | 默认 tenant | integration | S-01 后 | 查 tenants 首行 | cell_id=cell-default, placement_tier=pool |
| S-03 | TenantRegistry | integration | S-02 后 | `TenantRegistry.get_cell("default")` | `cell-default` |
| S-04 | outbox 写入 | integration | S-01 后 | `OutboxPort.publish(...)` | outbox_events 有行 |
| C-01 | mock health | integration | connector_sdk + route | GET health + tenant_id | 200, status=ok |

### DB 策略（Step3 无本地 PG）

- **首选**：pytest 用 **SQLite 内存库**（`sqlite+aiosqlite:///:memory:`）跑 Alembic upgrade + ORM 断言；与 asyncpg 方言差异在 Dev Step3 实现时以 `contracts/schemas` 为准对齐。
- **备选**：CI 有 PG 时用 `TEST_DATABASE_URL` 环境变量覆盖（conftest 读取，未设则 SQLite）。
- **不依赖 Redis**：S-04 in-process outbox 仅验 DB 持久化。

## 5. 与 plan 核对

| 项 | 结论 |
|----|------|
| plan 路径 | `_factoryos_pipeline/2026-06-25/plan/plan-0116-w1-base.md` ✓ |
| Step 范围 | 1～4 only；G/R/E 仍 pending ✓ |
| 必测 AC | S-01～S-04 · C-01 · workflow · contract ✓ |
| 建议测 | integration `_template` YAML vs SystemRelation（Step4 Dev 交付后补） |
| 回归 | 存量 `test_openapi_contract` · `test_redlines_static` · import_boundaries |
| 公共链路风险 | **低** — 本轮无 Legacy 写 · 无 execution/graph/rule 运行时 |
| 52 P0 其余 | 保持 `@pytest.mark.pending` 红测占位 |
