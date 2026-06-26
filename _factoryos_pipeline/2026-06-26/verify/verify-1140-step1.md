# Verify 回合：W3 Step 1 — Alembic 003 + graph_service 内核

> **plan**：`plan-1121-w3-graph-rule.md` · **对照** `step-stop-1132-step1.md` · `test-1132-step1-regression.md`

- **step-stop**：`_factoryos_pipeline/2026-06-26/step-stop/step-stop-1132-step1.md`
- **Test 验收**：`_factoryos_pipeline/2026-06-26/test/test-1132-step1-regression.md`
- **对照 AC**：G-01（harness `-k 'G-01'`）

## 核对项

| # | 项 | 结果 | 证据 |
|---|-----|------|------|
| 1 | 未超 plan 范围 | **Pass** | `003_graphs_rulesets` · `graph_service/` 内核 CRUD 对齐 Step1 |
| 2 | 写路径 / 红线 | **Pass** | Graph 不写 Legacy；import_boundaries 绿 |
| 3 | AC 可测 | **Pass** | `test_G01_create_draft_graph[G-01]` 绿 |
| 4 | 无重复逻辑 | **Pass** | store/service 分层；checksum 独立模块 |
| 5 | 注释四要素 | **Pass** | `graph_service/README.md` + service/store 文件头 |

## 机械门禁

联动链：`step-stop-1132-step1.md` → `test-1132-step1-regression.md` → 本文件。`check_verify.py --step 1 --require-pass`：**OK**

## 结论（必填 · gate 检查）

结论：通过

阻断理由（若有）：无

## 建议

1. W3 代码虽批量合入，逐步落盘已补录；后续迭代按 SH 逐步走链。
2. Step2 Dev 前须本 Step `gate step` 绿（联动门禁已机械校验）。
