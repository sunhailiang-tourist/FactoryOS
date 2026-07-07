# db · 数据库迁移域

## 是什么

PostgreSQL **Alembic 迁移** 与 ORM 模型落点；服务端持久化 schema 真源（非契约平面）。

## 子路径

| 路径 | 说明 |
|------|------|
| `migrations/` | Alembic env · versions |
| `migrations/versions/` | 版本化 migration 脚本 |

## 门禁

```bash
uv run alembic upgrade head
./scripts/gate pr
```

## 变更纪律

- 新 migration 文件 **不触发** 结构变更门禁；新 **顶层目录** 须用户确认
- 与 ADR-008 contract Registry 区分：业务表 vs 契约 artifact

## 相关文档

- [alembic.ini](../../../alembic.ini)
- [server/api/README.md](../api/README.md)
