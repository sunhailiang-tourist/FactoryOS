# 平台化变革 · 一步到位落盘摘要（终稿 2026-06-26）

> **plan**：`plan-platform-restructure-db-first.md` · **ADR-008** Accepted

## 全量完成项

| 层 | 内容 |
|----|------|
| **DB** | 18 Registry 表 · `004_platform_registry` · bootstrap |
| **server/** | `os_core` · `api` · `db/migrations` · `edge-agent` |
| **apps/** | `web-admin` · `h5-worker` |
| **Registry 运行时** | loaders DB 优先 · export 回退 · `deps` bootstrap |
| **Registry API** | `/v1/registry/health` · packs · tenants · contract-set |
| **fixtures** | `tests/fixtures/integration` · `tests/fixtures/tenants` |
| **Studio** | `server/api/data/studio_flows.json` |
| **scripts** | boundaries · harness · deptry · factoryos_cli · static |
| **.cursor** | INDEX · PRE-DEV · DEV/TEST-GATES · HARNESS · ORM · hooks |
| **docs** | 配置枢纽 v2 · 完整架构 · SystemRelation schema · 索引 ADR-008 |

## 验收

```bash
uv run alembic upgrade head
uv run pytest src/tests/ -m 'not pending' -q
python scripts/check_import_boundaries.py
python scripts/check_harness.py --tier boundaries
```

## 刻意保留

- `src/integration/` · `contracts/` — **export/fixture 镜像**（bootstrap 源 + CI gate）
- `_factoryos_pipeline/*` 历史 step 文档 — 不 retro 改路径（审计留痕）
- OpenAPI 正式域 `/v1/registry/*` 待下一版 contracts export 同步

## 后续（产品化 · 非本次变革）

- Studio **Web UI** 页面接 Registry API（`src/apps/web-admin`）
- `import_export_jobs` 批量 air-gap 出入库
- `connector_instances` activate 完整链路

## 变革状态

**本次变革（ADR-008 架构整改）已关闭。**
