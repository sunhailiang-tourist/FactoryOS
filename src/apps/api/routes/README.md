# apps/api/routes · HTTP 路由分包

本目录为 **FastAPI 路由模块**；仅做路径绑定、参数校验与依赖注入，**不含**业务规则。

| 路径 | 内容 |
|------|------|
| `connectors.py` | `GET /v1/connectors/{pack_id}/health`（AC C-01） |
| `audit.py` | `GET /v1/audit/events`（E-03） |
| `execute.py` | `POST /v1/execute`（E-03/06/07） |
| `executions.py` | `GET /v1/executions/{execId}/evidence`（E-09） |
| `__init__.py` | 路由包标记 |

## 门禁

```bash
uv run pytest src/tests/workflow/test_api_health.py -q
uv run pytest src/tests/integration/ -k 'C-01' -q
./scripts/gate step --step 4 -k 'C-01'
```

## 变更纪律

| 改了 | 必做 |
|------|------|
| 新增路由文件 | 在 `apps/api/main.py` 注册 `include_router`；对齐 `contracts/openapi/` |
| 响应形状 | 使用 `shared_contracts` 类型；补 workflow 或 integration pytest |
| 业务逻辑 | **禁止**写在路由内；下沉 `os_core` 对应模块 public API |

## 上下游

- **上游**：`apps/api/main.py` · OpenAPI v1.1.1
- **下游**：`os_core/*` 公开面（如 `connector_sdk.health`）

## 文档链接

- [apps/api/README.md](../README.md)
- [contracts/openapi/](../../../contracts/openapi/)
