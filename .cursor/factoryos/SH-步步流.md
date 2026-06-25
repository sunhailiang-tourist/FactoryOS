# SH-步步流 v2.1 · Governed Spec-Harness

> 版本 v2.1.0 · **每 Step Test 硬性验收 + Verify + 终轮回归后才能 commit**  
> **L3+ 增强型**：L1 人机轨 + L2 Spec + L3 Harness

## 公式

```text
步步确认（可以继续/确认规划/可以开始/可以提交）
  + 落盘（plan/test/step-regression/verify/final-regression/summary）
  + contracts/（OpenAPI · Schema · AC）
  + 每 Step：实现 → Test验收 → Verify → gate step 绿
  + 终轮：Test全量回归 → gate delivery 绿 → 可以提交
  = 步步为营 · 节奏可快 · 次序不乱
```

## 三层控制

| 层 | 内容 |
|----|------|
| L1 人机轨 | [GATES.md](./GATES.md) 关键词；每 Step 停机；commit 前 `可以提交` |
| L2 Spec 轨 | `contracts/` + plan AC/红线对账 |
| L3 Harness 轨 | `./scripts/gate step` · `./scripts/gate delivery` · [ACTIVATION.md](./ACTIVATION.md) |

## 三 Agent + 口令

| Agent | 激活 | 细则 |
|-------|------|------|
| Dev | `【Dev模式启动】` | [STEP0.md](./STEP0.md) · [DEV-GATES.md](./DEV-GATES.md) |
| Test | `【Test模式启动】`（编码前）· `【Test·Step N 验收】`（每 Step）· `【Test·终轮回归】`（commit 前） | [TEST-GATES.md](./TEST-GATES.md) |
| Verify | `【Verify回合】Step N`（**新对话** · Test 验收之后） | [VERIFY-GATES.md](./VERIFY-GATES.md) |

Test 只写 `src/tests/**`；Dev 不宣称测过；Verify 只写 `verify/` 审阅。

## 单次迭代

1. Step 0 → `可以继续`
2. plan 落盘 → `确认规划` → `gate plan`
3. test-plan + failing tests → `gate test`
4. **每 Step**（次序强制）：
   - `可以开始` → Dev 实现 → step-stop
   - `【Test·Step N 验收】` → `test-*-stepN-regression.md`
   - `【Verify回合】Step N` → `verify-*-stepN.md`
   - `gate step` 绿 → `可以继续`
5. change-summary → `DELIVERY`
6. `【Test·终轮回归】` → `test-*-final-regression.md` → `gate delivery` 绿 → `gate pr` 绿
7. 你 `可以提交` → commit / PR

## 模板

`.cursor/factoryos/templates/` · 运行时复制到 `_factoryos_pipeline/`

## 参考存档

`rules/coder-expert-workflow.mdc` · `rules/testing-expert-*.mdc` — **非真源**，仅纪律参考。
