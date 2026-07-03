# Verify 回合：W7 Step 1 — tenant shadow_mode（T-01）· 复验

> **plan**：`plan-0900-w7-gate0-gip-mcp.md` · **对照** `step-stop-1705-step1.md` · `test-1736-step1-regression.md`  
> **复验原因**：上轮 `verify-1738-step1.md` static quality Fail；Dev 已修 ruff

- **step-stop**：`_factoryos_pipeline/2026-07-01/step-stop/step-stop-1705-step1.md`
- **Test 验收**：`_factoryos_pipeline/2026-07-01/test/test-1736-step1-regression.md`
- **对照 AC**：T-01（harness `-k 'T-01'`）

## 核对项

| # | 项 | 结果 | 证据 |
|---|-----|------|------|
| 1 | 未超 plan 1 范围 | **Pass** | tenant_service · execution effective_shadow · API 薄路由 |
| 2 | 写路径 / 红线 | **Pass** | shadow 时 L2 simulated · Legacy 0 写 |
| 3 | AC 可测 | **Pass** | `test_T01_*[T-01]` 绿 |
| 4 | 无重复逻辑 | **Pass** | `resolve_shadow_mode` 单一真源 |
| 5 | 注释四要素 | **Pass** | tenant_service · execution · tenant controller |
| 6 | MCP 预留 | **Pass** | 内核 REST/MCP 共用 |
| 7 | import_boundaries | **Pass** | execution → tenant_service |
| 8 | 静态质量 | **Pass** | ruff · pyright 0 errors |
| 9 | 上轮 if applicable | **Pass** | Test 复验 95 passed（Step2–7 红测已 ignore） |

## 范围边界

| 项 | 评估 |
|----|------|
| 上轮 ruff I001/E501 | **已关闭** — import 排序 + payload 换行 |
| W7 红测文件 import | **已关闭** — 全仓 static 绿 |

## 机械门禁

```bash
.venv/bin/python scripts/check_static_quality.py                              # OK
.venv/bin/pytest src/tests/integration/test_shadow_w7.py -k 'T-01' -q          # 1 passed
.venv/bin/python scripts/gate_cli.py step --step 1 -k 'T-01'                 # 待执行
```

联动链：`step-stop-1705-step1.md` → `test-1736-step1-regression.md` → 本文件

## 结论（必填 · gate 检查）

结论：通过

阻断理由（若有）：无

## 建议

1. Step2：`CONNECTOR_NOT_CONFIGURED` + license 读 tenant `licensed_packs`（T-03）。
2. 可选：HTTP 返回类型改为强类型 TenantSettings schema。
