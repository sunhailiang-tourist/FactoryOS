# 平台化变革 · P1 落盘摘要（2026-06-26）

> **接续**：[summary-platform-restructure-p0.md](./summary-platform-restructure-p0.md)

## P1 已完成

| 类别 | 内容 |
|------|------|
| **物理搬迁** | `src/os_core` → `src/server/os_core` · `src/apps/api` → `src/server/api` · alembic → `src/server/db/migrations` |
| **客户端** | `src/apps/web-admin` · `src/apps/h5-worker` |
| **包名** | `server.api` → `server.api` |
| **路径工具** | `repo_paths.py`（搬迁后稳定解析） |
| **工程** | `pyproject.toml` · `alembic.ini` · scripts 边界/冗余/harness/static |
| **Hook** | `protect-paths.py` 新路径前缀 |
| **文档** | `server/README` · `src/README` · `MODULE-MAP` · `FactoryOS完整架构设计` 三平面 |

## 验收

```bash
uv run pytest src/tests/ -m 'not pending' -q   # 61 passed
python scripts/check_import_boundaries.py      # OK
```

## 待续（SYNC 余量）

- `.cursor/factoryos/` 全量模板 · `INTEGRATION-CHAIN` · `DEV-GATES`
- `scripts/README.md` · `factoryos_cli.py` flows 路径
- Studio Registry HTTP API
- `docs/` P1/P2 规格批量对齐
