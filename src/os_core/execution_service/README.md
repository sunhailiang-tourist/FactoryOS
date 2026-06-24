# execution_service · 执行与写门禁

## 是什么

**唯一** 经 Connector **写 Legacy** 的路径：DSL 执行、Saga、Compensator、Shadow、幂等。

## 主要功能

- DSL 解释执行、ExecutionRecord 落库
- Connector 调度、idempotency、connector_trace
- Revert / 对账钩子

## 不负责什么

- Graph freeze 逻辑（`graph_service`）
- Agent 规划（`agent_orchestrator`）

## 上下游

- **上游**：`apps/api`、`mcp_gateway`、Harness 确认后的计划
- **下游**：`connector_sdk`、`audit_service`、PostgreSQL

## 相关文档

- ADR-002 R-02、R-05、R-06 · ExecutionRecord v0.2
