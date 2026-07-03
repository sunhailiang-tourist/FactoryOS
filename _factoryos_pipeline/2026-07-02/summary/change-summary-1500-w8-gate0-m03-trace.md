# PR 变更摘要：W8 — Gate 0 收口（M-03 traceparent · core-v1.0.0）

- **plan**：`_factoryos_pipeline/2026-07-02/plan/plan-1000-w8-gate0-m03-trace.md`
- **日期**：2026-07-02
- **分支**：`dev_sunhailiang_core_260624`（W7 `f032aec` 已交付 · 同分支续开）

## 标题建议（PR title）

`feat(w8): Gate 0 closure — MCP M-03 traceparent · core-v1.0.0 ready`

## 变更背景（Why）

W7 达成 AC-BASE-001 **52 项 P0** 全绿，唯一遗留 **M-03**（MCP SEP-414 `_meta.traceparent`）defer 至 W8。本轮补齐 trace 传播，**108 pytest 全绿**，完成 Core 1.0 Gate 0 交付仪式。

## 主要改动（What）

| 模块 | 路径 | 说明 |
|------|------|------|
| trace_context | `shared_contracts/trace_context.py` | W3C traceparent → trace_id（M-03） |
| DslPlan | `models/dsl.py` + schema | 可选 `trace_id` |
| mcp_gateway | `service.py` | `_meta` 解析 · audit `mcp.tools_call` |
| mcp API | `modules/mcp/controllers/mcp.py` | `session.commit()` 持久化 audit |
| import_boundaries | `check_import_boundaries.py` | mcp_gateway 允许 audit_service |
| registry | `test_base001_registry.py` | M-03 pending 清零 |
| 测试 | `test_mcp_w8.py` | M-03 集成测 |

## AC 通过情况

| AC ID | Step | 结果 |
|-------|------|------|
| M-03 | 1 | **PASS** plan.trace_id · audit correlation_id |
| 52 P0 存量 | 2 回归 | **PASS** 108 passed |
| M-01/M-02 | 回归 | **PASS** |

## 业务口径确认

- **traceparent**：非法格式 **忽略**，仍产出 DslPlan（与 plan 口径一致）。
- **无 _meta**：trace_id 为空，行为与 W7 一致。
- **写路径**：MCP 仍只产 Plan + audit；不经 execution 写 Legacy。

## 测试结论

```bash
./scripts/gate step --step 1 -k 'M-03'
uv run pytest src/tests/ -q                    # 108 passed
./scripts/gate delivery
./scripts/gate pr
```

## 人工 tag（Gate 0 冻结）

```bash
git tag -a core-v1.0.0 -m "FactoryOS Core 1.0 — AC-BASE-001 Gate 0"
git push origin core-v1.0.0
```

## Summary（3 条，可贴 PR）

1. MCP SEP-414：`tools/call` 解析 `_meta.traceparent` → DslPlan.trace_id + audit `mcp.tools_call` correlation（M-03）。
2. DslPlan 契约增可选 trace_id；mcp_gateway import 边界扩展 audit_service。
3. W8 两步 gate · 终轮 **108 pytest 绿** · pending AC **0** → 可 tag **`core-v1.0.0`**。
