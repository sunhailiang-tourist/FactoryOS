# Step 停机：Step 4 — Revert HTTP + 闭环（E-04 · E-05 · B-04）

- **plan**：`_factoryos_pipeline/2026-06-26/plan/plan-1339-w4-connector-runtime.md`
- **时间**：2026-06-26 14:45

## 改动文件

| 路径 | 变更 |
|------|------|
| `execution_service/service.py` | `revert_execution` |
| `execution_service/store.py` | `update_execution_status` |
| `connector_sdk/mock_legacy.py` | `restore_entity` |
| `server/api/modules/*/controllers/execute.py` | `POST /v1/execute/{execId}/revert` |
| `server/api/modules/*/controllers/executions.py` | `GET /v1/executions/{execId}` |

## AC 结果

| AC | 结果 |
|----|------|
| E-04 | **PASS** — revert · Legacy 恢复 before_snapshot |
| E-05 | **PASS** — 重复 revert → 409 |
| B-04 | **PASS** — registry L2 无 revert 校验 |
| E-02/E-09 回归 | **PASS** |

```bash
uv run pytest src/tests/integration/test_execution_e02_e04_e05.py -v
uv run pytest src/tests/integration/test_connector_blueprint_w4.py -k B-04 -v
```

## W4 关单

四步 Dev 完成 → Test·终轮回归 → `gate delivery` → `可以提交`
