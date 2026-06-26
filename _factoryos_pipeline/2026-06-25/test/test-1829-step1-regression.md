# Step 1 单步验收 · Test 硬性验收报告

- **对照 plan**：`_factoryos_pipeline/2026-06-25/plan/plan-1809-w2-audit-execution.md` · Step 1
- **命名**：`test-1829-step1-regression.md`（HHmm=1829）
- **口令**：`【Test·Step 1 验收】`

## 1. git diff 改动面（本 Step）

| 路径 | 变更 | plan 预期落位 | 实际落位 | 结论 |
|------|------|---------------|----------|------|
| `alembic/versions/002_audit_execution.py` | 新增 | Step1 migration | ✅ | PASS |
| `src/server/os_core/audit_service/store.py` | 新增 | audit append/query | ✅ | PASS |
| `src/server/os_core/audit_service/__init__.py` | 新增 | 包入口 | ✅ | PASS |

## 2. 本 Step 硬性验收计划（执行记录）

| AC ID | 验收项 | pytest / 证据 | 结果 |
|-------|--------|---------------|------|
| workflow | import_boundaries + `/health` | `pytest src/tests/workflow/ -m 'not pending'` | **PASS** (4/4) |
| Step1 | migration 002 表存在 | `test_w2_audit_execution_migration_tables` | **PASS** |
| Step1 | audit append + query 内核 | `test_audit_service_append_only_kernel` | **PASS** |
| E-03 HTTP | GET `/v1/audit/events` | `test_E03_audit_events_after_execute` | **FAIL**（Step2 范围，预期红） |
| E-06/07/09 | execution | 对应用例 | **FAIL**（Step3/4，预期红） |

```bash
uv run pytest src/tests/integration/test_audit_e03.py::test_w2_audit_execution_migration_tables \
  src/tests/integration/test_audit_e03.py::test_audit_service_append_only_kernel \
  src/tests/workflow/ -m "not pending" -v
# → 5 passed

uv run python scripts/gate_cli.py step --step 1 -k 'workflow'
# → harness 绿 · pytest workflow 绿 · static quality FAIL（store.py UP017）
```

## 3. 代码落位合理性

| 维度 | 检查 | 结论 |
|------|------|------|
| 分层 | 业务在 `os_core/audit_service`；无 server/api 写规则 | **通过** |
| 写路径 | 仅 audit INSERT；无 Legacy 写 | **通过** |
| 红线 | append-only；无 UPDATE/DELETE | **通过** |
| 注释 | store.py 文件头 + 函数四要素 | **通过** |
| Schema | 表字段对齐 AuditEvent；execution_records 预埋 E-07 | **通过** |

## 4. 已改动代码测试报告（本 Step）

| 用例ID | AC/接口 | 步骤 | 结果 |
|--------|---------|------|------|
| — | migration 002 | alembic upgrade + inspect | PASS |
| — | `append_audit_event` | INSERT + list by exec_id | PASS |

**内核入参（append_audit_event）**：

```json
{
  "tenant_id": "default",
  "event_type": "execute.completed",
  "exec_id": "00000000-0000-4000-8000-000000000001",
  "actor": {"user_id": "test", "role": "operator"},
  "payload": {"probe": true}
}
```

**内核出参（AuditEvent 摘要）**：

```json
{
  "event_id": "96efa3e9-786e-430a-8423-88ed9a6834e1",
  "event_type": "execute.completed",
  "count": 1
}
```

结构依据：`contracts/schemas/AuditEvent.schema.json`

**HTTP**：本 Step 无新增接口。

## 5. 架构与代码质量评估（本 Step）

| 维度 | 结论 |
|------|------|
| 分层 | 通过 — store 在 audit_service，复用 shared_contracts.AuditEvent |
| 落位 | 通过 — migration 002 与 W1 001 链式；execution_records 预埋合理 |
| 耦合 | 通过 — 仅依赖 Session + Pydantic |
| 静态 | **需改进** — `store.py:57` ruff UP017（`timezone.utc` → `datetime.UTC`） |

## 6. 结论

**结论：需改进**

**功能验收通过**（Step1 范围 5/5 pytest 绿；Step2+ 仍红 4 项符合 plan）。

**机械验收盘未绿**：`./scripts/gate step --step 1 -k 'workflow'` 因 `check_static_quality` 失败。

**Dev 回修 1 项**（Test 不偷改业务）：

```text
src/server/os_core/audit_service/store.py:57
  datetime.now(timezone.utc) → datetime.now(datetime.UTC)
```

修后重跑 `./scripts/gate step --step 1 -k 'workflow'` 应全绿。

- 你回复 **`风险接受并继续`** → 可进 Verify（接受 static 欠账）
- 或 Dev 修 ruff 后 → **结论升通过** → Verify 新会话
