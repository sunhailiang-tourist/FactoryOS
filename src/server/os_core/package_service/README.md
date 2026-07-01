# package_service · Implementation Package export/import

## 是什么

租户实施快照（Graph · RuleSet · Connector 配置）的内核真源，供 REST 与 MCP 共用。

## 主要功能

- `export_implementation_package` — POST `/v1/packages/export`（W7 Step3 P-01）
- import / override 应用（W7 Step4+）

## 不负责什么

- HTTP 路由（`server/api/modules/package`）
- Legacy 读写（`connector_sdk`）
- Graph/Rule CRUD（`graph_service` · `rule_engine`）

## 上下游

- **上游**：Integration Studio export 步 · 未来 MCP tools
- **下游**：`graph_service.store` · `rule_engine.store` · `platform_registry.tenant_config_store`

## 相关文档

- `contracts/schemas/ImplementationPackage.schema.json` · AC P-01～P-03
