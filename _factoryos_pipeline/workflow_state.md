# SH-步步流 · 工作流状态机

> Agent **每次收到关键词后必须更新本文件**。Hook 据此机械拦截越权写码。  
> 真源说明：[ACTIVATION.md](../.cursor/factoryos/ACTIVATION.md)

```yaml
phase: DELIVERY
agent: test
step: 7
plan: _factoryos_pipeline/2026-07-01/plan/plan-0900-w7-gate0-gip-mcp.md
test_plan: _factoryos_pipeline/2026-07-01/test/test-1655-w7-gate0-gip-mcp.md
updated: 2026-07-01
goal: W7 整体回归绿 · `test-1148-final-regression.md` · gate delivery 可复验
```

## W7 进度

| Step | AC | 状态 |
|------|-----|------|
| Step0 + plan | Gate 0 范围 | ✅ **`确认规划`** · `gate plan` 绿 |
| Test 编码前 | failing tests | ✅ `test-1655` · `gate test` 绿 |
| 1–5 | T-01 … M-02 | ✅ gate 绿 |
| 6 | D-04 · E-08 | ✅ **`gate step` 绿** |
| 7 | N-01～N-04 | ✅ **`gate step` 绿** · Verify `verify-1128-step7.md` |

**W7 交付**：`change-summary-1145-w7-gate0-gip-mcp.md` · `test-1148-final-regression.md`（复验）→ `gate delivery` → `gate pr` → tag `core-v1.0.0`（人工）

## 上轮（W6 · 已 commit）

| 项 | 路径 |
|----|------|
| plan | `plan-1350-w6-reconcile-license.md` |
| summary | `change-summary-1510-w6-reconcile-license.md` |
| 分支 | `dev_sunhailiang_core_260624` |

## 绝对门禁 · 联动门禁（Dev→Test→Verify）

见 [GATES.md](../.cursor/factoryos/GATES.md) · `scripts/step_chain_lib.py`

## 变更日志

- 2026-07-01 Test·W7 整体回归复验 · `test-1148-final-regression.md` · 13+107+13 全绿 · gate delivery OK
- 2026-07-01 Dev·W7 交付 · `change-summary-1145-w7-gate0-gip-mcp.md` · `phase: DELIVERY`
- 2026-07-01 Test·终轮 · `test-1140-final-regression.md` · 107 passed
- 2026-07-01 Verify·Step7 复验 · `verify-1128-step7.md` · 通过
- 2026-07-01 Test·Step7 · N-01～N-04 · `test-1122-step7-regression.md` · 106/106 存量绿
- 2026-07-01 Dev·Step7 · `step-stop-1215-step7.md` · N-01～N-04 pytest 绿
- 2026-07-01 用户 **`可以开始`** · `gate start --step 7` · phase=CAN_CODE
- 2026-07-01 Test·Step6 · D-04/E-08 · `test-1107-step6-regression.md`
- 2026-07-01 Dev·Step6 · `step-stop-1205-step6.md` · D-04/E-08 pytest 绿
- 2026-07-01 Test·Step5 · `test-0942-step5-regression.md`
