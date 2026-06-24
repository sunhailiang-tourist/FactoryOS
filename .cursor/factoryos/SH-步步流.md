# SH-步步流 v2 · Governed Spec-Harness

> 版本 v2.0.0 · 已确认落地  
> **L3+ 增强型**：L1 人机轨 + L2 Spec + L3 Harness

## 公式

```text
步步确认（可以继续/确认规划/可以开始）
  + 落盘（plan/test/step-stop/verify/summary）
  + contracts/（OpenAPI · Schema · AC）
  + failing test → 实现 → `./scripts/gate step` 绿
  = 可控 · 不黑盒 · 假通过难混
```

## 三层控制

| 层 | 内容 |
|----|------|
| L1 人机轨 | [GATES.md](./GATES.md) 关键词；每 Step 停机 |
| L2 Spec 轨 | `contracts/` + plan AC/红线对账 |
| L3 Harness 轨 | `./scripts/gate step` · [ACTIVATION.md](./ACTIVATION.md) |

## 三 Agent

| Agent | 激活 | 细则 |
|-------|------|------|
| Dev | `【Dev模式启动】` | [STEP0.md](./STEP0.md) · [DEV-GATES.md](./DEV-GATES.md) |
| Test | `【Test模式启动】` | [TEST-GATES.md](./TEST-GATES.md) |
| Verify | `【Verify回合】Step N`（**新对话**） | [VERIFY-GATES.md](./VERIFY-GATES.md) |

Test 只写 `src/tests/**`；Dev 不宣称测过；Verify 只写 `verify/` 审阅。

## 单次迭代

1. Step 0 → `可以继续`
2. plan 落盘 → `确认规划`
3. test-plan + failing tests
4. 每 Step：`可以开始` → 实现 → step-stop → Verify 新会话 → `gate step` 绿 → `可以继续`
5. change-summary + Test 最终分区交付 → 你「整体测试通过」

## 模板

`.cursor/factoryos/templates/` · 运行时复制到 `_factoryos_pipeline/`

## 参考存档

`rules/coder-expert-workflow.mdc` · `rules/testing-expert-*.mdc` — **非真源**，仅纪律参考。
