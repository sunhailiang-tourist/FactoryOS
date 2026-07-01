# modules/integration · Integration Studio HTTP

## 是什么

OpenAPI `/v1/integration/*` 薄路由域（Connect · Discover · Prove 等）。

## 功能

- POST `/v1/integration/connect/test` — Connector 连通测试（P-03）

## 不负责什么

- base_url 解析逻辑（`connector_sdk.connect_test`）
- Legacy HTTP 真调用（W7+ mock）

## 上下游

- **上游**：Integration Studio Step 1
- **下游**：`os_core.connector_sdk.connect_test`

## 文档

- `contracts/openapi/工厂操作系统-v1.1.yaml` · IntegrationConnectReport
