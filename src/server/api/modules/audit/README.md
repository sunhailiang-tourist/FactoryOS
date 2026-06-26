# audit · 审计事件 HTTP 域

> **OpenAPI**：`GET /v1/audit/events` · AC **E-03**  
> **内核**：`os_core/audit_service`

## 是什么

**append-only 审计事件** 的只读查询面。  
记录谁在何时对哪条 execution/graph 做了什么；**禁止 UPDATE/DELETE**。

## 核心功能

| 端点 | 业务含义 |
|------|----------|
| `GET /v1/audit/events` | 按 tenant 分页查询；可选 exec_id · event_type · since |

查询参数：`tenant_id`（必填）· `exec_id` · `event_type` · `since` · `limit`。

## 怎么用

```bash
curl -s 'http://127.0.0.1:8000/v1/audit/events?tenant_id=default&limit=10'
```

写入 **不在此模块**：由 `execution_service` · `graph_service` 等内核 append。

## 承载业务

- **合规与追溯**：执行链 · 图谱变更 · 人审操作留痕  
- **多租户**：必须带 tenant_id 过滤（S1 RLS 双保险）

## 上下游

- **上游**：web-admin 审计页 · 对账 · 运维排查  
- **下游**：`audit_service.store.list_audit_events` → `audit_events` 表  
- **写入方**：execution · graph lifecycle · registry change approve

## 门禁

```bash
uv run pytest src/tests/integration/test_audit_e03.py -q
./scripts/gate step --step 2 -k 'E-03'
```

## 关联文档

- [AuditEvent.schema.json](../../../docs/文档/数据结构/AuditEvent.schema.json)  
- [os_core/audit_service/README.md](../../../os_core/audit_service/README.md)
