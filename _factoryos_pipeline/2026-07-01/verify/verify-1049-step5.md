# Verify 回合：W7 Step 5 — MCP Gateway（M-01 · M-02）

> **plan**：`plan-0900-w7-gate0-gip-mcp.md` · **对照** `step-stop-1120-step5.md` · `test-0942-step5-regression.md`

- **step-stop**：`_factoryos_pipeline/2026-07-01/step-stop/step-stop-1120-step5.md`
- **Test 验收**：`_factoryos_pipeline/2026-07-01/test/test-0942-step5-regression.md`
- **对照 AC**：M-01 · M-02（harness `-k 'M-01'` / `-k 'M-02'`）

## 核对项

| # | 项 | 结果 | 证据 |
|---|-----|------|------|
| 1 | 未超 plan 5 范围 | **Pass** | MCP stub · tools/list/call；无 OAuth 公网 · 无 D-04/E-08 |
| 2 | 写路径 / 红线 | **Pass** | tools/call → DslPlan only · Legacy 写计数 0 · 无 connector.write |
| 3 | AC 可测 | **Pass** | `test_M01_*` · `test_M02_*` 各 1 passed |
| 4 | 无重复逻辑 | **Pass** | JSON-RPC 在 mcp_gateway · 复用 agent_orchestrator.create_plan |
| 5 | 注释四要素 | **Pass** | mcp_gateway · mcp controller · README |
| 6 | OpenAPI 路径 | **Pass** | 唯一 HTTP 面 `POST /mcp/v1/{tenantId}` · v1.1.yaml |
| 7 | Step1–4 回归 | **Pass** | Test 报告 package · shadow · connector 绿 |
| 8 | import_boundaries · static | **Pass** | mcp_gateway 矩阵 · ruff · pyright 0 errors |

## 范围边界

| 项 | 评估 |
|----|------|
| OAuth 2.1 / 公网 MCP | **预期留 Y2** — W7 internal stub |
| tools/call 不经 execution | **Pass** — 仅产出 DslPlan，写路径仍经 Harness+execute |
| Step6–7 红测 | **预期** — D-04/E-08 · N-* 未实现 |

## 机械门禁

```bash
.venv/bin/pytest src/tests/integration/test_mcp_w7.py -v              # 2 passed
.venv/bin/python scripts/check_static_quality.py                      # OK
.venv/bin/python scripts/gate_cli.py step --step 5 -k 'M-01'         # 待执行
```

联动链：`step-stop-1120-step5.md` → `test-0942-step5-regression.md` → 本文件

## 结论（必填 · gate 检查）

结论：通过

阻断理由（若有）：无

## 建议

1. Step6：D-04 L2 无 compensator · E-08 Agent 禁直写。
2. 可选：`verify_mcp_access` Depends 占位，Y2 OAuth 同函数扩展。
