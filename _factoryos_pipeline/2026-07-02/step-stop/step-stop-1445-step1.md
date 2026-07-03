# Step 停机：Step 1 — MCP SEP-414 traceparent（M-03）

- **plan**：`_factoryos_pipeline/2026-07-02/plan/plan-1000-w8-gate0-m03-trace.md`
- **时间**：2026-07-02

## 1. Step 标识

Step 1 — MCP `_meta.traceparent` → DslPlan.trace_id · audit mcp.tools_call

## 2. 改动文件

| 路径 | 变更 |
|------|------|
| `shared_contracts/trace_context.py` | **新增** W3C traceparent → trace_id 解析 |
| `shared_contracts/models/dsl.py` | 可选 `trace_id` 字段 |
| `contracts/schemas/DslPlan.schema.json` | 可选 `trace_id` |
| `agent_orchestrator/service.py` | `create_plan(..., trace_id=None)` |
| `mcp_gateway/service.py` | 提取 `_meta` · audit append |
| `api/modules/mcp/controllers/mcp.py` | `session.commit()` 落 audit |
| `scripts/check_import_boundaries.py` | mcp_gateway 允许 import audit_service |
| `tests/ac/test_base001_registry.py` | M-03 移出 pending |

## 3. AC / 接口

| AC ID | 接口 | 结果 |
|-------|------|------|
| M-03 | POST `/mcp/v1/{tenantId}` tools/call + `_meta` | ✅ plan.trace_id · audit correlation_id |
| M-03-no-meta | 无 `_meta` | ✅ trace_id 空 · 与 W7 一致 |
| M-01/M-02 | 回归 `test_mcp_w7.py` | ✅ 2 passed |

## 4. 十项自检

| # | 项 | 结果 |
|---|-----|------|
| 1 | 分层/写路径 | Pass — api 薄；audit commit 在 controller |
| 2 | 响应契约 | Pass — DslPlan.schema 同步 trace_id |
| 3 | 鉴权/租户 | Pass — 未改 tenant 隔离 |
| 4 | 红线 | Pass — 无 Legacy 写；M-02 回归绿 |
| 5 | Schema | Pass — contract test DslPlan 绿 |
| 6 | 输入校验 | Pass — invalid traceparent 忽略 |
| 7 | Shadow | N/A |
| 8 | 幂等/补偿 | N/A |
| 9 | 静态检查 | Pass — import_boundaries OK |
| 10 | 注释 | Pass — 新文件/函数中文头 |

## 5. Harness 结果

```bash
uv run pytest src/tests/integration/test_mcp_w8.py -v
uv run pytest -q
```

```text
test_mcp_w8.py : 2 passed
full suite    : 109 passed, 1 skipped
gate step     : 待 Test/Verify 落盘后复跑
```

## 6. 最短验证路径

```bash
uv run pytest src/tests/integration/test_mcp_w8.py -k M-03 -v
```

## 7. Verify

- 口令：`【Verify回合】Step 1`

## 8. 等待

Test Step 1 验收 → Verify → `./scripts/gate step --step 1 -k 'M-03'` → **`可以继续`** Step 2
