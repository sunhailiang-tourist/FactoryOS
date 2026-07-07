# SH-步步流 · 工作流状态机

> Agent **每次收到关键词后必须更新本文件**。Hook 据此机械拦截越权写码。  
> 真源说明：[ACTIVATION.md](../.cursor/factoryos/ACTIVATION.md)

```yaml
phase: CAN_CODE
agent: test
step: 1
plan: _factoryos_pipeline/2026-07-03/plan/plan-1356-stage1-platform-stu001.md
test_plan: _factoryos_pipeline/2026-07-03/test/test-1401-stage1-stu001.md
updated: 2026-07-03
execution_strategy: .cursor/factoryos/PLATFORM-FIRST-EXECUTION-STRATEGY.md
current_stage: 1_platform_polish
goal: 阶段1 Step1 Test 通过 · 待 Verify → gate step → Step2
```

## 执行策略（锁死 · 2026-07-03）

| 阶段 | 状态 | 硬 Gate |
|------|------|---------|
| P0 内核 Gate 0 | ✅ 完成 | BASE-001 52 P0 · 116 pytest |
| **1 平台打磨** | **→ 当前** | **STU-001 P0** |
| 2 终端设计 | 待 | UX-001 P0（须阶段 1 绿） |
| 3 哈森项目验证 | 待 | 四 Gate · D1 |

真源：[PLATFORM-FIRST-EXECUTION-STRATEGY.md](../.cursor/factoryos/PLATFORM-FIRST-EXECUTION-STRATEGY.md) · [14-路线图 §〇](../docs/准备/2026-06-16/14-一年冲刺路线图与并行研发.md)

## W8 进度（已结案）

| Step | AC | 状态 |
|------|-----|------|
| Step0 + plan | | ✅ **`确认规划`** · `gate plan` 绿 |
| Test 编码前 | | ✅ `test-1333` |
| 1 | M-03 | ✅ gate step 绿 · Verify OK |
| 2 | Gate 0 交付 | ✅ **Test 通过** · `test-1422-step2-regression.md` · `test-1422-final-regression.md` · gate delivery OK |

**W8 交付**：`test-1711-w1-w8-full-regression-reverify.md` · **116 pytest 绿** · gate pr OK

## 绝对门禁 · 联动门禁（Dev→Test→Verify）

见 [GATES.md](../.cursor/factoryos/GATES.md) · `scripts/step_chain_lib.py`

## 上轮（W7 · 已 commit）

| 项 | 路径 |
|----|------|
| commit | `f032aec` W7开发完成 |
| summary | `change-summary-1145-w7-gate0-gip-mcp.md` |

## 阶段 1 进度

| Step | AC | 状态 |
|------|-----|------|
| plan | STU-001 | ✅ **`确认规划`** · `gate plan` 绿 |
| Test | failing tests | ✅ `test-1401` · STU 红 13/17 · `gate test` 绿 |
| 0 | BASE-001 基线 · core-v1.0.0 tag | ⏳ |
| 1 | STU-09 | ✅ **Test 通过** · `test-1409-step1-regression.md` · 待 Verify |
| 2 | STU-02/03/11 | 待 |
| 3 | STU-10 | 待 |
| 4 | STU-01/03/04/05 | 待 |
| 5 | STU-06/07/08 · 全量 | 待 |


## WEB-PROFILE 进度（前端自治轨 · **与 STU 无依赖**）

> Charter：`_factoryos_pipeline/2026-07-06/plan/plan-web-admin-profile-autonomy.md`  
> 验收盘：`cd src/apps/web-admin && ./scripts/activate.sh` · **非** STU gate

| 项 | AC | 状态 |
|----|-----|------|
| charter | W-00 | ✅ 2026-07-06 决策修正 · 废止 STU 混轨 |
| v1.7 S1 代码 | W-01～W-05 | ✅ |
| v1.8 S2 | W-06～W-07 | ✅ `test-1702-web-profile-s2s3-regression.md` · activate 绿 |
| v1.9 S3 | W-08～W-10 | ✅ 同上 · 待 **WEB-PROFILE Verify** |
| standalone S | W-11 | 待 |

## 变更日志

- 2026-07-03 Test·Step1 · STU-09 · `test-1409-step1-regression.md` · 120/120 存量绿
- 2026-07-06 **前端自治修正** · WEB-PROFILE 独立轨 · STU Step1 勘误为 **仅 server RBAC** · `corrective-frontend-autonomy-2026-07-06.md`
- 2026-07-03 Dev·**Step1** · Studio API RBAC（web-admin→WEB-PROFILE）· `step-stop-1407-step1.md`
- 2026-07-03 Dev·**`确认规划`** · `gate plan` 绿 · phase→CAN_TEST
- 2026-07-03 Dev·Step0 通过 · plan `plan-1356-stage1-platform-stu001.md` · phase→PLANNING
- 2026-07-03 **执行策略锁死** · 平台先行三阶段 · `PLATFORM-FIRST-EXECUTION-STRATEGY.md` · `14` v1.2.0 · phase→STEP0 阶段1
- 2026-07-02 Test·W1～W8 复验（治理改动后）· `test-1711-w1-w8-full-regression-reverify.md` · 116 passed · gate pr OK
- 2026-07-02 Test·W1～W8 全量复盘 · `test-1656-w1-w8-full-regression.md` · 109 passed · gate delivery/pr OK
- 2026-07-02 Test·Step2 · Gate 0 交付 · `test-1422-step2-regression.md` · `test-1422-final-regression.md` · 109 passed · gate delivery OK
- 2026-07-02 Dev·Step2 · `step-stop-1510-step2.md` · `change-summary-1500` · DELIVERY
- 2026-07-02 Dev·Step1 gate step · M-03 绿
- 2026-07-02 Test·Step1 · `test-1341-step1-regression.md`
- 2026-07-02 Dev·Step1 · `step-stop-1445-step1.md`
