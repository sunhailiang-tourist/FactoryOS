# Step 1 单步验收 · Test 硬性验收报告（复验）

- **对照 plan**：`_factoryos_pipeline/2026-06-30/plan/plan-0330-w5-agent-harness.md` · Step 1
- **命名**：`test-1156-step1-regression.md`
- **口令**：`【Test·Step 1 验收】`（复验 · 对照 `step-stop-0345-step1.md`）

## 1. git diff 改动面（本 Step）

| 路径 | 变更 | plan 预期落位 | 实际落位 | 结论 |
|------|------|---------------|----------|------|
| `agent_orchestrator/service.py` | `create_plan` 无 session | Step1 内核 | ✅ | PASS |
| `agent_orchestrator/plan_store.py` | 内存 PlanStore | Step1 | ✅ | PASS |
| `step-stop-0345-step1.md` | Dev 停机 | 联动门禁 | ✅ | PASS |

**复验修复**：移除 `graph_service`/`rule_engine` import；API 层注入 `allowed_dsl` · `ruleset_id`。

## 2. 本 Step 硬性验收计划（执行记录）

| AC ID | 验收项 | pytest / 证据 | 结果 |
|-------|--------|---------------|------|
| workflow | `create_plan` → DslPlan | `test_w5_step1_*` | **PASS** |
| import_boundaries | 红线 | `test_import_boundaries_*` | **PASS** |
| H-01～H-03 | HTTP | Step2–4 | **FAIL**（预期） |
| 存量 | `-m 'not pending'` | 78 passed | **PASS** |

```bash
uv run pytest src/tests/integration/test_agent_orchestrator_w5_step1.py -v   # 1 passed
uv run pytest src/tests/workflow/test_redlines_static.py::test_import_boundaries_script_passes -v   # 1 passed
uv run pytest src/tests/contract src/tests/workflow src/tests/integration -m 'not pending' -q
# 78 passed · 3 failed（H 预期红）
```

## 3. 代码落位合理性

| 维度 | 检查 | 结论 |
|------|------|------|
| 分层 | agent_orchestrator 仅 shared_contracts + plan_store | ✅ |
| 写路径 | 不写 Legacy | ✅ |
| 红线 | import_boundaries 绿 | ✅ |

## 4. 已改动代码测试报告（本 Step）

| 用例ID | 步骤 | 结果 |
|--------|------|------|
| workflow | `create_plan` + 注入 allowed_dsl | **PASS** |

## 5. 架构与代码质量评估

import 边界修复正确；Graph/Rule 校验上移 API 符合矩阵。

## 6. 结论

**结论：通过**

**下一步**：Verify·Step1 → `gate step --step 1 -k 'workflow'`
