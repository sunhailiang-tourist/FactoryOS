# src/server/db/migrations · 数据库迁移真源（ADR-008）

本目录为 **PostgreSQL / SQLite 表结构演进** 的机器执行真源；Platform Registry 表见 `004_platform_registry`。

| 路径 | 内容 |
|------|------|
| `env.py` | Alembic 运行环境 |
| `versions/` | revision 链 · 含 004 Platform Registry |
| `../../../alembic.ini` | `script_location = src/server/db/migrations` |

## 门禁

```bash
uv run alembic upgrade head
uv run pytest src/tests/integration/ -k 'S-01 or registry' -q
```

## 文档

- [ORM-MIGRATION-PRINCIPLE](../../../.cursor/factoryos/ORM-MIGRATION-PRINCIPLE.md)
- [ADR-008](../../../docs/文档/架构/架构决策记录-008-配置与契约平面DB化.md)
