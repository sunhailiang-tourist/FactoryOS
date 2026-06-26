"""FactoryOS 服务端（内核 + API + 迁移 + Edge Agent）。

作用：src/ 下运行时核心代码根。
业务关联：ADR-008 Platform Registry · Modular Monolith。
上游：pyproject pythonpath
下游：src/apps/web-admin · src/apps/h5-worker（UI 壳）
"""

## 目录

| 路径 | 职责 |
|------|------|
| `os_core/` | 内核（execution 唯一写路径 · platform_registry） |
| `api/` | FastAPI 薄路由（`server.api` 包） |
| `db/migrations/` | Alembic 迁移 |
| `edge-agent/` | 边缘 Agent（占位） |

## 启动

```bash
uv run uvicorn server.api.main:app --reload
```

## 迁移

```bash
uv run alembic upgrade head
```
