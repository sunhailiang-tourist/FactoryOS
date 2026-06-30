# SH-步步流 · 工作流状态机

> Agent **每次收到关键词后必须更新本文件**。Hook 据此机械拦截越权写码。  
> 真源说明：[ACTIVATION.md](../.cursor/factoryos/ACTIVATION.md)

```yaml
phase: STEP0
agent: —
step: —
plan: —
test_plan: —
updated: 2026-06-30
goal: W5 已交付 · 待 W6 plan（对账 Job stub + License stub）
```

## 上轮交付（W5 · 已闭合）

| 项 | 路径 |
|----|------|
| plan | `_factoryos_pipeline/2026-06-30/plan/plan-0330-w5-agent-harness.md` |
| summary | `_factoryos_pipeline/2026-06-30/summary/change-summary-1341-w5-agent-harness.md` |
| 终轮 Test | `_factoryos_pipeline/2026-06-30/test/test-1330-final-regression.md` |
| git | `dev_sunhailiang_core_260624` · 已 commit + push |

**W5 AC**：workflow · H-01 · H-02 · H-03 · OpenAPI 对账 — 全绿 · `gate delivery` · `gate pr` OK

## 下一轮（W6 · 未启动）

路线图：[14-一年冲刺路线图](../docs/准备/2026-06-16/14-一年冲刺路线图与并行研发.md) — **对账 Job stub + License stub**

启动口令：**【Dev模式启动】** → Step0 → `可以继续` → plan 落盘 → `确认规划`

## 绝对门禁 · 联动门禁

见 [GATES.md](../.cursor/factoryos/GATES.md) · `scripts/step_chain_lib.py`

## 变更日志

- 2026-06-30 W5 交付闭合 · summary 落盘 · `phase: STEP0` 重置（待 W6）
- 2026-06-30 W5 commit + push · gate delivery/pr 绿
- 2026-06-30 Test·终轮回归 · `test-1330-final-regression.md`
