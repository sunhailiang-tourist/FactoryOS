# _factoryos_pipeline · SH-步步流 v2.1 运行时落盘

每轮 Dev/Test 的 **可审计工件**（策略真源在 `.cursor/factoryos/`）。

## 结构

```text
_factoryos_pipeline/
  workflow_state.md                         # 状态机（hooks 读取）
  .gates/plan.ok                            # gate plan 成功后写入
  <YYYY-MM-DD>/
    plan/plan-<HHmm>-<slug>.md
    test/test-<HHmm>-<slug>.md              # 编码前 test-plan
    test/test-<HHmm>-stepN-regression.md      # 每 Step Test 硬性验收（强制）
    test/test-<HHmm>-final-regression.md      # 终轮回归（commit 前强制）
    step-stop/step-stop-<HHmm>-stepN.md
    verify/verify-<HHmm>-stepN.md           # Verify（Test 之后）
    report/                                 # 可选 pytest 摘要
    summary/change-summary-<HHmm>.md
    bug/bug-<HHmm>-<slug>.md
    dev/HH-MM_gate-*.md
    test/HH-MM_gate-*.md
    verify/HH-MM_gate-*.md
```

## 模板（复制用）

| 模板 | 路径 |
|------|------|
| plan | `.cursor/factoryos/templates/plan-template.md` |
| test（编码前） | `.cursor/factoryos/templates/test-template.md` |
| test-step（每 Step） | `.cursor/factoryos/templates/test-step-regression-template.md` |
| test-final（commit 前） | `.cursor/factoryos/templates/test-final-regression-template.md` |
| step-stop | `.cursor/factoryos/templates/step-stop-template.md` |
| verify | `.cursor/factoryos/templates/verify-template.md` |
| summary | `.cursor/factoryos/templates/change-summary-template.md` |

本目录 `_templates/` 与 `.cursor/factoryos/templates/` 保持同步。

开发前全链路：[.cursor/factoryos/PRE-DEV-CHAIN.md](../.cursor/factoryos/PRE-DEV-CHAIN.md)

## 规则

- 无 plan → 不写码
- 无 test-plan → 不宣称测过
- 无 **stepN-regression** → 不许 Verify / `gate step` / `可以继续`
- 无 **final-regression** + `gate delivery` 绿 → 不许 `可以提交` / commit
- pytest + CI 未绿 → 不说「可继续」
- 聊天长文 **不能** 代替落盘
