# tenant_service · 租户设置真源

## 是什么

租户级 **shadow_mode** 等运行时开关的内核读/写；REST 与 MCP 共用同一 API。

## 主要功能

- `get_tenant_settings` / `update_tenant_settings`
- `resolve_shadow_mode` — execution / MCP tools/call 门禁

## 不负责什么

- HTTP 路由（`modules/tenant`）
- License / Package / Connector 配置（W7 Step2+）

## 上下游

- **上游**：`platform_registry.tenant_config_store` · `integration/tenants` seed
- **下游**：`execution_service` · 未来 `mcp_gateway`（读 shadow，不写 Legacy）

## 相关文档

- OpenAPI `TenantSettings` · T-01 · plan W7 Step1/Step5
