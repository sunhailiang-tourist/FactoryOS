# mcp_gateway · MCP 网关

## 是什么

**MCP JSON-RPC** 入口：`tools/list`、`tools/call` → DslPlan（Y1 末 GA；W7 stub）。

## 主要功能

- 外部 Agent 工具发现与调用转 DSL
- 与 Harness / Rule 门禁对齐

## 不负责什么

- 直写 Legacy
- 替代 `apps/api` 主 REST

## 上下游

- **上游**：MCP 客户端、Integration Studio
- **下游**：`agent_orchestrator`、`execution_service`（经确认门）

## 相关文档

- MCP-Gateway 规格 · ADR-006
