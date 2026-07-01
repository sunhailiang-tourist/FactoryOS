# mcp_gateway · MCP 网关

## 是什么

**MCP JSON-RPC** 入口：`tools/list`、`tools/call` → DslPlan（Y1 内部 GA · W7/W8）。

## 主要功能

- `tools/list`：tenant 已授权 CMV 子集（M-01）
- `tools/call` → `agent_orchestrator` → DslPlan，确认前不写 Legacy（M-02）
- `params._meta.traceparent` → DslPlan.trace_id + audit `mcp.tools_call`（M-03 · SEP-414）
- 与 Harness / Graph / Rule / License 门禁对齐

## 不负责什么

- 直写 Legacy（须经 harness → execution）
- OAuth 2.1 对外鉴权（Y2）
- 替代 `server/api` 主 REST

## 上下游

- **上游**：MCP 客户端 · Integration Studio
- **下游**：`agent_orchestrator` · `graph_service` · `rule_engine` · `audit_service` · `tenant_service`（shadow）

## 相关文档

- MCP-Gateway 规格 §4.1 · ADR-006 · 可观测性规范

## 验收盘

```bash
pytest src/tests/integration/test_mcp_w7.py src/tests/integration/test_mcp_w8.py -v
pytest src/tests/contract/test_trace_context.py -v
```
