# Step 1 单步验收 · Test 硬性验收报告

- **对照 plan**：`_factoryos_pipeline/2026-07-02/plan/plan-1000-w8-gate0-m03-trace.md` · Step 1
- **命名**：`test-1341-step1-regression.md`
- **口令**：`【Test·Step 1 验收】`（对照 `step-stop-1445-step1.md`）

## 1. git diff 改动面（本 Step）

| 路径 | 变更 | plan 预期落位 | 实际落位 | 结论 |
|------|------|---------------|----------|------|
| `shared_contracts/trace_context.py` | **新增** traceparent 解析 | Step1 M-03 | ✅ | PASS |
| `shared_contracts/models/dsl.py` | 可选 `trace_id` | Step1 M-03 | ✅ | PASS |
| `contracts/schemas/DslPlan.schema.json` | 可选 `trace_id` | Step1 M-03 | ✅ | PASS |
| `agent_orchestrator/service.py` | `create_plan(..., trace_id=None)` | Step1 M-03 | ✅ | PASS |
| `mcp_gateway/service.py` | `_meta` · audit append | Step1 M-03 | ✅ | PASS |
| `api/modules/mcp/controllers/mcp.py` | `session.commit()` 落 audit | Step1 M-03 | ✅ | PASS |
| `scripts/check_import_boundaries.py` | mcp_gateway → audit_service | Step1 | ✅ | PASS |
| `tests/ac/test_base001_registry.py` | M-03 移出 pending | Step1 末 | ✅ | PASS |

## 2. 本 Step 硬性验收计划（执行记录）

| AC ID | 验收项 | pytest / 证据 | 结果 |
|-------|--------|---------------|------|
| M-03 | traceparent → plan.trace_id · audit correlation_id | `test_M03_*[M-03]` | **PASS** |
| M-03-no-meta | 无 `_meta` · trace_id 空 | `test_M03_*[M-03-no-meta]` | **PASS** |
| M-01/M-02 | W7 MCP 回归 | `test_mcp_w7.py` | **PASS** |
| pending 清零 | registry 无 M-03 pending | `test_base001_registry.py` | **PASS** (1 skipped) |
| import_boundaries | 矩阵 | `test_import_boundaries` | **PASS** |
| 存量 | `-m 'not pending'` | 109 passed | **PASS** |

```bash
uv run pytest src/tests/integration/test_mcp_w8.py -v                    # 2 passed
uv run pytest src/tests/integration/test_mcp_w7.py -q                      # 2 passed
uv run pytest src/tests/workflow/test_redlines_static.py::test_import_boundaries_script_passes -q  # 1 passed
uv run pytest src/tests/contract src/tests/workflow src/tests/integration -m 'not pending' -q
# 109 passed in 17.95s
```

## 3. 代码落位合理性

| 维度 | 检查 | 结论 |
|------|------|------|
| 分层 | trace 解析在 shared_contracts · gateway 编排 · API 仅 commit | ✅ |
| 写路径 | tools/call 仍只产 DslPlan · 无 Legacy 写 | ✅ M-02 回归绿 |
| 可观测 | audit `mcp.tools_call` · plan_id + correlation_id=trace_id | ✅ |
| invalid traceparent | 忽略 · plan 仍产出 | ✅ no-meta 用例绿 |
| import 边界 | mcp_gateway 新增 audit_service 已登记 | ✅ |

## 4. 已改动代码测试报告（本 Step）

| 用例ID | AC/接口 | 步骤 | 结果 |
|--------|---------|------|------|
| M-03 | POST `/mcp/v1/default` tools/call + `_meta` | trace_id 解析 | **PASS** |
| M-03 | GET `/v1/audit/events?event_type=mcp.tools_call` | plan_id 关联 | **PASS** |
| M-03-no-meta | tools/call 无 `_meta` | trace_id 空 | **PASS** |

**M-03 出参（HTTP · 摘要）**：

```json
{
  "result": {
    "plan_id": "<uuid>",
    "source": "mcp",
    "trace_id": "0af7651916cd43dd8448eb211c80319c"
  }
}
```

**audit 关联（摘要）**：

```json
{
  "event_type": "mcp.tools_call",
  "plan_id": "<same plan_id>",
  "correlation_id": "0af7651916cd43dd8448eb211c80319c"
}
```

## 5. 架构与代码质量评估（本 Step）

| 维度 | 评估 |
|------|------|
| 契约轨 | DslPlan.schema.json 与 Pydantic 同步 · contract 绿 |
| SEP-414 | trace_context 独立可测 · invalid 安全忽略 |
| 审计 | append-only · controller commit 符合 W2 模式 |
| Gate 0 | pending AC 清零 · 109 pytest 全绿 |

## 6. 结论

**结论：通过**

- Step 1 目标 **M-03 绿** · M-01/M-02 回归绿 · **存量 109/109 绿**
- 唯一 pending **M-03** 已移出 registry

**下一步**：**Verify 新会话** `【Verify回合】Step 1` → `./scripts/gate step --step 1 -k 'M-03'`
