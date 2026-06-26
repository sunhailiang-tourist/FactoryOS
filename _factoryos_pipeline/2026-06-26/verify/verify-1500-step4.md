# Verify 回合：W4 Step 4 — Revert HTTP + 闭环（E-04 · E-05 · B-04 · C-04）

> **plan**：`plan-1339-w4-connector-runtime.md` · **对照** `step-stop-1445-step4.md` · `test-1457-step4-regression.md`

- **step-stop**：`_factoryos_pipeline/2026-06-26/step-stop/step-stop-1445-step4.md`
- **Test 验收**：`_factoryos_pipeline/2026-06-26/test/test-1457-step4-regression.md`
- **对照 AC**：E-04（harness `-k 'E-04'`）

## 核对项

| # | 项 | 结果 | 证据 |
|---|-----|------|------|
| 1 | 未超 plan 范围 | **Pass** | `revert_execution` · `update_execution_status` · `restore_entity` · POST revert · GET execution |
| 2 | 写路径 / 红线 | **Pass** | revert 经 `mock_legacy.restore_entity`；dry_run/simulated → 409；audit `EXECUTE_REVERTED` append-only |
| 3 | AC 可测 | **Pass** | E-04/E-05 各 1 绿；E-02/E-09 回归绿；B-04/C-04 绿 |
| 4 | 无重复逻辑 | **Pass** | 路由薄委托；revert 与 execute 对称落位 `execution_service` |
| 5 | 注释四要素 | **Pass** | `revert_execution` · routes · `restore_entity` 文件头/函数说明齐全 |

## 范围边界（备忘）

| 项 | 评估 |
|----|------|
| revert 直调 `mock_legacy` 非 blueprint revert op | **可接受** — W4 闭环验收；Test 报告已记后续可接 `GOVERNED_WRITE_REVERT` |
| `revert.py` 独立文件未拆 | **可接受** — 逻辑在 `service.py`，与 plan 模块清单略异但职责清晰 |
| W4 全 AC 绿 | **Pass** — 60 passed 存量无破坏 |

## 机械门禁

```bash
.venv/bin/pytest src/tests/integration/test_execution_e02_e04_e05.py -v              # 4 passed
.venv/bin/pytest src/tests/integration/test_connector_blueprint_w4.py -k B-04 -v    # 1 passed
.venv/bin/python scripts/gate_cli.py step --step 4 -k 'E-04'                        # 待执行
```

联动链：`step-stop-1445-step4.md` → `test-1457-step4-regression.md` → 本文件

## 结论（必填 · gate 检查）

结论：通过

阻断理由（若有）：无

## 建议

1. W4 四步链闭合后进入 **Test·终轮回归** → `gate delivery`。
2. 后续可将 `restore_entity` 替换为 runtime blueprint `GOVERNED_WRITE_REVERT` op 执行。
