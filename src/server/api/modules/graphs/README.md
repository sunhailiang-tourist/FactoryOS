# graphs · 业务图谱 HTTP 域

> **OpenAPI**：`/v1/graphs/*` · AC **G-01～G-08**  
> **内核**：`os_core/graph_service`

## 是什么

**业务图谱（Business Graph）** 的 HTTP 适配层：创建 draft、版本演进、submit、freeze、clone。  
图谱描述工厂流程节点与边；freeze 后 checksum 锁定，供执行链引用。

## 核心功能

| 端点 | 业务含义 |
|------|----------|
| `POST /v1/graphs` | 创建 draft 图谱（G-01） |
| `GET /v1/graphs/{graphId}` | 读指定版本 |
| `PUT .../versions/{version}` | 更新 draft/in_review（G-02/G-06 负向） |
| `POST .../submit` | draft → in_review（G-04） |
| `POST .../freeze` | 冻结版本 · checksum（G-05） |
| `POST .../clone` | 克隆新版本 draft（G-07） |

## 怎么用

```bash
# 创建（示例，body 见 BusinessGraph schema）
curl -X POST http://127.0.0.1:8000/v1/graphs -H 'Content-Type: application/json' -d @graph.json
```

开发扩展：

- **Controller**：`controllers/graphs.py` — 薄路由，Depends `get_db_session`  
- **Application**：`application/` — 可选 DTO 编排  
- **业务真源**：`os_core.graph_service.*` — **禁止** 在 controller 写 freeze/checksum 规则

## 承载业务

- **L0 图谱平面**：Studio 编辑 · Agent 读图 · Execution 引用 graph_id+version  
- **红线**：Agent 不得自动 freeze（R-09 · ADR-008）

## 上下游

- **上游**：Integration Studio · web-admin · Agent orchestrator（读）  
- **下游**：`os_core/graph_service` → `graphs` 表 · `audit_service`（生命周期事件）  
- **契约**：`contracts/schemas/业务图谱.schema.json`

## 门禁

```bash
uv run pytest src/tests/integration/test_graph_w3.py -q
./scripts/gate step --step 2 -k 'G-01'
```

## 关联文档

- [业务图谱规格](../../../docs/文档/规格说明/业务图谱.md)  
- [os_core/graph_service/README.md](../../../os_core/graph_service/README.md)
