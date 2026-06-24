# _factoryos_pipeline · SH-步步流 v2 运行时落盘

每轮 Dev/Test 的 **可审计工件**（策略真源在 `.cursor/factoryos/`）。

## 结构

```text
_factoryos_pipeline/
  workflow_state.md                         # 状态机（hooks 读取）
  .gates/plan.ok                            # gate plan 成功后写入
  <YYYY-MM-DD>/
    plan/plan-<HHmm>-<slug>.md
    test/test-<HHmm>-<slug>.md
    step-stop/step-stop-<HHmm>-stepN.md
    verify/verify-<HHmm>-stepN.md           # Verify 独立审阅（T4.5+）
    report/                                 # 可选 pytest 摘要
    summary/change-summary-<HHmm>.md
    bug/bug-<HHmm>-<slug>.md                # Test 发现缺陷时
```

## 模板（复制用）

| 模板 | 路径 |
|------|------|
| plan | `.cursor/factoryos/templates/plan-template.md` |
| test | `.cursor/factoryos/templates/test-template.md` |
| step-stop | `.cursor/factoryos/templates/step-stop-template.md` |
| bug | `.cursor/factoryos/templates/bug-template.md` |
| summary | `.cursor/factoryos/templates/change-summary-template.md` |
| verify | `.cursor/factoryos/templates/verify-template.md` |

本目录 `_templates/` 与 `.cursor/factoryos/templates/` 保持同步（改模板请改 `.cursor` 侧后 `cp` 同步）。

开发前全链路：[.cursor/factoryos/PRE-DEV-CHAIN.md](../.cursor/factoryos/PRE-DEV-CHAIN.md)

## 规则

- 无 plan → 不写码
- 无 test-plan → 不宣称测过
- pytest + CI 未绿 → 不说「可继续」
- 聊天长文 **不能** 代替落盘
