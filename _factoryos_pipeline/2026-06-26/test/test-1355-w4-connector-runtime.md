# 测试用例与改动面：W4 connector runtime · L2 真写 · Revert failing tests

- **对照 plan**：`_factoryos_pipeline/2026-06-26/plan/plan-1339-w4-connector-runtime.md`
- **命名**：`test-1355-w4-connector-runtime.md`（HHmm=1355 落盘当下本地时间）
- **目的**：新增 · W4 Step1～4 failing tests（B/C/E 目标 AC · W1–W3 存量回归）

## 1. 改动文件（Test Agent 本轮）

| 路径 | 变更 | 职责 |
|------|------|------|
| `src/tests/integration/test_connector_blueprint_w4.py` | 新增 | B-01～B-04 blueprint registry · 校验 |
| `src/tests/integration/test_connector_runtime_w4.py` | 新增 | C-02～C-04 runtime entity read/write |
| `src/tests/integration/test_execution_e02_e04_e05.py` | 新增 | E-02 · E-04 · E-05 · E-09 snapshot 增强 |
| `src/tests/ac/test_base001_registry.py` | 修改 | W4 目标 AC 移出 pending 池 |

## 2. AC 用例

| ID | 标题 | 类型 | 期望 |
|----|------|------|------|
| B-01 | 加载 mock blueprint | integration | `load_blueprint(conn-mock)` · ops 含 `GOVERNED_WRITE` |
| B-02 | Runtime 执行 L2 op | integration | `execute_op` · `legacy_refs` 非空 |
| B-03 | mapping 错误 | integration | 缺 mapping 字段 → `MAPPING_ERROR` |
| B-04 | revert 声明 | integration | L2 op 无 revert → `BLUEPRINT_INVALID` / 422 |
| C-02 | read entity | integration | `entity.get` 返回 snapshot |
| C-03 | write entity | integration | `entity.update` · `legacy_refs` populated |
| C-04 | revert read-back | integration | write 后 read 与 `after_snapshot` 一致 |
| E-02 | L2 写成功 | integration | `dry_run=false` · success · before/after snapshot |
| E-03 | Audit 产生 | integration | 随 E-02 回归（存量 `test_audit_e03`） |
| E-04 | Revert 成功 | integration | POST revert · status=reverted · Legacy 恢复 |
| E-05 | 重复 revert | integration | 已 reverted 再 revert → 409 |
| E-09 | Evidence 可重建 | integration | L2 写后 evidence 含 snapshot 字段 |
| G/R/D/E-01 等 | W3 存量 | 回归 | `pytest -m 'not pending'` 42 项保持绿 |

## 3. Harness（Step 停机验收盘）

```bash
./scripts/gate step --step 1 -k 'B-01'
./scripts/gate step --step 2 -k 'C-02'
./scripts/gate step --step 3 -k 'E-02'
./scripts/gate step --step 4 -k 'E-04'
```

## 4. 标准测试用例

| ID | 标题 | 类型 | 前置 | 步骤摘要 | 期望 |
|----|------|------|------|----------|------|
| B-01 | blueprint load | integration | `registry.load_blueprint` | pack_id=conn-mock | ops 含 GOVERNED_WRITE |
| B-02 | runtime L2 | integration | blueprint loaded | `execute_op(GOVERNED_WRITE)` | legacy_refs 非空 |
| B-03 | mapping 负向 | integration | runtime | 缺必填 mapping 入参 | MAPPING_ERROR |
| B-04 | revert 声明 | integration | validate | L2 op 无 revert 块 | BLUEPRINT_INVALID |
| C-02 | entity.get | integration | mock entity store | read work_order | snapshot dict |
| C-03 | entity.update | integration | C-02 前置 | update 字段 | legacy_refs |
| C-04 | read-back | integration | C-03 写后 | entity.get | == after_snapshot |
| E-02 | L2 HTTP | integration | frozen graph | POST execute dry_run=false | success · snapshots |
| E-04 | revert HTTP | integration | E-02 成功 | POST `/v1/execute/{id}/revert` | reverted |
| E-05 | dup revert | integration | E-04 后 | 再次 revert | 409 |
| E-09+ | evidence snapshot | integration | E-02 | GET evidence | execution 含 before/after |

### DB 策略

- 延续 W1–W3：`TEST_DATABASE_URL` 或 SQLite + Alembic upgrade head
- E-02/E-04/E-05 走 HTTP + `frozen_graph_env` fixture
- B/C 内核测经 `connector_sdk.registry` · `connector_sdk.runtime`

## 5. 与 plan 核对

| 项 | 结论 |
|----|------|
| plan 路径 | `plan-1339-w4-connector-runtime.md` ✓ |
| Step 范围 | 1 B-01 → 2 C-02 → 3 E-02 → 4 E-04 ✓ |
| 不在 W4 | D-04 · E-08 · H/K/P/T/M · 52 其余 pending ✓ |
| 必测 | B-01～04 · C-02～04 · E-02/04/05 · E-03/09 回归 |
| 回归 | W1–W3 42 项 `pytest -m 'not pending'` |
| 公共链路风险 | **高** — connector_sdk runtime · execution L2 真写 · revert HTTP |
| 红线 | 写仅经 execution_service → connector_sdk · audit append-only |

## Gate A–G 摘要

| Gate | 结论 |
|------|------|
| A 复盘 | 九模块 · R-01 写路径 · OpenAPI execute/revert · integration 布局 |
| B 目的 | **新增** — W4 failing tests 驱动红→绿 |
| C 协作 | plan 改动：registry · runtime · conn-mock · execution revert · 4 Step |
| D 质量 | 待 Dev 实现后单步评估 |
| E 接口分区 | 见下节 |
| F 字段 | ExecutionRecord before/after_snapshot · legacy_refs · evidence 增强 |
| G 命名 | test-1355 与落盘时间一致 ✓ |

## 📦 本次新增接口

```json
POST /v1/execute/{execId}/revert
```

响应 `ExecutionRecord`（status=`reverted`）。

## 🔁 本次需求涉及到的接口（字段调整）

`POST /v1/execute`（非 dry_run L2）响应增：

```json
{
  "exec_id": "uuid",
  "verb": "GOVERNED_WRITE",
  "status": "success",
  "dry_run": false,
  "before_snapshot": { "entity_type": "work_order", "entity_id": "wo-1", "fields": {} },
  "after_snapshot": { "entity_type": "work_order", "entity_id": "wo-1", "fields": { "status": "in_progress" } },
  "legacy_refs": [{ "system": "mock", "ref_type": "entity", "ref_id": "wo-1" }]
}
```

`GET /v1/executions/{execId}/evidence` 中 `execution` 须含上述 snapshot 字段。
