# application · 应用创建与装配

> **定位**：FastAPI **应用工厂**；把 `config` 与 `router` 按固定顺序接到 app 实例上  
> **不负责**：定义 HTTP 端点、业务规则

## 是什么

`application/` 回答「进程启动时，如何 new 一个配置好的 FastAPI app」。  
`main.py` 只 export `app`；**装配逻辑全在这里**。

## 核心功能

| 文件 | 职责 |
|------|------|
| `factory.py` | `create_app()` · FastAPI 元数据 · 绑定 `config/lifespan` |
| `assemble.py` | `register_config(app)` → `register_routers(app)` 固定顺序 |

## 怎么用

```python
# 本地 / Uvicorn
from server.api.application.factory import app, create_app

# 测试可单独 create_app() 获得新实例
client = TestClient(create_app())
```

装配顺序（不可颠倒）：

```text
create_app()
  → assemble(app)
       ├─ config.registry.register_config(app)   # 先横切
       └─ router.registry.register_routers(app)    # 后路由
```

## 承载业务

- **无直接业务**：纯工程装配层  
- **业务影响**：装配顺序错误会导致 middleware 不生效或路由未挂载

## 上下游

- **上游**：`main.py`（Uvicorn import）  
- **下游**：`config/` · `router/`  
- **并行**：`config/lifespan` 在 factory 绑定时引用，startup 调 `os_core.registry.init_kernel()`

## 门禁

```bash
uv run pytest src/tests/workflow/test_api_health.py -q
grep -L include_router src/server/api/main.py   # main 不得挂路由
```

## 关联文档

- [api/README.md](../README.md) · [config/README.md](../config/README.md) · [router/README.md](../router/README.md)
