# Verify 回合：W7 Step 2 — CONNECTOR_NOT_CONFIGURED + license 真源（T-03）

> **plan**：`plan-0900-w7-gate0-gip-mcp.md` · **对照** `step-stop-0950-step2.md` · `test-1750-step2-regression.md`

- **step-stop**：`_factoryos_pipeline/2026-07-01/step-stop/step-stop-0950-step2.md`
- **Test 验收**：`_factoryos_pipeline/2026-07-01/test/test-1750-step2-regression.md`
- **对照 AC**：T-03（harness `-k 'T-03'`）

## 核对项

| # | 项 | 结果 | 证据 |
|---|-----|------|------|
| 1 | 未超 plan 2 范围 | **Pass** | connector/license 真源 · execution 门禁；无 Package/MCP |
| 2 | 写路径 / 红线 | **Pass** | T-03 写前 403 · audit `execute.failed` · 无 silent no-op |
| 3 | AC 可测 | **Pass** | `test_T03_execute_unconfigured_connector_returns_403[T-03]` 绿 |
| 4 | 无重复逻辑 | **Pass** | `assert_tenant_connector_configured` · `is_pack_entitled` 集中 store |
| 5 | 注释四要素 | **Pass** | registry · license · tenant_config_store · execution |
| 6 | 门禁顺序 | **Pass** | connector → license → graph → rule |
| 7 | Step1 / T-02 回归 | **Pass** | shadow + license 3 passed |
| 8 | import_boundaries | **Pass** | license → platform_registry |
| 9 | 静态质量 | **Pass** | ruff · pyright 0 errors |

## 范围边界

| 项 | 评估 |
|----|------|
| `DEFAULT_PACK_ID` 硬编码 | **备忘** — W7+ 从 relation 解析 |
| license fallback dict | **可接受** — 无 Session 单测路径 |
| W7 Step3–7 红测 | **预期** — 未在本 Step 实现 |

## 机械门禁

```bash
.venv/bin/pytest src/tests/integration/test_connector_t03_w7.py -k 'T-03' -v   # 1 passed
.venv/bin/pytest src/tests/integration/test_shadow_w7.py src/tests/integration/test_license_t02_w6.py src/tests/integration/test_license_w6_step1.py -q  # 3 passed
.venv/bin/python scripts/check_static_quality.py                              # OK
.venv/bin/python scripts/gate_cli.py step --step 2 -k 'T-03'                 # 待执行
```

联动链：`step-stop-0950-step2.md` → `test-1750-step2-regression.md` → 本文件

## 结论（必填 · gate 检查）

结论：通过

阻断理由（若有）：无

## 建议

1. Step3：Package export（P-01）。
2. 可选：`assert_pack_licensed` 统一要求 Session，逐步移除 fallback dict。
