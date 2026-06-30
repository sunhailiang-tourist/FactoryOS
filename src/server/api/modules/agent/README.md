# agent · Agent 计划 HTTP 域

> **OpenAPI**：`POST /v1/agent/plan` · AC **H-01**  
> **内核**：`os_core/agent_orchestrator`（仅产 DslPlan · 禁写 Legacy）

## 是什么

**Agent 薄 stub** 的 HTTP 入口：自然语言/结构化 **intent → DslPlan**，不执行、不写 Legacy（Harness 确认门 R-11）。

## 核心功能

| 端点 | 业务含义 |
|------|----------|
| `POST /v1/agent/plan` | Graph frozen + Rule 绑定校验 → `create_plan` → DslPlan |

## 上下游

- **上游**：web-admin · MCP · 第三方 HTTP 客户端  
- **下游**：`graph_service.assert_graph_executable` · `rule_engine.find_frozen_ruleset_id` · `agent_orchestrator.create_plan`  
- **不负责**：Harness confirm · execution · Legacy 写（Step3+）

## 门禁

```bash
uv run pytest src/tests/integration/test_harness_w5.py -k 'H-01' -q
./scripts/gate step --step 2 -k 'H-01'
```

## 关联文档

- [contracts/openapi/工厂操作系统-v1.1.yaml](../../../../contracts/openapi/工厂操作系统-v1.1.yaml)  
- [ADR-002 写路径与 Agent 禁写](../../../../docs/文档/架构/架构决策记录-002-写路径与Agent禁写.md)
