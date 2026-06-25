# tests/integration · 集成与规模 AC  pytest

本目录为 **跨模块、数据库、Connector 连通性** 的集成验收；对照 AC S-*、C-* 与 W1 规模预埋表。

| 文件 | 覆盖 |
|------|------|
| `test_scale_s01_s04.py` | Alembic S-01～S-04：tenants / connector_instances / quotas / outbox |
| `test_connector_c01.py` | C-01：`GET /v1/connectors/{pack_id}/health` |
| `__init__.py` | 包标记 |

## 门禁

```bash
uv run pytest src/tests/integration/ -v
./scripts/gate step --step 3 -k 'S-01'
./scripts/gate step --step 4 -k 'C-01'
./scripts/gate delivery    # 终轮含本目录全量
```

## 变更纪律

| 改了 | 必做 |
|------|------|
| `alembic/versions/` | 更新或新增本目录用例；`-k S-*` 须绿 |
| `apps/api/routes/` · `connector_sdk/` | 更新 C-* 用例 |
| 新 AC 集成场景 | test-plan 落盘 · 命名 `test_<域>_<ac_id>` 或 `pytest -k` |

## 不负责什么

- OpenAPI/Schema 静态契约（见 `tests/contract/`）
- 红线与门禁脚本（见 `tests/workflow/`）
- 业务实现（只测行为，实现在 `os_core` / `apps`）

## 文档链接

- [tests/README.md](../README.md)
- [contracts/acceptance/](../../../contracts/acceptance/)
- [alembic/README.md](../../../alembic/README.md)
