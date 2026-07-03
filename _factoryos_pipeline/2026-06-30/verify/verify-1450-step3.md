# Verify 回合：W6 Step 3 — reconciliation 内核（K-01）

> **plan**：`plan-1350-w6-reconcile-license.md` · **对照** `step-stop-1440-step3.md` · `test-1445-step3-regression.md`

- **step-stop**：`_factoryos_pipeline/2026-06-30/step-stop/step-stop-1440-step3.md`
- **Test 验收**：`_factoryos_pipeline/2026-06-30/test/test-1445-step3-regression.md`
- **对照 AC**：K-01（harness `-k 'K-01'`）

## 核对项

| # | 项 | 结果 | 证据 |
|---|-----|------|------|
| 1 | 未超 plan 范围 | **Pass** | 仅内核 `run_reconciliation` · store · contracts；无 `POST /v1/reconciliation/run` |
| 2 | 写路径 / 红线 | **Pass** | read-back `mock_legacy.get_entity` · 不写 Legacy · Shadow 过滤 dry_run/shadow |
| 3 | AC 可测 | **Pass** | `test_K01_reconciliation_run_returns_ok[K-01]` 绿 |
| 4 | 无重复逻辑 | **Pass** | `_compare_fields` 复用 K-02；store 查询集中 `list_success_legacy_writes` |
| 5 | 注释四要素 | **Pass** | service · store · README · reconciliation 模型 |
| 6 | Step1–2 回归 | **Pass** | license workflow + T-02 各 1 passed |
| 7 | 内核 registry | **Pass** | 11 modules · import_boundaries 矩阵含 reconciliation_service |
| 8 | 静态质量 | **Fail** | ruff F821 · pyright 未定义 `Any`（`service.py:28`） |

## 范围边界

| 项 | 评估 |
|----|------|
| K-02 仍红 | **预期** — Step4 HTTP |
| `studio_flows.json` 提及 reconciliation API | **可接受** — 文档/flow 占位，无路由实现 |
| `records_skipped_shadow` 计数含 dry_run/非 success | **备忘** — 命名略宽，行为不影响 K-01 |

## 机械门禁

```bash
.venv/bin/pytest src/tests/integration/test_reconciliation_w6.py -k 'K-01' -v   # 1 passed
.venv/bin/python scripts/gate_cli.py step --step 3 -k 'K-01'                 # FAIL（static quality）
```

| 子门禁 | 结果 |
|--------|------|
| harness full · K-01 | **绿** · `06-49_gate-step_harness-full_step3.md` |
| static quality | **红** · `06-49_gate-step_static-quality_step3.md` |

联动链：`step-stop-1440-step3.md` → `test-1445-step3-regression.md` → 本文件

## 结论（必填 · gate 检查）

结论：需改进

阻断理由（若有）：`reconciliation_service/service.py` 第 28 行使用 `Any` 未 `from typing import Any`，ruff/pyright 双失败，**gate step 3 未绿**。

## 建议

1. Dev 补 `from typing import Any`（或改为 `dict[str, object]`）后重跑 `gate step --step 3 -k 'K-01'`。
2. Step4 实现 `POST /v1/reconciliation/run` + K-02 drift HTTP 路径。
3. 可选：收紧 `records_skipped_shadow` 计数语义或改名，避免与 shadow_mode 字段混淆。
