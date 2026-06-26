# Step 停机：Step 1 — Blueprint catalog + registry（B-01）

- **plan**：`_factoryos_pipeline/2026-06-26/plan/plan-1339-w4-connector-runtime.md`
- **时间**：2026-06-26 14:05

## 1. Step 标识

Step 1 — `connector_sdk/registry` + `conn-mock` ConnectorBlueprint（B-01 · validate B-04）

## 2. 改动文件

| 路径 | 变更 |
|------|------|
| `src/server/os_core/connector_sdk/registry.py` | 新增 load_blueprint · validate_blueprint |
| `src/server/os_core/connector_sdk/runtime/` | 包骨架 + README |
| `src/integration/catalog/conn-mock.yaml` | 升级为 ConnectorBlueprint |
| `src/server/os_core/shared_contracts/errors.py` | BLUEPRINT_INVALID 等 |
| `src/server/os_core/connector_sdk/__init__.py` | 导出 registry |

## 3. AC / 接口

| AC ID | 证据 | 结果 |
|-------|------|------|
| B-01 | `test_B01_load_mock_blueprint_lists_governed_write` | **PASS** |
| B-04 | `test_B04_l2_op_without_revert_is_blueprint_invalid` | **PASS**（registry 校验） |

## 4. Harness

```bash
uv run pytest src/tests/integration/test_connector_blueprint_w4.py -k B-01 -v
# gate step 待 Test/Verify 落盘后
```

## 5. 最短验证

```bash
uv run python -c "from os_core.connector_sdk.registry import load_blueprint; b=load_blueprint(pack_id='conn-mock', tenant_id='default'); print([o['verb'] for o in b['spec']['ops']])"
```

## 6. 等待

【Test·Step 1 验收】→ Verify → `gate step --step 1 -k 'B-01'`
