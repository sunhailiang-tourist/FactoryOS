# probes · 进程探针

> **OpenAPI**：非正式域（运维/K8s 专用）  
> **路由登记**：`router/v1/registry.py` → `probes.get_routers`

## 是什么

进程 **存活与就绪** 探针；不承载制造业务，仅供负载均衡、CI、gate workflow 使用。

## 核心功能

| 端点 | 方法 | 说明 |
|------|------|------|
| `/health` | GET | 进程存活（W1 Step1 AC） |
| `/ready` | GET | 就绪（S0 与 health 等价，预留 DB/Registry 检查） |

## 怎么用

```bash
curl -s http://127.0.0.1:8000/health
curl -s http://127.0.0.1:8000/ready
```

代码入口：`controllers/health.py` · 聚合在 `routers.py`。

## 承载业务

- **运维面**：K8s liveness/readiness、本地开发冒烟  
- **不含**：租户鉴权、OpenAPI 契约域

## 上下游

- **上游**：SLB · K8s · `./scripts/gate` workflow 测试  
- **下游**：无 os_core 调用（纯 HTTP 200 JSON）

## 门禁

```bash
uv run pytest src/tests/workflow/test_api_health.py -q
```

## 关联文档

- [modules/README.md](../README.md)
