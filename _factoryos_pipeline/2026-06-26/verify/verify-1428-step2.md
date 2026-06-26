# Verify 回合：W4 Step 2 — Runtime read/write + mapping（B-02/B-03 · C-02～C-04）

> **plan**：`plan-1339-w4-connector-runtime.md` · **对照** `step-stop-1420-step2.md` · `test-1426-step2-regression.md`

- **step-stop**：`_factoryos_pipeline/2026-06-26/step-stop/step-stop-1420-step2.md`
- **Test 验收**：`_factoryos_pipeline/2026-06-26/test/test-1426-step2-regression.md`
- **对照 AC**：C-02（harness `-k 'C-02'`）

## 核对项

| # | 项 | 结果 | 证据 |
|---|-----|------|------|
| 1 | 未超 plan 范围 | **Pass** | `execute.py` · `entity.py` · `mapping.py` · `mock_legacy` 扩展；`execution_service` / revert HTTP 未改 |
| 2 | 写路径 / 红线 | **Pass** | Legacy 写经 `mock_legacy.update_entity`；内核测直调 runtime，非 Agent 旁路 |
| 3 | AC 可测 | **Pass** | B-02/B-03 各 1 绿；C-02/C-03/C-04 各 1 绿 |
| 4 | 无重复逻辑 | **Pass** | execute → entity → mock_legacy 链清晰；mapping 校验独立模块 |
| 5 | 注释四要素 | **Pass** | execute/entity/mapping/mock_legacy 文件头 + 函数说明齐全 |

## 范围边界（合理超前）

| 项 | 评估 |
|----|------|
| C-04 read-back 在 Step2 落地 | **可接受** — 与 `entity_update` + `mock_legacy` 同域；plan Step4 侧重 HTTP revert 闭环 |
| E-02/E-04/E-05/E-09 仍红（4 项） | **预期** — Step3–4 execution L2 真写 + revert HTTP |
| `legacy_refs` 为 dict 非数组 | **备忘** — Step3 接线 execution_service 时须对齐 OpenAPI schema |

## 机械门禁

```bash
.venv/bin/pytest src/tests/integration/test_connector_blueprint_w4.py -k 'B-02 or B-03' -v   # 2 passed
.venv/bin/pytest src/tests/integration/test_connector_runtime_w4.py -v                        # 3 passed
.venv/bin/python scripts/gate_cli.py step --step 2 -k 'C-02'                                # 待执行
```

联动链：`step-stop-1420-step2.md` → `test-1426-step2-regression.md` → 本文件

## 结论（必填 · gate 检查）

结论：通过

阻断理由（若有）：无

## 建议

1. Step3 将 `mock_legacy_write` 替换为 runtime `execute_op` 接线时，注意 `legacy_refs` 形态与 snapshot 字段持久化。
2. `validate_op_params` 当前按 mapping 键名校验，与 conn-mock YAML 一致；复杂 JSONPath 映射留后续迭代。
