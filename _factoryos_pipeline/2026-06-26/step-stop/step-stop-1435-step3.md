# Step 停机：Step 3 — execution L2 真写 + snapshot（E-02 · E-09）

- **plan**：`_factoryos_pipeline/2026-06-26/plan/plan-1339-w4-connector-runtime.md`
- **时间**：2026-06-26 14:35

## 改动文件

| 路径 | 变更 |
|------|------|
| `execution_service/service.py` | L2 真写 → `runtime.execute_op` · snapshot/legacy_refs |
| `execution_service/store.py` | 持久化 before/after/legacy_refs JSON |
| `connector_sdk/mock_legacy.py` | snapshot 含 entity_type/id · get_entity_snapshot |

## AC 结果

| AC | 结果 |
|----|------|
| E-02 | **PASS** — success + snapshots + legacy_refs[] |
| E-09 | **PASS** — evidence.execution 含 snapshots |
| E-06/07/01 回归 | **PASS** |

```bash
uv run pytest src/tests/integration/test_execution_e02_e04_e05.py -k 'E-02 or E-09' -v
uv run pytest src/tests/integration/test_execution_e06_e07.py test_execution_e01.py -q
```

## 等待

【Test·Step 3 验收】→ Verify → `gate step --step 3 -k 'E-02'`
