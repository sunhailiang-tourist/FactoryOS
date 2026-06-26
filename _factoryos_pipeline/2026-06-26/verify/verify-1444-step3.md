# Verify 回合：W4 Step 3 — execution L2 真写 + snapshot（E-02 · E-09）

> **plan**：`plan-1339-w4-connector-runtime.md` · **对照** `step-stop-1435-step3.md` · `test-1442-step3-regression.md`

- **step-stop**：`_factoryos_pipeline/2026-06-26/step-stop/step-stop-1435-step3.md`
- **Test 验收**：`_factoryos_pipeline/2026-06-26/test/test-1442-step3-regression.md`
- **对照 AC**：E-02（harness `-k 'E-02'`）

## 核对项

| # | 项 | 结果 | 证据 |
|---|-----|------|------|
| 1 | 未超 plan 范围 | **Pass** | `execution_service/service.py` 接线 `execute_op`；`store.py` 持久化 snapshot/legacy_refs；无 `revert.py` / revert HTTP |
| 2 | 写路径 / 红线 | **Pass** | `writes_legacy` → `execute_op` 唯一 L2 出口；dry_run 仍不写 Legacy（E-06 回归绿） |
| 3 | AC 可测 | **Pass** | `test_E02_*` · `test_E09_*` 各 1 绿 |
| 4 | 无重复逻辑 | **Pass** | `_runtime_legacy_refs` 桥接 runtime dict → `LegacyRef[]`；store 读写对称 |
| 5 | 注释四要素 | **Pass** | service/store/mock_legacy 文件头已更新 |

## 范围边界（合理超前 / 备忘）

| 项 | 评估 |
|----|------|
| E-03 audit 旁证 | **可接受** — L2 写路径产生 EXECUTE_STARTED/COMPLETED 事件 |
| 未新增 migration 004 | **正确** — 002 已预埋 `before_snapshot_json` / `after_snapshot_json` / `legacy_refs_json` |
| `DEFAULT_PACK_ID = conn-mock` 硬编码 | **备忘** — W5+ Pack 配置化，非阻断 |
| E-04/E-05 仍红（2 项） | **预期** — Step4 revert HTTP 未实现 |
| `get_entity_snapshot` alias | **可接受** — 为 Step4 revert 读回预埋，无 revert 逻辑 |

## 机械门禁

```bash
.venv/bin/pytest src/tests/integration/test_execution_e02_e04_e05.py -k 'E-02 or E-09' -v   # 2 passed
.venv/bin/pytest src/tests/integration/test_execution_e06_e07.py test_execution_e01.py -q  # 3 passed
.venv/bin/python scripts/gate_cli.py step --step 3 -k 'E-02'                                # 待执行
```

联动链：`step-stop-1435-step3.md` → `test-1442-step3-regression.md` → 本文件

## 结论（必填 · gate 检查）

结论：通过

阻断理由（若有）：无

## 建议

1. Step4 实现 `POST /v1/execute/{execId}/revert` 时复用 `before_snapshot` 与 `get_entity_snapshot`。
2. 可选：补 E-03 L2 路径专用用例（当前旁证已足够）。
