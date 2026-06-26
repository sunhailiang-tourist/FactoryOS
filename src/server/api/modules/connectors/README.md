# connectors · Connector 健康 HTTP 域

> **OpenAPI**：`/v1/connectors/{packId}/health` · AC **C-01**  
> **内核**：`os_core/connector_sdk/health`

## 是什么

**Connector Pack 连通性探针** 的 HTTP 薄层。  
实施/integration 阶段验证 Pack 是否可达；W1～W4 为 mock health，生产接 Blueprint Runtime。

## 核心功能

| 端点 | 业务含义 |
|------|----------|
| `GET /v1/connectors/{packId}/health?tenant_id=` | 返回 status · latency_ms · pack_id |

## 怎么用

```bash
curl -s 'http://127.0.0.1:8000/v1/connectors/conn-erp-kingdee-write/health?tenant_id=default'
```

```python
# controller 仅委托公开面
from os_core.connector_sdk.health import check_connector_health
```

## 承载业务

- **GIP 集成验证**：Studio「连通测试」· 监控告警  
- **不含**：Legacy 读写规则（在 connector_sdk runtime · execution_service）

## 上下游

- **上游**：Integration Studio · 实施顾问 · 监控  
- **下游**：`connector_sdk.health` → Pack Registry / mock Legacy  
- **Pack 定义**：`integration/packs` export · DB `pack_registry`

## 门禁

```bash
uv run pytest src/tests/integration/test_connector_c01.py -q
./scripts/gate step --step 4 -k 'C-01'
```

## 关联文档

- [Connector-Blueprint 规格](../../../docs/文档/规格说明/Connector-Blueprint规格.md)  
- [integration/registry.py](../../../../integration/registry.py)
