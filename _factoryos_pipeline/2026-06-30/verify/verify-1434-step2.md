# Verify 回合：W6 Step 2 — execution license 门禁（T-02）

> **plan**：`plan-1350-w6-reconcile-license.md` · **对照** `step-stop-1425-step2.md` · `test-1432-step2-regression.md`

- **step-stop**：`_factoryos_pipeline/2026-06-30/step-stop/step-stop-1425-step2.md`
- **Test 验收**：`_factoryos_pipeline/2026-06-30/test/test-1432-step2-regression.md`
- **对照 AC**：T-02（harness `-k 'T-02'`）

## 核对项

| # | 项 | 结果 | 证据 |
|---|-----|------|------|
| 1 | 未超 plan 范围 | **Pass** | `execution_service` license 钩子 · import 矩阵；无 reconciliation HTTP |
| 2 | 写路径 / 红线 | **Pass** | 未授权 tenant 403 · 无 graph/rule/execute/Legacy 写 |
| 3 | AC 可测 | **Pass** | `test_T02_execute_unlicensed_pack_returns_403_and_audit[T-02]` 绿 |
| 4 | audit | **Pass** | `license.denied` ≥1 条 |
| 5 | Step1 回归 | **Pass** | workflow 1 passed · import_boundaries 绿 |
| 6 | 静态质量 | **Pass** | ruff · pyright 全绿 |

## 范围边界

| 项 | 评估 |
|----|------|
| license 在幂等查询之后 | **可接受** — 未授权 tenant 仍应拦截；已授权幂等返回不受影响 |
| `DEFAULT_PACK_ID` 硬编码 | **备忘** — W7+ Pack 解析 |
| K-01/K-02 仍红（2 项） | **预期** — Step3–4 |
| 存量 83 passed | **Pass** |

## 机械门禁

```bash
.venv/bin/pytest src/tests/integration/test_license_t02_w6.py -k 'T-02' -v   # 1 passed
.venv/bin/python scripts/gate_cli.py step --step 2 -k 'T-02'              # 待执行
```

联动链：`step-stop-1425-step2.md` → `test-1432-step2-regression.md` → 本文件

## 结论（必填 · gate 检查）

结论：通过

阻断理由（若有）：无

## 建议

1. Step3 实现 `reconciliation_service.run_reconciliation`（K-01）。
2. 可选：未授权路径也写 audit 前避免 commit 与后续 rollback 交互 — 当前单测已绿。
