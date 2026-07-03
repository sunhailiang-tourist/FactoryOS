# Verify 回合：W7 Step 7 — 负向安全 N-01～N-04 · Gate 0

> **plan**：`plan-0900-w7-gate0-gip-mcp.md` · **对照** `step-stop-1215-step7.md` · `test-1122-step7-regression.md`

- **step-stop**：`_factoryos_pipeline/2026-07-01/step-stop/step-stop-1215-step7.md`
- **Test 验收**：`_factoryos_pipeline/2026-07-01/test/test-1122-step7-regression.md`
- **对照 AC**：N-01～N-04（harness `-k 'N-01'`）

## 核对项

| # | 项 | 结果 | 证据 |
|---|-----|------|------|
| 1 | 未超 plan 7 范围 | **Pass** | N-03/N-04 实现 · N-01/N-02 既有机制 |
| 2 | 写路径 / 红线 | **Pass** | 无 internal bypass · GET tenant 隔离 · param 校验在 execute 前 |
| 3 | AC 可测 | **Pass** | N-01～N-04 各 1 passed |
| 4 | 无重复逻辑 | **Pass** | `assert_params_safe` · `get_execution_for_tenant` 集中 |
| 5 | 注释四要素 | **Pass** | param_safety · execution · executions controller |
| 6 | Step1–6 回归 | **Pass** | Test 报告 106 passed · 1 skipped |
| 7 | Gate 0 AC 全集 | **Pass** | W7 七步 AC 行为均绿 |
| 8 | 静态质量 | **Fail** | ruff I001 · `execution_service/service.py` import 块未排序 |

## 范围边界

| 项 | 评估 |
|----|------|
| N-01/N-02 无本 Step 新代码 | **Pass** — 404 旁路 · checksum freeze 既有 |
| N-04 模式扫描 | **可接受** — 输入层第一道门禁，非唯一防御 |
| param_safety import 顺序 | **需 Dev 修** — 阻塞 gate |

## 机械门禁

```bash
.venv/bin/pytest src/tests/integration/test_negative_w7.py -v              # 4 passed
.venv/bin/python scripts/check_static_quality.py                          # FAIL（I001）
.venv/bin/python scripts/gate_cli.py step --step 7 -k 'N-01'             # 待执行
```

**static quality 明细**：`execution_service/service.py:8` — `param_safety` 须在 `shared_contracts.models.*` 之后排序

联动链：`step-stop-1215-step7.md` → `test-1122-step7-regression.md` → 本文件

## 结论（必填 · gate 检查）

结论：需改进

阻断理由（若有）：N-01～N-04 **行为与分层通过**，但 **static quality 未绿**，`gate step 7` 无法全绿。

## 建议

1. Dev 修 `execution_service/service.py` import 排序（`ruff check --fix` 可自动修）。
2. 修补后复验 Verify → `gate step --step 7 -k 'N-01'` → 终轮 `gate delivery`。
3. 可选：N-04 模式列表与 ADR/规格文档交叉引用。
