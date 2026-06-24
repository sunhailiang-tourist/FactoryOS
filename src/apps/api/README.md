# apps/api · HTTP API

## 是什么

**FastAPI** 生产入口：路由、依赖注入、请求校验；Modular Monolith 唯一 deployable。

## 主要功能

- REST `/v1/*` 对齐 OpenAPI v1.1.1
- perception / harness 多模态与确认门路由
- 调用 `os_core` public API，**不含** 业务规则实现

## 不负责什么

- 在路由层重复 `os_core` 已有能力
- 绕过 Rule / Harness 写 Legacy

## 上下游

- **上游**：`web-admin`、`h5-worker`、第三方集成
- **下游**：`os_core/*`、PostgreSQL、Redis

## 本地开发

W1 起：`uv run uvicorn apps.api.main:app --reload`（路径待实现）。

## 相关文档

- `contracts/openapi/工厂操作系统-v1.1.yaml`
