# modules/tenant · 租户设置 HTTP

## 是什么

OpenAPI `/v1/tenants/{tenantId}/settings` 薄路由域。

## 功能

- GET/PUT 租户 Shadow · write_approved 设置

## 不负责什么

- shadow 判定逻辑（`tenant_service.resolve_shadow_mode`）
- execution 内 simulated 编排（`execution_service`）
- MCP JSON-RPC（W7 Step5 · `modules/mcp`）

## 上下游

- **上游**：Integration Studio · Harness · 未来 MCP admin
- **下游**：`os_core.tenant_service`（与 MCP gateway 共用内核）

## 文档

- `contracts/openapi/工厂操作系统-v1.1.yaml` · TenantSettings
