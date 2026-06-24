# graph_service · 图版本与冻结

## 是什么

**Graph** 版本管理、freeze、checksum、Override 合并；L2 写前门禁状态源。

## 主要功能

- Graph CRUD、版本链、frozen 状态
- Override 与租户配置合并（无 `if tenant_id` 分支）

## 不负责什么

- 写 Legacy（R-02）
- Rule 判定（`rule_engine`）

## 上下游

- **上游**：`apps/api` `/v1/graphs/*`、`agent_orchestrator` 读图
- **下游**：PostgreSQL `graphs` 表；`execution_service` 读 frozen 状态

## 相关文档

- ADR-002 R-03、R-08 · Graph 规格
