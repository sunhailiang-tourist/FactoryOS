# execution · 执行与证据 HTTP 域

> **OpenAPI**：`/v1/execute` · `/v1/executions/*` · AC **E-02～E-09**  
> **内核**：`os_core/execution_service`（**唯一写 Legacy 路径**）

## 是什么

**L2 DSL 执行平面** 的 HTTP 入口：提交执行计划、真写/ dry_run、回滚、查状态与 **ExecutionEvidence**。  
执行前经 graph freeze + rule evaluate 门禁（内核编排）。

## 核心功能

| 端点 | 业务含义 |
|------|----------|
| `POST /v1/execute` | 提交 ExecuteRequest · 触发 DSL 链（E-02/E-03） |
| `POST /v1/execute/{execId}/revert` | Saga 回滚（E-04/E-05） |
| `GET /v1/executions/{execId}` | 查询执行状态 |
| `GET /v1/executions/{execId}/evidence` | 执行证据包（E-09） |

## 怎么用

```bash
curl -X POST http://127.0.0.1:8000/v1/execute \
  -H 'Content-Type: application/json' \
  -d '{"tenant_id":"default","verb":"WORK_REPORT",...}'
```

推荐后续在 `application/execute_flow.py` 集中：**DTO → 多步 os_core 编排**（graph→rule→execute），controller 保持薄。

## 承载业务

- **制造执行闭环**：报工、查工单、写 Legacy（经 connector_sdk）  
- **Harness 确认门**：执行前须 Rule allow · Graph frozen  
- **审计**：每次执行 append audit + execution_records

## 上下游

- **上游**：h5-worker · MCP Gateway · Agent 产出的 DslPlan · Harness confirm  
- **下游**：`execution_service` → `rule_engine` · `graph_service` · `connector_sdk` · `audit_service`  
- **数据**：`execution_records` · Legacy 经 ADR-002 唯一写路径

## 门禁

```bash
uv run pytest src/tests/integration/test_execution_e01.py -q
uv run pytest src/tests/integration/test_execution_e06_e07.py -q
./scripts/gate step --step 4 -k 'E-03'
```

## 关联文档

- [执行与回滚规格](../../../docs/文档/规格说明/执行与回滚.md)  
- [ADR-002 写路径](../../../docs/文档/架构/架构决策记录-002-写路径与Agent禁写.md)
