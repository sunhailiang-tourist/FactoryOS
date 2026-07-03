# 平台化变革 · 落盘摘要（2026-06-26）

> **状态**：P0 已落盘 · pytest 61 passed  
> **plan**：`_factoryos_pipeline/plan/plan-platform-restructure-db-first.md`  
> **非 W5**：独立变革 initiative

## 已完成

| 类别 | 内容 |
|------|------|
| ADR | ADR-008 Accepted |
| DB | `src/server/db/migrations/versions/004_platform_registry.py`（18 表 + connector_instances 扩列） |
| 代码 | `src/server/os_core/platform_registry/`（contract/pack/tenant/snapshot stores + bootstrap） |
| Loader | `cmv_registry` · `schema_loader` · `connector_sdk.registry` → DB 优先 + export 回退 |
| 测试 | `conftest` bootstrap + `tests/fixtures/integration/catalog/` |
| 文档 | 配置枢纽 v2 · contracts/README · integration/README · server/README · docs/索引 ADR-008 |
| 策略 | UI-FIRST 真源链修订 |

## 待续（SYNC-SNAPSHOT 余量）

- `server/` 物理搬迁（`src/` → `server/` · `apps/` 客户端分离）
- scripts/ · .cursor/ 全量 76+ 文件 gate 路径同步
- Studio v0 Registry API
- `FactoryOS完整架构设计.md` 等 P1/P2 docs 批量对齐

## 验收

```bash
uv run alembic upgrade head
uv run pytest src/tests/ -m 'not pending' -q
```
