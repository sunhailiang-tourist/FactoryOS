# Step 停机：Step 2 — Runtime read/write + mapping（B-02/B-03 · C-02～C-04）

- **plan**：`_factoryos_pipeline/2026-06-26/plan/plan-1339-w4-connector-runtime.md`
- **时间**：2026-06-26 14:20

## 改动文件

| 路径 | 变更 |
|------|------|
| `connector_sdk/mock_legacy.py` | entity store · get/update · reset_entity_store |
| `connector_sdk/runtime/execute.py` | execute_op · GOVERNED_WRITE |
| `connector_sdk/runtime/entity.py` | entity_get · entity_update |
| `connector_sdk/runtime/mapping.py` | validate_op_params · MAPPING_ERROR |

## AC 结果

| AC | 结果 |
|----|------|
| B-02 · B-03 | **PASS** |
| C-02 · C-03 · C-04 | **PASS** |

```bash
uv run pytest src/tests/integration/test_connector_blueprint_w4.py -k 'B-02 or B-03' -v
uv run pytest src/tests/integration/test_connector_runtime_w4.py -v
```

## 等待

【Test·Step 2 验收】→ Verify → `gate step --step 2 -k 'C-02'`
