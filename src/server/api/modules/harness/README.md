# harness · Harness 确认门 HTTP 域

> **OpenAPI**：`POST /v1/harness/confirm` · AC **H-02 · H-03**  
> **编排**：`application/confirm_flow.py` → `execution_service`（确认后唯一写路径）

## 是什么

**Harness 确认门** HTTP 入口：`confirmed=true` → Rule → Execute；`false` → 拒绝 + audit。

## 核心功能

| 端点 | 业务含义 |
|------|----------|
| `POST /v1/harness/confirm` | 读 plan_store → audit → execution（R-11） |

## 上下游

- **上游**：Agent plan · 操作员确认 UI  
- **下游**：`agent_orchestrator.get_plan` · `audit_service` · `execution_service`  
- **说明**：编排位于 API application 层（`agent_orchestrator` import 边界仅 shared_contracts）

## 门禁

```bash
uv run pytest src/tests/integration/test_harness_w5.py -k 'H-02' -q
./scripts/gate step --step 3 -k 'H-02'
```

## 关联文档

- [contracts/openapi/工厂操作系统-v1.1.yaml](../../../../contracts/openapi/工厂操作系统-v1.1.yaml)  
- ADR-002 R-11 Harness 确认门
