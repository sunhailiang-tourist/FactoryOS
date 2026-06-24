# audit_service · 审计

## 是什么

**append-only** 审计日志；所有写操作与门禁拒绝须可追溯。

## 主要功能

- AuditEvent 写入、查询 API（只增不改）
- 与 ExecutionRecord 关联

## 不负责什么

- 修改或删除历史审计
- 业务补偿（`execution_service`）

## 上下游

- **上游**：全模块写操作钩子、`rule_engine` 拒绝
- **下游**：PostgreSQL `audit_events`

## 相关文档

- ADR-002 R-06 · 可观测性规格
