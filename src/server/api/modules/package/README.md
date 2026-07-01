# modules/package · Implementation Package HTTP

## 是什么

OpenAPI `/v1/packages/export` · `/v1/packages/import` 薄路由域。

## 功能

- POST export — 租户实施快照（P-01）
- POST import — Step4 P-02

## 不负责什么

- 快照聚合逻辑（`package_service`）
- Connector runtime（`connector_sdk`）

## 上下游

- **上游**：Integration Studio export/import 步
- **下游**：`os_core.package_service`（MCP Step5 复用内核）

## 文档

- `contracts/schemas/ImplementationPackage.schema.json`
