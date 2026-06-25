# SH-步步流 · 工作流状态机

> Agent **每次收到关键词后必须更新本文件**。Hook 据此机械拦截越权写码。  
> 真源说明：[ACTIVATION.md](../.cursor/factoryos/ACTIVATION.md)

```yaml
phase: DELIVERY
agent: test
step: 4
plan: _factoryos_pipeline/2026-06-25/plan/plan-0116-w1-base.md
test_plan: _factoryos_pipeline/2026-06-25/test/test-1443-w1-step1-4.md
summary: _factoryos_pipeline/2026-06-25/summary/change-summary-0807-w1-base.md
updated: 2026-06-25
goal: W1 基座首轮 — 完成
w1_coding_gate: confirmed
step1_gate: green
step2_gate: green
step3_gate: green
step4_gate: green
step4_verify: _factoryos_pipeline/2026-06-25/verify/verify-1558-step4.md
gate_pr: green
```

## phase 取值

| phase | 解锁条件（用户关键词） | 允许写入 |
|-------|------------------------|----------|
| `STEP0` | 初始 / 新一轮 | `_factoryos_pipeline/` · `contracts/` · `scripts/` · `.cursor/` · `docs/` · `*.md` |
| `PLANNING` | `可以继续`（Step0 通过） | + `plan/` 落盘 |
| `CAN_TEST` | `确认规划` | + `test/` · `src/tests/**` |
| `CAN_CODE` | `可以开始` | + `src/os_core/**` · `src/apps/**` · `src/integration/**` 业务代码 |
| `DELIVERY` | 整体测试通过 | summary；准备 PR |

## agent 取值

| agent | 激活口令 | 写权限 |
|-------|----------|--------|
| `dev` | `【Dev模式启动】` | 按 phase；业务码需 `CAN_CODE` |
| `test` | `【Test模式启动】` | **仅** `src/tests/**` + `_factoryos_pipeline/` |

## 变更日志

- 2026-06-16 初始化 · 治理包落地
- 2026-06-25 W1 基座 · Step0 通过 → PLANNING · plan-0116-w1-base.md
- 2026-06-25 用户确认规划 → CAN_TEST · plan §1.1 编码纪律
- 2026-06-25 W1 编码门禁口令已确认 · gate test 绿 · 待 `可以开始` Step 1
- 2026-06-25 Step 1 停机 + Verify 通过 · 用户 `可以继续` → 进入 Step 2 待开工
- 2026-06-25 Step 2 shared_contracts 实现完成 · 待 Verify + gate step 2
- 2026-06-25 Step 2 停机 + Verify 通过 · 用户 `可以继续` → 进入 Step 3 待开工
- 2026-06-25 Step 4 mock connector + C-01 完成 · 待 Verify
- 2026-06-25 W1 四轮 Step+Verify 全绿 · gate pr 绿 · summary 落盘 · phase DELIVERY
