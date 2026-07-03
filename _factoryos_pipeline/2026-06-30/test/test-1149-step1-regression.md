# Step 1 单步验收 · Test 硬性验收报告

- **对照 plan**：`_factoryos_pipeline/2026-06-30/plan/plan-0330-w5-agent-harness.md` · Step 1
- **命名**：`test-1149-step1-regression.md`
- **口令**：`【Test·Step 1 验收】`

## 1. git diff 改动面（本 Step）

| 路径 | 变更 | plan 预期落位 | 实际落位 | 结论 |
|------|------|---------------|----------|------|
| `agent_orchestrator/service.py` | 新增 `create_plan` | Step1 内核 | ✅ | PASS（功能） |
| `agent_orchestrator/plan_store.py` | 内存 PlanStore | Step1 | ✅ | PASS |
| `step-stop-*-step1.md` | — | Dev 停机 | ❌ 缺失 | 需改进 |

## 2. 本 Step 硬性验收计划（执行记录）

| AC ID | 验收项 | pytest / 证据 | 结果 |
|-------|--------|---------------|------|
| workflow | `create_plan` → DslPlan | `test_w5_step1_*` | **PASS** |
| H-01～H-03 | HTTP | Step2–4 | **FAIL**（预期） |
| import_boundaries | 红线 | `test_import_boundaries_*` | **FAIL** |
| 存量 | `-m 'not pending'` | 77 passed | **PASS** |

```bash
uv run pytest src/tests/integration/test_agent_orchestrator_w5_step1.py -v   # 1 passed
uv run pytest src/tests/contract src/tests/workflow src/tests/integration -m 'not pending' -q
# 77 passed · 4 failed
```

## 3. 代码落位合理性

| 维度 | 检查 | 结论 |
|------|------|------|
| 写路径 | create_plan 不写 Legacy | ✅ |
| 红线 | import_boundaries 违规 | ❌ |

**违规**：`service.py` 不得 import `graph_service` · `rule_engine`（agent_orchestrator 仅允许 `shared_contracts`）。

## 4. 已改动代码测试报告（本 Step）

| 用例ID | 步骤 | 结果 |
|--------|------|------|
| workflow | `create_plan` frozen graph | **PASS** |

出参含 `source=agent` · `steps[0].verb=GOVERNED_WRITE` · `plan_id` UUID。

## 5. 架构与代码质量评估

**需改进**：Graph/Rule 校验上移 API 层或去耦 import；补 Dev step-stop。

## 6. 结论

**结论：需改进**

- create_plan **功能 PASS** · import_boundaries **FAIL** · 缺 step-stop
- 修复后 → Verify·Step1 → `gate step --step 1 -k 'workflow'`
