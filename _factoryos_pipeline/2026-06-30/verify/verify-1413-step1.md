# Verify 回合：W6 Step 1 — license_service stub（workflow）

> **plan**：`plan-1350-w6-reconcile-license.md` · **对照** `step-stop-1415-step1.md` · `test-1408-step1-regression.md`

- **step-stop**：`_factoryos_pipeline/2026-06-30/step-stop/step-stop-1415-step1.md`
- **Test 验收**：`_factoryos_pipeline/2026-06-30/test/test-1408-step1-regression.md`
- **对照 AC**：workflow（harness `-k 'workflow'`）

## 核对项

| # | 项 | 结果 | 证据 |
|---|-----|------|------|
| 1 | 未超 plan 范围 | **Pass** | 仅 `license_service/service.py` · `__init__.py`；无 execution 钩子 · 无 reconciliation |
| 2 | 写路径 / 红线 | **Pass** | 只读校验；无 Legacy 写 |
| 3 | AC 可测 | **Pass** | `test_w6_step1_assert_pack_licensed_allows_known_pack[workflow]` 绿 |
| 4 | import 边界 | **Pass** | 仅 `shared_contracts` · import_boundaries 绿 |
| 5 | 静态质量 | **Pass** | ruff · pyright 全绿 |
| 6 | 注释/模块治理 | **Pass** | service/__init__/README 齐全 |

## 范围边界

| 项 | 评估 |
|----|------|
| T-02/K-01/K-02 仍红（3 项） | **预期** — Step2–4 |
| 存量 W1–W5（82 passed） | **Pass** |
| 静态 `_LICENSED_BY_TENANT` | **可接受** — plan stub；Step2+ 接 execution |

## 机械门禁

```bash
.venv/bin/pytest src/tests/integration/test_license_w6_step1.py -k workflow -v   # 1 passed
.venv/bin/python scripts/gate_cli.py step --step 1 -k 'workflow'                # 待执行
```

联动链：`step-stop-1415-step1.md` → `test-1408-step1-regression.md` → 本文件

## 结论（必填 · gate 检查）

结论：通过

阻断理由（若有）：无

## 建议

1. Step2 在 `execution_service.execute` 调用 `assert_pack_licensed` 并写 `license.denied` audit。
2. 负向 pack 测试可留在 T-02 HTTP 用例，内核已具备抛错能力。
