# registry · Platform Registry HTTP 域

> **OpenAPI**：`/v1/registry/*` · **ADR-008** 配置与契约平面 DB 化  
> **内核**：`os_core/platform_registry`

## 是什么

**Platform Registry** 的 HTTP 读面 + **变更请求人审写路径**。  
租户/Pack/Contract/Relation 真源在 PostgreSQL Registry，本模块不做 Git YAML 日常编辑。

## 核心功能

### 只读（Studio · 集成实施）

| 端点 | 业务含义 |
|------|----------|
| `GET /v1/registry/contract-set/active` | 当前 published contract_set |
| `GET /v1/registry/packs` | 已发布 Pack 列表 |
| `GET /v1/registry/packs/{packId}` | Blueprint JSON |
| `GET /v1/registry/tenants/{tenantId}/profile` | 租户 profile |
| `GET /v1/registry/tenants/{tenantId}/relations` | system_relations |
| `GET /v1/registry/health` | seed/contract_set 就绪探针 |

### 人审写路径（变更提案）

| 端点 | 业务含义 |
|------|----------|
| `POST /v1/registry/change-requests` | 提案 pending（不直接改 Registry） |
| `GET .../change-requests` | 列表 |
| `POST .../approve` · `.../reject` | 人审后落库（R-09：AI 不得自动 publish） |

## 怎么用

```bash
curl -s http://127.0.0.1:8000/v1/registry/health
curl -s http://127.0.0.1:8000/v1/registry/packs
```

Controller 分文件：

- `controllers/registry.py` — 只读  
- `controllers/registry_changes.py` — 变更请求

## 承载业务

- **配置枢纽**：Pack 认证 · 租户关系 · Contract publish  
- **Studio 链**：connect → discover → map → prove → freeze → export  
- **与 integration/**：export 镜像；日常编辑走 API+DB

## 上下游

- **上游**：web-admin Studio · CI seed · bootstrap  
- **下游**：`platform_registry/*_store` · PostgreSQL Registry 表（migration 004）  
- **契约镜像**：`contracts/` export（非编辑真源）

## 门禁

```bash
uv run pytest src/tests/integration/test_registry_adr008.py -q
uv run pytest src/tests/ac/test_base001_registry.py -q
```

## 关联文档

- [ADR-008](../../../docs/文档/架构/架构决策记录-008-配置与契约平面DB化.md)  
- [配置枢纽与关系模型](../../../docs/文档/架构/配置枢纽与关系模型.md)
