# SH-步步流 · 工作流状态机

> Agent **每次收到关键词后必须更新本文件**。Hook 据此机械拦截越权写码。  
> 真源说明：[ACTIVATION.md](../.cursor/factoryos/ACTIVATION.md)

```yaml
phase: STEP0
agent: dev
step: 0
plan: null
test_plan: null
updated: 2026-07-14
execution_strategy: .cursor/factoryos/PLATFORM-FIRST-EXECUTION-STRATEGY.md
current_stage: awaiting_goal
goal: null  # 【Dev模式启动】已激活 · 待用户给出本轮目标
blocked_until: null
blocked_1b_plan: _factoryos_pipeline/2026-07-08/plan/plan-1524-stu-ui-studio-api-wiring.md
last_closed: CMNT-C (plan-1554) · 1a.5 已结案 · 1b 曾封存于 plan-1524
```

## 执行策略（锁死 · 2026-07-08 插入 1a.5）

| 阶段 | 状态 | 硬 Gate |
|------|------|---------|
| P0 内核 Gate 0 | ✅ 完成 | BASE-001 52 P0 · 116 pytest |
| **1a 平台 API** | **✅ 结案** | STU pytest 17/17 · `gate delivery`（API 切片） |
| **1a.5 注释债闭合** | **✅ 结案** | CMNT 647→0 · `gate step 5` · 用户 **`可以继续`** |
| **1b 平台 UI** | **⏸ 暂停** | **CMNT-C08 后** 才开 Studio 联调 · plan-1524 封存 |
| **CMNT-C 注释闭环** | **→ 当前** | staged 严审 + comment_fix · 待 **`确认规划 CMNT-C`** |
| **2 终端设计** | 待（须 1b 绿） | UX-001 · **h5-worker** |
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
| 0 | BASE-001 基线 · core-v1.0.0 tag | ✅ `core-v1.0.0` 已打 |
| 1 | STU-09 | ✅ Verify 绿 · `verify-1518` · `gate step 1` 绿 |
| 2 | STU-02/03/11 | ✅ Verify 绿 · `verify-1656` · `gate step 2` 绿 |
| 3 | STU-10 | ✅ Verify 绿 · `verify-1717` · `gate step 3` 绿 |
| 4 | STU-01/03/04/05 | ✅ `gate step 4` 绿 · `verify-1737` |
| 5 | STU-06/07/08 · 全量 | ✅ **1a** · `gate step 5` · `test-1754-final`（API 切片） |
| **1a.5** | **CMNT-01～07** | **✅ 结案** · `gate step 5` · 647→0 |
| **1b** | **STU-UI 联调** | **⏸ 封存** · plan-1524 · **CMNT-C08 后解锁** |
| **CMNT-C** | **注释闭环 v2** | **✅ 落地** · plan-1554 · 待用户 **`可以继续`** 解锁 1b |


## WEB-PROFILE 进度（前端自治轨 · **与 STU 无依赖**）

> Charter：`_factoryos_pipeline/2026-07-06/plan/plan-web-admin-profile-autonomy.md`  
> 验收盘：`cd src/apps/web-admin && ./scripts/activate.sh` · **非** STU gate

| 项 | AC | 状态 |
|----|-----|------|
| charter | W-00 | ✅ 2026-07-06 决策修正 · 废止 STU 混轨 |
| v1.7 S1 代码 | W-01～W-05 | ✅ |
| v1.8 S2 | W-06～W-07 | ✅ `test-1702-web-profile-s2s3-regression.md` · activate 绿 |
| v1.9 S3 | W-08～W-10 | ✅ 同上 · 待 **WEB-PROFILE Verify** |
| standalone S | W-11 | ✅ 封存 `frontend-devkit 2.0.0-s5` |

## 阶段 1a.5 进度（注释债 · ✅ 结案）

| Step | AC | 状态 |
|------|-----|------|
| plan | CMNT-* | ✅ **`确认规划`** · `gate plan` 绿 · `plan.ok` |
| Test | 回归基线 | ✅ **`【Test模式启动】`** · `test-0910` · STU 17/17 · pytest 135 · 注释 647 基线 |
| 0 | 基线 647 | ✅ `summary/0910-comment-baseline.md` |
| 1 | CMNT-01 B0 | ✅ `gate step 1` 绿 · 用户 **`可以继续`** |
| 2 | CMNT-02 B1a | ✅ `gate step 2` 绿 · 用户 **`可以继续`** |
| 3 | CMNT-02 B1b | ✅ **`gate step 3` 绿** · 用户 **`可以继续`** |
| 4 | CMNT-03 B2 | ✅ **`gate step 4` 绿** · 用户 **`可以继续`** |
| 5 | CMNT-04～07 | ✅ **`gate step 5` 绿** · 用户 **`可以继续`** · **1b 已解锁** |

真源：`contracts/python_comment_backfill_batches.yaml` · 机械门禁已接 `gate step`（`--gate`）；Step5 切全量。

## 变更日志

- 2026-07-14 【Dev模式启动】· `phase: STEP0` · 上轮 CMNT-C/1a.5 已结 · 本轮目标未定 · 等用户补齐后开 Step 0

- 2026-07-08 用户决策 · **先 CMNT-C 注释闭环，暂停 1b 联调** · plan `plan-1554` · `blocked_until: CMNT-C08` · plan-1524 封存

- 2026-07-08 用户 **`可以继续`** · 1b Step0 完成 · plan `plan-1524` 封存（待 CMNT-C 后确认）

- 2026-07-08 **`gate step 5` 绿** · CMNT-05 · 1a.5 注释债 0 违规

- 2026-07-08 Test·**Step5 终轮** · `test-1038-step5` · `test-1038-final` · 647→0 · 145 pytest
- 2026-07-08 Dev·**Step5** · CMNT-04/05 · 153→0 · 全量门禁硬化 · `step-stop-1032-step5` · 145 pytest 绿
- 2026-07-08 **`gate step 4` 绿** · CMNT-03 · 153 债
- 2026-07-08 Test·**Step4** · CMNT-03 B2 · `test-1020-step4-regression.md` · 153 债 · 143 pytest 0 FAIL
- 2026-07-08 Dev·**Step4** · CMNT-03 B2 · 370→0 · 523→153 · `step-stop-1015-step4` · 143 pytest 绿
- 2026-07-08 用户 **`可以继续`** · Step3 结案 → Step4 待开工
- 2026-07-08 Test·**Step3** · CMNT-02 B1b · `test-1001-step3-regression.md` · 523 债 · 143 pytest 0 FAIL
- 2026-07-08 Dev·**Step3** · CMNT-02 B1b · 24→0 · 547→523 · `step-stop-1000-step3` · 143 pytest 绿
- 2026-07-08 Test·**Step2** · CMNT-02 B1a · `test-0951-step2-regression.md` · 547 债 · 141 pytest 0 FAIL
- 2026-07-08 Dev·**Step2** · B1a 74→0 · 621→547 · `step-stop-0945-step2`
- 2026-07-08 workflow_state yaml 修复 · Step1 结案 → Step2 待开工
- 2026-07-08 用户 **`可以继续`** · Step1 结案 → Step2
- 2026-07-08 Test·**Step1** · CMNT-01 · `test-0927-step1-regression.md` · B0 绿 · 140 pytest · 647→621
- 2026-07-08 Test·**【Test模式启动】** · `test-0910` · 回归基线 17/17 · 135 pytest · 647 注释债 · `gate test` 绿
- 2026-07-08 用户 **`可以开始` Step1** · `gate start 1` · Dev·B0 注释 9 文件 · CMNT-01 机械绿 · pytest 140 绿
- 2026-07-08 **插入 1a.5** · plan `plan-0910-server-comment-debt-closure` · 647 基线 · **1b 阻塞至 CMNT-07**
- 2026-07-07 Test·**终轮回归** · `test-1754-final-regression.md` · 134 passed · **`gate delivery` 绿**
- 2026-07-07 **主流程同步** · PLATFORM-FIRST v1.1.0 · 阶段 **1a/1b** 双子步 · D16 · `current_stage: 1b_stu_ui`
- 2026-07-07 **`gate delivery` 绿** · `test-1754-final-regression.md` · 134 pytest · STU 17/17
- 2026-07-07 **`gate step 5` 绿** · `verify-1751` · STU-06/07/08
- 2026-07-07 Dev·**Step5 停机** · STU-06/07/08 回归 · 17/17 · 84 integration · `step-stop-1746-step5.md`
- 2026-07-07 用户 **`可以开始` Step5** · `gate start 5` 绿
- 2026-07-07 **`gate step 4` 绿** · STU-01/04/05 · `verify-1737`
- 2026-07-07 Test·**Step4** · `test-1728-step4-regression.md` · AC 3/3 绿 · workflow import 边界需改进
- 2026-07-07 Dev·**Step4 回修** · import 边界编排上移 · workflow CAN_VERIFY 归一化 · 待 Test 重验
- 2026-07-07 Dev·**Step4 停机** · STU-01/04/05 · `step-stop-1730-step4.md` · 81 integration 绿
- 2026-07-07 Test·**Step3** · STU-10 · `test-1712-step3-regression.md` · 4/4 · 存量 78 绿
- 2026-07-07 Dev·Verify 修复 · ruff I001 `registry.py` import · static OK
- 2026-07-07 Dev·**Step3 停机** · path 模板 + tenant provision · `step-stop-1710-step3.md`
- 2026-07-07 用户 **`可以继续`** · Step2 结案 · `gate step 2` 绿 → Step3
- 2026-07-07 Dev·**方案 A** · K-01/K-02 `since` · integration 存量 74/74 绿
- 2026-07-07 Test·Step2 · STU-02/03/11 · `test-1644-step2-regression.md` · 4/4 绿 · K-01 存量需改进
- 2026-07-07 Dev·Step0 通过 · 用户 **`可以继续`** · 待 **`可以开始` Step2**
- 2026-07-07 Dev·**【Dev模式启动】** · 阶段1 Step2 Step0 · WEB-PROFILE 封存对齐 · 续 STU integration API
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
