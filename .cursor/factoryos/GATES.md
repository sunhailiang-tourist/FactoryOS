# 关键词闸门（L1 人机轨 · 不可越级）

| 关键词 | 阶段 | 允许行为 |
|--------|------|----------|
| `可以继续` | Step0 / Step 验收 | 进入规划或下一 Step |
| `确认规划` | 规划关 | plan 落盘 + **`./scripts/gate plan` 绿（plan.ok）** |
| `可以开始` | 编码关 | **`./scripts/gate start --step N`（code.ok）** + 仅当前 Step 写实现 |
| `风险接受并继续` | 存量风险 / Test·Verify 需改进 | 评估为需改进且你书面接受后 |
| `测试不通过` | Step 失败 | Dev 回当前 Step 修复，禁止下一步 |
| `可以提交` | 终轮回归后 | **仅** `gate delivery` 绿 + 终轮 Test 落盘后允许 commit |

## 绝对门禁（机械 · 不可跳过 · 不认 Agent 自改 phase）

三重 stamp（**仅 `./scripts/gate` 可写** · Hook 拦截 Agent 伪造）：

| stamp | 写入命令 | 解锁 |
|-------|----------|------|
| `plan.ok` | `./scripts/gate plan` | 用户 **`确认规划`** 后 · 写 `src/tests/**` · pipeline 落盘 |
| `test.ok` | `./scripts/gate test` | Test test-plan 就绪后 |
| `code.ok` | `./scripts/gate start --step N` | 用户 **`可以开始`** 后 · 写业务码/迁移 |

写测/写码/`gate step` 须：**plan 文件存在** + **stamp 与 workflow_state 一致**。  
`workflow_state` 升到 `CAN_TEST`/`CAN_CODE` 时 Hook **同样校验 stamp**，禁止 Agent 自报 phase 绕门。

真源：`scripts/plan_gate_lib.py` · `.cursor/hooks/protect-paths.py`

## 联动门禁（Dev → Test → Verify · plan 目录隔离）

Step N 全链闭合后才允许 `gate step` 绿 / `可以继续` / 开 Step N+1 Dev：

```text
Dev step-stop-*-stepN.md
  → Test test-*-stepN-regression.md（结论：通过）
  → Verify verify-*-stepN.md（结论：通过）
  → gate step --step N
```

真源：`scripts/step_chain_lib.py` · Hook · `check_test_regression.py` · `check_verify.py` · `check_pipeline.py`

## 禁止

- 未收到关键词 → 禁止 ApplyPatch、改业务代码/迁移
- **Agent 禁止写 `.gates/*`** · 无 stamp 禁止写 `src/**` 代码
- **无「确认规划」+ plan.ok → 禁止一切 src 代码与 pipeline 落盘（plan 草稿除外）**
- 无 plan 落盘 → 禁止 Step 1 编码
- 无 test-plan → 禁止宣称「已测过」
- 无 **Step N Test 单步验收落盘** → 禁止 Verify / `gate step` / `可以继续`
- 无 **终轮 Test 回归落盘** → 禁止 `gate delivery` / 提示 commit
- pytest + CI 未绿 → 禁止输出「可继续」/「可以提交」
- 跳 Step / 超 plan → 立即停机
- Test 改 `os_core`/`apps` 业务 → 违规
- **乱序**：未 step-stop → Test → Verify → `gate step` 绿，禁止 `可以继续`

## Step 内顺序（强制 · 不可乱序）

```text
（编码前，一次性或按 Step 补）Test 写/更新 failing tests（红）
  → 你：可以开始
  → Dev 实现本 Step（绿）
  → Dev step-stop 落盘
  → 【Test·Step N 验收】新会话
        · git diff 本步改动面
        · 业务正确性 + 代码落位合理性
        · 落盘 test-*-stepN-regression.md（结论：通过/需改进/阻断）
  → 【Verify回合】Step N 新会话
        · 只读 plan + git diff + step-stop + Test 落盘
        · 落盘 verify-*-stepN.md（结论：通过/需改进/阻断）
  → ./scripts/gate step --step N -k '<AC-ID>' 绿
  → 你：可以继续
```

**节奏可以快，次序不能乱。** 允许合并对话，但落盘与 gate 顺序不变。

## 整轮结束顺序（commit 前强制）

```text
全部 Step 可以继续
  → Dev change-summary 落盘
  → workflow_state → DELIVERY
  → 【Test·终轮回归】
        · 全量 git diff · 新增功能 · 存量回归 · 落位优雅性
        · 落盘 test-*-final-regression.md（结论：通过/需改进/阻断）
  → ./scripts/gate delivery 绿（workflow+contract+integration 全量 pytest）
  → ./scripts/gate pr 绿
  → 你：可以提交
  → 才允许 git commit / 推 PR
```

## 落盘路径

```text
_factoryos_pipeline/<YYYY-MM-DD>/
  plan/plan-<HHmm>-<slug>.md
  test/test-<HHmm>-<slug>.md                    # 编码前 test-plan
  test/test-<HHmm>-stepN-regression.md          # 每 Step Test 硬性验收（强制）
  test/test-<HHmm>-final-regression.md          # 终轮全量回归（commit 前强制）
  step-stop/step-stop-<HHmm>-stepN.md
  verify/verify-<HHmm>-stepN.md
  summary/change-summary-<HHmm>.md
```

模板：`.cursor/factoryos/templates/test-step-regression-template.md` · `test-final-regression-template.md`

## 违规回滚

立即停止 → 报告越界门禁 → 回到当前阶段 → 重新获得关键词后继续。
