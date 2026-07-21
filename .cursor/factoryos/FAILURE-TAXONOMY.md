# 失败税则 FAILURE-TAXONOMY（L4 · P0）

> **代码真源**：`scripts/failure_taxonomy_lib.py` · 本文件为人类镜像（须同步登记全部 `FT-*`）  
> **用法**：Test/Verify/gate 失败后归类 → 回灌契约/规则/脚本（禁止只修业务码）

## 工作流

```bash
# 从失败日志归类 + 生成回灌草稿
python scripts/check_failure_taxonomy.py --classify < fail.log

# 按已知码出草稿
python scripts/check_failure_taxonomy.py --codes FT-PLAN-UI FT-VERIFY-BLOCK

# 完整性
python scripts/check_failure_taxonomy.py --validate
```

落盘回灌 PR 时用模板：`templates/harness-feedback-pr-template.md`

## 税则表

| 码 | 摘要 | 检测面 | 建议回灌 |
|----|------|--------|----------|
| `FT-MATERIALS-MISSING` | 材料准入缺失或新功能滥用 N/A | materials.ok · check_materials · HE-03/04/09 | STEP0.md §材料准入 · gate materials · protect-paths |
| `FT-STAMP-CHAIN` | 四重 stamp 垂直链断裂或伪造 | plan_gate_lib.validate_* · protect-paths | GATES.md · plan_gate_lib · gate_cli |
| `FT-PLAN-STRUCTURE` | plan v2 缺总览/Step 详表 | check_plan_spec.check_structure_v2 · HE-01/02 | plan-template.md · DEV-GATES Gate 3 |
| `FT-PLAN-UI` | UI 对账命中但状态非法/缺表 | check_plan_spec.check_ui_reconcile · HE-05 | STEP0 UI 门禁 · plan §8 |
| `FT-STEP-STOP-UI` | step-stop 缺 UI 字段对账 | step_chain_lib.check_step_stop_ui_gate · HE-06 | step-stop-template.md · DEV-GATES |
| `FT-RUNTIME-EVIDENCE` | step-stop 缺运行时证据合同 | step_chain_lib.check_step_stop_runtime_evidence · HE-07 | step-stop-template §4c · gate step |
| `FT-TEST-FAIL` | Test 单步/终轮结论非通过或缺落盘 | check_test_regression · validate_step_test_done | TEST-GATES.md · test-*-regression.md |
| `FT-VERIFY-BLOCK` | Verify 阻断/需改进被当成通过 | check_conclusion · HE-08 | VERIFY-GATES.md · check_verify.py |
| `FT-CONTRACT-AC` | AC/OpenAPI 与 plan 不对账 | check_plan_spec.check_contracts | contracts/acceptance · OpenAPI export |
| `FT-SENSOR-LINT` | PostToolUse 传感器发现语法/静态问题 | post-edit-sensor.py · sensor_scoped_check.py | 强化 ruff 修复说明书 · scoped pytest |
| `FT-TAXONOMY` | 税则表自身不完整（meta） | validate_taxonomy_integrity · HE-10 | failure_taxonomy_lib.TAXONOMY · 本文件 |
| `FT-HARNESS-DRIFT` | 文档死链/过期 draft/规则漂移 | harness_gc.py | INDEX.md · HARNESS-SCRIPTS · 删除死引用 |

## 纪律

1. **先归类再修码**：同一 FT-* 连续出现 ≥2 次 → 必须开 harness 回灌（规则/脚本/模板），不得只改业务。  
2. **改门禁后必跑**：`./scripts/gate harness-eval`  
3. **禁止** 在未登记税则码的情况下「发明」一次性口令替代门禁。
