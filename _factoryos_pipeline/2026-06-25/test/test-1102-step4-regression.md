# Step 4 单步验收 · Test 硬性验收报告

- **对照 plan**：`_factoryos_pipeline/2026-06-25/plan/plan-1809-w2-audit-execution.md` · Step 4
- **命名**：`test-1102-step4-regression.md`（HHmm=1102）
- **口令**：`【Test·Step 4 验收】`
- **step-stop**：`step-stop-w2-step4.md`

## 1. git diff 改动面（本 Step）

| 路径 | 变更 | plan 预期 | 结论 |
|------|------|-----------|------|
| `src/os_core/execution_service/service.py` | `assemble_evidence` | Step4 | PASS |
| `src/os_core/execution_service/store.py` | `find_by_exec_id` | Step4 | PASS |
| `src/apps/api/routes/executions.py` | **新增** | Step4 | PASS |
| `src/apps/api/main.py` | 注册 executions router | Step4 | PASS |

## 2. 硬性验收计划（执行记录）

| AC ID | 验收项 | pytest / 证据 | 结果 |
|-------|--------|---------------|------|
| E-09 | evidence 可重建 | `test_E09_execution_evidence_rebuildable[E-09]` | **PASS** |
| E-03 存量 | audit 套件 | `test_audit_e03.py` | **PASS** (3/3) |
| E-06/E-07 存量 | execution 内核 | `test_execution_e06_e07.py` | **PASS** (2/2) |
| W1 存量 | S-* · C-01 · workflow · contract | `-m 'not pending'` | **PASS** (25/25) |
| W2 integration 全量 | 11 项 | `pytest src/tests/integration/` | **PASS** (11/11) |

```bash
uv run pytest src/tests/integration/test_execution_e09.py -v
# → 1 passed

uv run python scripts/check_static_quality.py
# → OK

uv run python scripts/gate_cli.py step --step 4 -k 'E-09'
# → 本报告落盘后执行
```

## 3. 代码落位合理性

| 维度 | 结论 |
|------|------|
| 分层 | **通过** — `executions.py` 薄路由 · `assemble_evidence` 在 os_core |
| F1 契约 | **通过** — required：`exec_id` · `tenant_id` · `execution` · `audit_events` · `assembled_at` |
| W2 范围 | **通过** — `rule_snapshot=null`（W3 Rule 未接入，符合 plan） |
| 404 | **通过** — 无 exec 时 HTTP 404 |
| Verify W2 | **需改进** — 建议补 W2 专用 `verify-*-step4.md`（勿仅依赖 W1 `verify-1558`） |

## 4. 已改动代码测试报告（本 Step · E-09）

| 用例ID | AC/接口 | 步骤 | 结果 |
|--------|---------|------|------|
| E-09 | POST execute → GET evidence | dry_run 执行后拉证据包 | PASS |

**入参 POST `/v1/execute`**：

```json
{
  "tenant_id": "default",
  "graph_id": "graph-d1-generic-template",
  "graph_version": "v1.0.0",
  "verb": "GOVERNED_WRITE",
  "params": {"entity": "work_order", "action": "mock_update"},
  "dry_run": true,
  "idempotency_key": "test-e09-evidence-001",
  "actor": {"user_id": "test-operator", "role": "operator", "channel": "api"}
}
```

**出参 GET `/v1/executions/{execId}/evidence`（摘要）**：

```json
{
  "exec_id": "6f008a5a-89c0-4c67-8064-9dcfa24ffe1b",
  "tenant_id": "default",
  "assembled_at": "2026-06-26T03:02:29.000399Z",
  "execution": {
    "status": "simulated",
    "dry_run": true
  },
  "audit_events": [
    {"event_type": "execute.started"},
    {"event_type": "execute.simulated"}
  ],
  "rule_snapshot": null
}
```

结构依据：`contracts/schemas/ExecutionEvidence.schema.json`

## 5. 架构与代码质量评估

**结论：通过**

| 维度 | 评估 |
|------|------|
| E-09 功能 | **通过** — 200 · audit_events ≥ 1 · execution 嵌套一致 |
| 聚合逻辑 | **通过** — `find_by_exec_id` + `list_audit_events` |
| 存量未破坏 | **通过** — W2 全 integration 11/11 |
| 过程 | **需改进（非阻断）** — 建议 W2 Verify Step4 独立落盘 |

## 6. 结论

**结论：通过**

W2 plan AC 子集 **E-03 · E-06 · E-07 · E-09** 全部 pytest 绿；Step4 机械 gate 待本报告落盘后复跑。

→ 可进入 **【Test·终轮回归】** + `./scripts/gate delivery` → `./scripts/gate pr`
