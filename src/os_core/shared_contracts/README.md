# shared_contracts · 共享契约

## 是什么

全平台 **Pydantic 模型、JSON Schema 加载、错误码、DomainEvent** 的单一真源包。

## 主要功能

- 对齐 `文档/数据结构/*.schema.json`
- 跨模块 DTO、HTTP 请求/响应类型
- 错误码常量与事件信封

## 不负责什么

- 业务规则、Graph 校验、DSL 执行
- 数据库 ORM 实体（各 service 自有，字段须与 Schema 一致）

## 上下游

- **上游**：所有 `os_core/*`、`apps/api` import
- **下游**：无运行时依赖；被全栈消费

## 相关文档

- [CMV 注册表](../文档/数据结构/CMV注册表.yaml) · OpenAPI v1.1.1
