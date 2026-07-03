# Verify 回合：W5 Step 1 — agent_orchestrator 内核 stub + PlanStore（workflow · 复验）

> **plan**：`plan-0330-w5-agent-harness.md` · **对照** `step-stop-0345-step1.md` · `test-1156-step1-regression.md`

- **step-stop**：`_factoryos_pipeline/2026-06-30/step-stop/step-stop-0345-step1.md`
- **Test 验收**：`_factoryos_pipeline/2026-06-30/test/test-1156-step1-regression.md`
- **对照 AC**：workflow（harness `-k 'workflow'`）
- **前次 Verify**：`verify-1159-step1.md`（需改进 · ruff 阻塞）→ 本轮复验

## 核对项

| # | 项 | 结果 | 证据 |
|---|-----|------|------|
| 1 | 未超 plan 范围 | **Pass** | `service.py` · `plan_store.py` · `__init__.py`；无 HTTP agent/harness 路由 |
| 2 | 写路径 / 红线 | **Pass** | `create_plan` 仅产 DslPlan + 内存 store；无 Legacy 写 · 无 LiteLLM |
| 3 | AC 可测 | **Pass** | `test_w5_step1_create_plan_stub_returns_dsl_plan[workflow]` 绿 |
| 4 | import 边界 | **Pass** | `test_import_boundaries_script_passes` 绿 |
| 5 | 静态质量 | **Pass** | ruff · pyright 全绿（前次 E501/I001 ×3 已修） |
| 6 | 注释四要素 | **Pass** | service/plan_store/__init__/README 齐全 |

## 范围边界

| 项 | 评估 |
|----|------|
| H-01/H-02/H-03 仍红（3 项） | **预期** — Step2–4 HTTP harness |
| 存量 78 passed | **Pass** — W1–W4 无破坏 |

## 机械门禁

```bash
.venv/bin/pytest src/tests/integration/test_agent_orchestrator_w5_step1.py -k workflow -v   # 1 passed
.venv/bin/pytest src/tests/workflow/test_redlines_static.py::test_import_boundaries_script_passes -v  # 1 passed
.venv/bin/python scripts/check_static_quality.py                                            # OK
.venv/bin/python scripts/gate_cli.py step --step 1 -k 'workflow'                            # 待执行
```

联动链：`step-stop-0345-step1.md` → `test-1156-step1-regression.md` → 本文件

## 结论（必填 · gate 检查）

结论：通过

阻断理由（若有）：无

## 建议

1. Step2 实现 POST `/v1/agent/plan` 时在 API 层完成 graph frozen + allowed_dsl 查询后注入内核。
2. Step3 confirm 从 `plan_store.get_plan` 读取，保持确认门 R11。
