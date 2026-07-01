# modules/mcp · MCP JSON-RPC HTTP

## 是什么

OpenAPI `POST /mcp/v1/{tenantId}` 薄路由域。

## 功能

- tools/list — 已授权 CMV（M-01）
- tools/call — DslPlan（M-02）

## 不负责什么

- JSON-RPC 分发与 Graph/Rule 门禁（`mcp_gateway`）
- Legacy 写（`execution_service` · Harness 确认后）

## 上下游

- **上游**：MCP 客户端 · 治理型 Agent
- **下游**：`os_core.mcp_gateway`

## 文档

- `docs/文档/规格说明/MCP-Gateway规格.md`
