# modules · 业务域 HTTP 模块

> **定位**：OpenAPI `/v1/*` 各域的 **HTTP 适配实现**（Controller · Schema · Application）  
> **真源路由登记**：[router/v1/registry.py](../router/v1/registry.py)

本目录承载 **对外 REST 业务面**；业务规则在 `os_core/`，此处只做入参校验、Depends、DTO 转换与薄编排。

## 域清单

| 模块 | 路径前缀 | 承载业务 | README |
|------|----------|----------|--------|
| **probes** | `/health` · `/ready` | 进程/K8s 探针（非 OpenAPI 正式域） | [probes/README.md](./probes/README.md) |
| **graphs** | `/v1/graphs/*` | 业务图谱版本生命周期（draft→freeze） | [graphs/README.md](./graphs/README.md) |
| **execution** | `/v1/execute` · `/v1/executions/*` | L2 DSL 执行、回滚、执行证据 | [execution/README.md](./execution/README.md) |
| **registry** | `/v1/registry/*` | Platform Registry 读 + 变更请求人审 | [registry/README.md](./registry/README.md) |
| **connectors** | `/v1/connectors/*` | Connector Pack 健康检查 | [connectors/README.md](./connectors/README.md) |
| **rulesets** | `/v1/rulesets/*` | 规则集 CRUD · evaluate 授权 | [rulesets/README.md](./rulesets/README.md) |
| **dsl** | `/v1/dsl/registry` | CMV 动词注册表只读 | [dsl/README.md](./dsl/README.md) |
| **audit** | `/v1/audit/events` | append-only 审计事件查询 | [audit/README.md](./audit/README.md) |
| **agent** | `/v1/agent/plan` | 意图 → DslPlan（H-01 · 不写 Legacy） | [agent/README.md](./agent/README.md) |
| **harness** | `/v1/harness/confirm` | Harness 确认门 → Rule → Execute（H-02） | [harness/README.md](./harness/README.md) |

## 标准目录结构

```text
modules/<域>/
  controllers/    # HTTP handler · APIRouter
  schemas/        # OpenAPI DTO（与 os_core 领域模型分离）
  application/    # 薄编排（复杂域 mandatory；只读域可选）
  routers.py      # get_routers() → 供 router/v1 登记
```

## 调用链

```text
Client → router/v1 → modules/<域>/controllers → [application] → os_core/*/service → store
```

## 新增域纪律

1. 新建 `modules/<域>/` 并按上表结构落目录  
2. 实现 `routers.py` 的 `get_routers()`  
3. 在 [router/v1/registry.py](../router/v1/registry.py) 的 `ROUTER_PROVIDERS` 登记  
4. 对齐 `contracts/openapi/` · 补 integration/workflow pytest  
5. **禁止** 在 `main.py` 或 controller 内写业务规则

## 门禁

```bash
./scripts/check_router_registry.py
uv run pytest src/tests/integration/ -q
./scripts/harness --tier full
```

## 上下游

- **上游**：`router/v1/registry.py` · web-admin / h5-worker / 第三方 HTTP 客户端  
- **下游**：`os_core/*` · PostgreSQL · Platform Registry

## 关联文档

- [api/README.md](../README.md) · [router/README.md](../router/README.md)  
- [contracts/openapi/](../../../contracts/openapi/) · [os_core/registry.py](../../os_core/registry.py)
