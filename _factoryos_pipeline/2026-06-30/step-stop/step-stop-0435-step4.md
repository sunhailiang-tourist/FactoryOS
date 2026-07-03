# Step 停机：Step 4 — H-03 全链路 audit + OpenAPI 对账 + 回归

- **plan**：`_factoryos_pipeline/2026-06-30/plan/plan-0330-w5-agent-harness.md`
- **时间**：2026-06-30

## 1. Step 标识

Step 4 — H-03 audit 全链路 · OpenAPI 对账 · W1–W4 存量回归

## 2. 改动文件

| 路径 | 变更 |
|------|------|
| `src/tests/contract/test_openapi_contract.py` | W5 OpenAPI 路径对账（agent/harness） |
| `src/server/api/modules/README.md` | 域清单补 agent · harness |

## 3. AC / 接口

| AC ID | 接口 | 结果 |
|-------|------|------|
| H-03 | GET `/v1/audit/events`（exec_id · tenant） | ✅ pytest 绿 |
| OpenAPI | `/v1/agent/plan` · `/v1/harness/confirm` | ✅ contract 对账 |

## 4. 全链路 audit（H-03）

| 阶段 | event_type | plan_id |
|------|------------|---------|
| confirm | `harness.confirmed` | ✅ |
| execute dry_run | `execute.started` · `execute.simulated` | exec_id 过滤 |

## 5. 十项自检

| # | 项 | 结果 |
|---|-----|------|
| 1 | 分层/写路径 | Pass — 全链经 harness→execution |
| 2 | 响应契约 | Pass — OpenAPI DslPlan/ExecutionRecord |
| 3 | 鉴权/租户 | Pass |
| 4 | 红线 R01/R11 | Pass |
| 5 | Schema | Pass — check_openapi_schema_refs |
| 6 | 输入校验 | Pass |
| 7 | Shadow | Pass — dry_run simulated |
| 8 | 幂等 | Pass |
| 9 | 静态 | Pass |
| 10 | 注释 | Pass |

## 6. Harness 结果

```bash
uv run pytest src/tests/integration/test_harness_w5.py -k 'H-03' -q
uv run pytest src/tests/integration/test_harness_w5.py -q
uv run pytest src/tests -m 'not pending' -q
uv run python scripts/check_openapi_schema_refs.py
uv run python scripts/check_plan_spec.py --plan _factoryos_pipeline/2026-06-30/plan/plan-0330-w5-agent-harness.md
```

## 7. Verify

- 口令：`【Verify回合】Step 4`
- 全局：`./scripts/gate step --step 4 -k 'H-03'` → `./scripts/gate delivery`

## 8. 等待

Test 验收 → Verify → gate step 4 → W5 交付 summary
