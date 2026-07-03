# Verify 回合：W7 Step 4 — Package import + Override（P-02 · P-03）

> **plan**：`plan-0900-w7-gate0-gip-mcp.md` · **对照** `step-stop-1105-step4.md` · `test-0936-step4-regression.md`

- **step-stop**：`_factoryos_pipeline/2026-07-01/step-stop/step-stop-1105-step4.md`
- **Test 验收**：`_factoryos_pipeline/2026-07-01/test/test-0936-step4-regression.md`
- **对照 AC**：P-02 · P-03（harness `-k 'P-02'` / `-k 'P-03'`）

## 核对项

| # | 项 | 结果 | 证据 |
|---|-----|------|------|
| 1 | 未超 plan 4 范围 | **Pass** | import · overrides · connect/test；无 MCP Gateway HTTP |
| 2 | 写路径 / 红线 | **Pass** | import 写 Graph/Rule/relations · 非 Legacy 直写 |
| 3 | AC 可测 | **Pass** | `test_P02_*` · `test_P03_*` 各 1 passed |
| 4 | 无重复逻辑 | **Pass** | import 内核 · `resolve_pack_base_url` 集中 override 合并 |
| 5 | 注释四要素 | **Pass** | package · tenant · connect_test · integration controller |
| 6 | P-01 回归 | **Pass** | export 1 passed |
| 7 | Step1–2 回归 | **Pass** | Test 报告 shadow · T-03 绿 |
| 8 | import_boundaries · static | **Pass** | 矩阵绿 · ruff · pyright 0 errors |

## 范围边界

| 项 | 评估 |
|----|------|
| P-03 connect/test 允许 override 无 relation | **可接受** — Studio 预配置场景 |
| import 幂等跳过已存在 graph/ruleset | **Pass** — relations upsert |
| MCP Step5 红测 | **预期** — 未在本 Step 实现 |

## 机械门禁

```bash
.venv/bin/pytest src/tests/integration/test_package_w7.py -k 'P-02 or P-03' -v   # 2 passed
.venv/bin/python scripts/check_static_quality.py                                  # OK
.venv/bin/python scripts/gate_cli.py step --step 4 -k 'P-02'                   # 待执行
```

联动链：`step-stop-1105-step4.md` → `test-0936-step4-regression.md` → 本文件

## 结论（必填 · gate 检查）

结论：通过

阻断理由（若有）：无

## 建议

1. Step5：MCP Gateway（M-01/M-02）。
2. 可选：connect/test 失败路径统一 PlatformError 403 与 OpenAPI 错误体。
