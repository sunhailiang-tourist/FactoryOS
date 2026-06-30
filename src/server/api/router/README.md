# router · HTTP 路由模块

> **定位**：全站 **HTTP 面第一站** · 路由注册唯一入口  
> **开发者**：新增/排查 API 从本目录开始

## 是什么

`router/` 统一管理「哪些 APIRouter 挂载到 app、以什么顺序」。  
域内 handler 实现在 `modules/*/controllers/`，**不在此写业务**。

## 核心功能

| 文件 | 职责 |
|------|------|
| `registry.py` | `register_routers(app)` — 全站唯一 `include_router` 入口 |
| `v1/registry.py` | `API_ROUTER_DOMAINS`（summary/problem/usage）→ `ROUTER_PROVIDERS` |
| `v1/mount.py` | v1 prefix/tags 策略（当前路径已含 `/v1`，多为 no-op） |
| `catalog.py` | 路由清单（治理 · harness 扩展） |

## 怎么用

**新增 HTTP 域：**

1. 在 `modules/<域>/` 实现 controller + `routers.py`  
2. 编辑 `v1/registry.py`，追加 `ApiRouterDomain(...)`（**须** summary · problem · usage）：

```python
ApiRouterDomain(
  name="my_domain",
  summary="…",
  problem="…",
  usage="POST /v1/…",
  provider=my_domain.get_routers,
),
```

3. 跑 `./scripts/check_router_registry.py` · `./scripts/check_registry_annotations.py`

**禁止** 在 `main.py` 或 `application/` 里 `include_router`。

## 承载业务

| 登记域 | OpenAPI 业务面 |
|--------|----------------|
| probes | 运维探针 |
| graphs | 业务图谱 |
| execution | 执行与证据 |
| registry | 配置平面 Registry |
| connectors | 集成连通性 |
| rulesets | 规则授权 |
| dsl | CMV 动词表 |
| audit | 审计只读 |

## 上下游

- **上游**：`application/assemble.py` 调用 `register_routers`  
- **下游**：`modules/*/routers.py` → `controllers/*.py`  
- **契约对齐**：`contracts/openapi/工厂操作系统-v1.1.yaml`

## 门禁

```bash
./scripts/check_router_registry.py
./scripts/harness --tier boundaries
uv run pytest src/tests/workflow/test_registry_harness.py -q
```

## 关联文档

- [modules/README.md](../modules/README.md) · [contracts/openapi/](../../../contracts/openapi/)
