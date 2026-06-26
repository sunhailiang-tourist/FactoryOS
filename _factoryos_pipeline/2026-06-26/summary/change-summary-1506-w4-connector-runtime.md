# PR 变更摘要：W4 — connector_sdk/runtime · L2 真写 · Revert

- **plan**：`_factoryos_pipeline/2026-06-26/plan/plan-1339-w4-connector-runtime.md`
- **日期**：2026-06-26

## 标题建议

`feat(w4): blueprint runtime · L2 governed write · revert HTTP`

## 主要改动

| 模块 | 说明 |
|------|------|
| `connector_sdk/registry.py` | catalog 加载 · blueprint 校验（B-01/B-04） |
| `connector_sdk/runtime/` | execute_op · entity · mapping（B-02/B-03 · C-02～C-04） |
| `conn-mock.yaml` | ConnectorBlueprint 样例 |
| `mock_legacy.py` | entity store · restore（C/E 验收） |
| `execution_service` | L2 真写接线 · snapshot · `revert_execution`（E-02/E-04） |
| `routes/execute.py` | `POST /v1/execute/{execId}/revert` |
| integration 测试 | 11 项 W4 + W1–W3 回归 |

## AC

B-01～B-04 · C-02～C-04 · E-02 · E-03 · E-04 · E-05 · E-09 **PASS**；52 P0 其余 **16 pending**。

## 测试

`pytest … -m 'not pending'` → **60 passed** · `gate step` 1–4 OK

Test 终轮：`test-1506-w4-final-regression.md`
