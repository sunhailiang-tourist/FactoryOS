# 测试用例与改动面：W8 Gate 0 收口 — M-03 traceparent failing tests

- **对照 plan**：`_factoryos_pipeline/2026-07-02/plan/plan-1000-w8-gate0-m03-trace.md`
- **命名**：`test-1333-w8-gate0-m03-trace.md`
- **目的**：**新增** · W8 Step1 M-03 红测 · Gate 0 唯一 pending AC 清零路径

## 1. 改动文件（Test Agent 本轮）

| 路径 | 变更 | 职责 |
|------|------|------|
| `src/tests/integration/test_mcp_w8.py` | 新增 | Step1 M-03 traceparent → plan + audit |
| `src/tests/ac/test_base001_registry.py` | Step1 末 Dev 改 | M-03 移出 pending（Test 不写） |

## 2. AC 用例

| ID | 标题 | 类型 | Step | 期望 |
|----|------|------|------|------|
| M-03 | SEP-414 `_meta.traceparent` | integration | 1 | plan.trace_id · audit correlation_id 一致 |
| M-01/M-02 | MCP 不回归 | integration | 1 | 复跑 `test_mcp_w7.py` |
| 存量 W1～W7 | 回归 | Step1–2 | `-m 'not pending'` → 108 绿 |

## 3. Harness（Step 停机验收盘）

```bash
./scripts/gate step --step 1 -k 'M-03'
./scripts/gate step --step 2   # Gate 0 交付仪式
./scripts/gate delivery        # 108 passed · pending 清零
./scripts/gate pr
```

## 4. 标准测试用例

| ID | 标题 | 前置 | 步骤摘要 | 期望 |
|----|------|------|----------|------|
| M-03 | traceparent | frozen graph | tools/call + `_meta.traceparent` | trace_id=`0af7651916cd43dd8448eb211c80319c` |
| M-03 | no meta | frozen graph | tools/call 无 `_meta` | DslPlan 正常 · trace_id 空 |
| M-01 | list | default | POST /mcp/v1/default tools/list | tools≥1 |
| M-02 | call | frozen graph | tools/call 无 trace | Legacy 写 0 |

**traceparent 示例**（MCP-Gateway 规格）：

```json
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "GOVERNED_WRITE",
    "arguments": {
      "tenant_id": "default",
      "graph_id": "<frozen>",
      "graph_version": "v1.0.0",
      "intent": "report work order wo-m03 completed qty 1"
    },
    "_meta": {
      "traceparent": "00-0af7651916cd43dd8448eb211c80319c-00f067aa0ba902b7-01"
    }
  }
}
```

## 5. 与 plan 核对

| 项 | 结论 |
|----|------|
| plan 路径 | `plan-1000-w8-gate0-m03-trace.md` ✓ |
| Step 范围 | 2 Step · 唯一 pending **M-03** ✓ |
| Dev 落位 | `trace_context.py` · `mcp_gateway` · `create_plan(trace_id)` · audit ✓ |
| 不在 W8 | 真实 ERP · OAuth · H-04/H-05 ✓ |
| invalid traceparent | plan 定：忽略 · plan 仍产出（可选 Step1 负向） |

## Gate A–G 摘要

| Gate | 结论 |
|------|------|
| A 复盘 | W7 107 passed · 唯一 pending M-03 · MCP M-01/M-02 已绿 |
| B 目的 | **新增** — M-03 failing test 驱动 Gate 0 收口 |
| C 协作 | plan Step1 模块/接口/AC 对齐 · 触及 mcp_gateway + audit + DslPlan schema |
| D 质量 | Step1 验收须评估 trace 落位 · schema 同步 |
| E 接口 | 见下方分区 |
| F 字段 | DslPlan 增可选 `trace_id` · audit `correlation_id`/`plan_id` 关联 |
| G 命名 | `test-1333` = 落盘当下 HHmm |

## 📦 本次新增/调整接口（测）

```json
POST /mcp/v1/{tenantId}
{
  "jsonrpc": "2.0",
  "id": 3,
  "method": "tools/call",
  "params": {
    "name": "GOVERNED_WRITE",
    "arguments": {
      "tenant_id": "default",
      "graph_id": "graph-xxx",
      "graph_version": "v1.0.0",
      "intent": "report work order wo-m03 completed qty 1"
    },
    "_meta": {
      "traceparent": "00-0af7651916cd43dd8448eb211c80319c-00f067aa0ba902b7-01"
    }
  }
}
```

**期望 DslPlan 出参（摘要）**：

```json
{
  "plan_id": "<uuid>",
  "tenant_id": "default",
  "graph_id": "graph-xxx",
  "graph_version": "v1.0.0",
  "source": "mcp",
  "trace_id": "0af7651916cd43dd8448eb211c80319c",
  "steps": [{ "verb": "GOVERNED_WRITE", "params": {} }]
}
```

```json
GET /v1/audit/events?tenant_id=default&event_type=mcp.tools_call
[
  {
    "event_type": "mcp.tools_call",
    "plan_id": "<same plan_id>",
    "correlation_id": "0af7651916cd43dd8448eb211c80319c"
  }
]
```

## 🔁 本次需求涉及到的接口（字段调整）

- `DslPlan.schema.json`：新增可选 `trace_id`（32 hex · W3C trace 段）
- `POST /mcp/v1/{tenantId}`：`params._meta.traceparent` 已有 OpenAPI 描述 · 行为待实现
- `GET /v1/audit/events`：只读 · 断言 `event_type=mcp.tools_call` + `correlation_id`

## 红测证据

```bash
uv run pytest src/tests/integration/test_mcp_w8.py -v
# 预期：test_M03_mcp_tools_call_propagates_traceparent_to_plan_and_audit FAIL（无 trace_id · 无 audit）
# test_M03_tools_call_without_meta_behaves_like_w7 PASS（W7 行为已满足）
```

## 结论

Test-plan 就绪 → `./scripts/gate test` → Dev **`可以开始`** Step 1（M-03）
