# agent_orchestrator · Agent 编排

## 是什么

**LangGraph** Skill FSM：多模态意图 → **DSL 计划**（不执行写）。

## 主要功能

- LiteLLM 调用、工具路由
- 输出 DslPlan 供 Harness 确认

## 不负责什么

- **禁止** Connector.write、直写 DB（R-01）
- **禁止** 自动 freeze Graph（R-09）

## 上下游

- **上游**：`server/api` perception / agent 路由
- **下游**：`graph_service`（读）、Harness → `execution_service`

## 相关文档

- ADR-002 R-01、R-11 · Harness 规格
