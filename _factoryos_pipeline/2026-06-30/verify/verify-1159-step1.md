# Verify 回合：W5 Step 1 — agent_orchestrator 内核 stub + PlanStore（workflow）

> **plan**：`plan-0330-w5-agent-harness.md` · **对照** `step-stop-0345-step1.md` · `test-1156-step1-regression.md`

- **step-stop**：`_factoryos_pipeline/2026-06-30/step-stop/step-stop-0345-step1.md`
- **Test 验收**：`_factoryos_pipeline/2026-06-30/test/test-1156-step1-regression.md`（复验 · 初验 `test-1149` 需改进已修）
- **对照 AC**：workflow（harness `-k 'workflow'`）

## 核对项

| # | 项 | 结果 | 证据 |
|---|-----|------|------|
| 1 | 未超 plan 范围 | **Pass** | `service.py` · `plan_store.py` · `__init__.py`；无 HTTP agent/harness 路由 |
| 2 | 写路径 / 红线 | **Pass** | `create_plan` 仅产 DslPlan + 内存 store；无 Legacy 写 · 无 LiteLLM |
| 3 | AC 可测 | **Pass** | `test_w5_step1_create_plan_stub_returns_dsl_plan[workflow]` 绿 |
| 4 | import 边界 | **Pass** | 移除 graph/rule 内核 import；`test_import_boundaries_script_passes` 绿 |
| 5 | 注释四要素 | **Pass** | service/plan_store/__init__/README 齐全 |

## 架构修正（初验阻断 → 复验通过）

| 项 | 评估 |
|----|------|
| Graph/Rule 校验上移 API | **正确** — `create_plan` 接收 `ruleset_id` · `allowed_dsl` 注入，符合 os_core-public-api 矩阵 |
| 内存 PlanStore | **可接受** — plan 明确 Step1 可选 005 migration；W6+ 可换 DB |
| stub 动词 `GOVERNED_WRITE` | **Pass** — `require_known_verb` + allowed_dsl 可选校验 |

## 范围边界

| 项 | 评估 |
|----|------|
| H-01/H-02/H-03 仍红（3 项） | **预期** — Step2–4 HTTP harness |
| 存量 78 passed | **Pass** — W1–W4 无破坏 |

## 机械门禁

```bash
.venv/bin/pytest src/tests/integration/test_agent_orchestrator_w5_step1.py -k workflow -v   # 1 passed
.venv/bin/pytest src/tests/workflow/test_redlines_static.py::test_import_boundaries_script_passes -v  # 1 passed
.venv/bin/python scripts/gate_cli.py step --step 1 -k 'workflow'                          # ❌ Static quality FAILED
```

**gate 阻塞项（ruff · 3 处）**：

| 文件 | 规则 | 说明 |
|------|------|------|
| `agent_orchestrator/service.py:60` | E501 | docstring 行超 100 字符 |
| `test_agent_orchestrator_w5_step1.py:7` | I001 | import 排序 |
| `test_harness_w5.py:150` | E501 | assert 行超 100 字符 |

联动链：`step-stop-0345-step1.md` → `test-1156-step1-regression.md` → 本文件

## 结论（必填 · gate 检查）

结论：需改进

阻断理由（若有）：`gate step --step 1` 未绿 — static quality（ruff E501/I001 ×3）；范围/红线/AC 审阅通过，Dev 修 ruff 后复跑 gate

## 建议

1. Dev 修上述 3 处 ruff（`ruff check --fix` 可修 I001）→ 复跑 `gate step --step 1 -k 'workflow'`。
2. Step2 实现 POST `/v1/agent/plan` 时在 API 层完成 graph frozen + allowed_dsl 查询后注入内核。
3. Step3 confirm 从 `plan_store.get_plan` 读取，保持确认门 R11。
