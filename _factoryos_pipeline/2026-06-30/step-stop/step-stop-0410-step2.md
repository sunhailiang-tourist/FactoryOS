# Step 停机：Step 2 — POST `/v1/agent/plan` + H-01

- **plan**：`_factoryos_pipeline/2026-06-30/plan/plan-0330-w5-agent-harness.md`
- **时间**：2026-06-30

## 1. Step 标识

Step 2 — POST `/v1/agent/plan` · H-01（plan 阶段不写 Legacy）

## 2. 改动文件

| 路径 | 变更 |
|------|------|
| `src/server/api/modules/agent/` | 新增 agent 域（README · controllers · routers） |
| `src/server/api/router/v1/registry.py` | 登记 `agent.get_routers` |

## 3. AC / 接口

| AC ID | 接口 | 结果 |
|-------|------|------|
| H-01 | POST `/v1/agent/plan` | ✅ pytest 绿 |

## 4. 架构要点

| 项 | 处理 |
|----|------|
| Graph/Rule 门禁 | API 层 `assert_graph_executable` + `find_frozen_ruleset_id` 后注入内核 |
| Legacy 写 | plan 阶段 `mock_legacy` 写计数不变（R-11） |
| import 边界 | 内核仍仅 `shared_contracts` |

## 5. 十项自检

| # | 项 | 结果 |
|---|-----|------|
| 1 | 分层/写路径 | Pass — 无 execution · 无 Legacy |
| 2 | 响应契约 | Pass — DslPlan JSON |
| 3 | 鉴权/租户 | Pass — tenant_id 透传 |
| 4 | 红线 R01/R11 | Pass — 仅 DslPlan |
| 5 | Schema | Pass — OpenAPI 对齐 |
| 6 | 输入校验 | Pass — Pydantic AgentPlanBody |
| 7 | Shadow | N/A |
| 8 | 幂等 | N/A（Step2） |
| 9 | 静态 | Pass |
| 10 | 注释 | Pass |

## 6. Harness 结果

```bash
uv run pytest src/tests/integration/test_harness_w5.py -k 'H-01' -q
uv run python scripts/check_router_registry.py
```

## 7. Verify

- 口令：`【Verify回合】Step 2`

## 8. 等待

Test 验收 → Verify → `gate step --step 2 -k 'H-01'` → **`可以继续`**
