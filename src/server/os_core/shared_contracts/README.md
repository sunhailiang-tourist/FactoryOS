# shared_contracts · 共享契约

## 是什么

全平台 **Pydantic 模型、JSON Schema 加载、错误码、DomainEvent** 的代码化包（**published 真源** = Contract Registry · ADR-008）。

## 主要功能

- 运行时加载：`platform_registry.contract_store`（优先）→ `contracts/schemas/*.schema.json` export 回退
- 跨模块 DTO、HTTP 请求/响应类型
- 错误码常量与事件信封（`errors.py` · `schema_loader.py` · `tenant_registry.py` · `outbox.py`）

## 不负责什么

- 业务规则、Graph 校验、DSL 执行
- 数据库 ORM 实体（各 service 自有，字段须与 Schema 一致）

## 上下游

- **上游**：所有 `os_core/*`、`server/api` import
- **下游**：无运行时依赖；被全栈消费

## 相关文档

- [`models/README.md`](./models/README.md) · [contracts/schemas/](../../../contracts/schemas/)
