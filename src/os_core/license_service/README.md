# license_service · Pack 授权

## 是什么

Pack **授权**、租户 Override 生效域；未授权模块 403。

## 主要功能

- `licensed_packs` 校验、MODULE_NOT_LICENSED
- 与 `integration/tenants` 配置对齐

## 不负责什么

- 执行 DSL
- 计费与商务合同

## 上下游

- **上游**：`rule_engine`、`apps/api`
- **下游**：租户配置缓存 / DB

## 相关文档

- ADR-003 · 能力追溯矩阵
