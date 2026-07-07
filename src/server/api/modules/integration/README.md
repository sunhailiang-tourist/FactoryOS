# modules/integration · Integration Studio HTTP

## 是什么

OpenAPI `/v1/integration/*` 薄路由域（Connect · Discover · Prove 等）。

## 功能

- POST `/v1/integration/connect/test` — Connector 连通测试（P-03）
- POST `/v1/integration/connect/register` — Studio Connect 落库（STU-02）
- POST `/v1/integration/discover` — CMV 候选发现（STU-02）
- POST `/v1/integration/blueprint/validate` — Blueprint 校验
- PUT `/v1/integration/mappings/{packId}` — 字段映射 · secrets_ref（STU-11）
- POST `/v1/integration/prove/run` — Shadow Prove（STU-03）

## 不负责什么

- base_url 解析逻辑（`connector_sdk.connect_test`）
- Legacy HTTP 真调用（W7+ mock）

## 上下游

- **上游**：Integration Studio Step 1
- **下游**：`os_core.connector_sdk.connect_test` · `studio_integration`

## 文档

- `contracts/openapi/工厂操作系统-v1.1.yaml` · IntegrationConnectReport
