# SH-步步流 · 工作流状态机

> Agent **每次收到关键词后必须更新本文件**。Hook 据此机械拦截越权写码。  
> 真源说明：[ACTIVATION.md](../.cursor/factoryos/ACTIVATION.md)

```yaml
phase: DELIVERY
agent: dev
step: 4
plan: _factoryos_pipeline/2026-06-26/plan/plan-1121-w3-graph-rule.md
test_final: _factoryos_pipeline/2026-06-26/test/test-1132-w3-final-regression.md
summary: _factoryos_pipeline/2026-06-26/summary/change-summary-1132-w3-graph-rule.md
updated: 2026-06-26
goal: W3 交付关单 — graph · rule · DSL · execution 门禁
```

## W3 四步联动链落盘（Dev → Test → Verify）

| Step | step-stop | Test 单步验收 | Verify |
|------|-----------|---------------|--------|
| 1 | `_factoryos_pipeline/2026-06-26/step-stop/step-stop-1132-step1.md` | `_factoryos_pipeline/2026-06-26/test/test-1132-step1-regression.md` | `_factoryos_pipeline/2026-06-26/verify/verify-1140-step1.md` |
| 2 | `_factoryos_pipeline/2026-06-26/step-stop/step-stop-1132-step2.md` | `_factoryos_pipeline/2026-06-26/test/test-1132-step2-regression.md` | `_factoryos_pipeline/2026-06-26/verify/verify-1140-step2.md` |
| 3 | `_factoryos_pipeline/2026-06-26/step-stop/step-stop-1132-step3.md` | `_factoryos_pipeline/2026-06-26/test/test-1132-step3-regression.md` | `_factoryos_pipeline/2026-06-26/verify/verify-1140-step3.md` |
| 4 | `_factoryos_pipeline/2026-06-26/step-stop/step-stop-1132-step4.md` | `_factoryos_pipeline/2026-06-26/test/test-1132-step4-regression.md` | `_factoryos_pipeline/2026-06-26/verify/verify-1140-step4.md` |

**终轮**：`test_final` · **摘要**：`summary` · **批量摘要索引**：`step-stop/step-stop-w3-impl.md`

**下一步**：`./scripts/gate delivery` 绿 → `./scripts/gate pr` 绿 → 用户 **`可以提交`**

## 绝对门禁（plan · 不可跳过）

| 条件 | 阻断 |
|------|------|
| 无 `workflow_state.plan` 或 plan 文件不存在 | 写 `src/tests/**` · 业务码 · migration · `gate step/delivery` |
| 无 `.gates/plan.ok` 或 与 state.plan 不一致 | 同上 |
| `phase` 为 `STEP0` / `PLANNING` | 写业务码 · `gate step` |
| 未 `可以开始`（`phase≠CAN_CODE`） | 写 `src/os_core/**` · `src/apps/**` · `alembic/versions/**` |

**唯一解锁**：用户 **`确认规划`** → Dev 填 `plan:` → **`./scripts/gate plan` 绿**（写 `plan.ok`）→ 再 `可以开始`。

## 联动门禁（Dev → Test → Verify · 不可跳步）

| 阶段 | 须先满足 | 机械阻断 |
|------|----------|----------|
| **Test·Step N 验收** | Dev `step-stop-*-stepN.md` | Hook · `check_test_regression.py` |
| **Verify·Step N** | Test `test-*-stepN-regression.md` 结论通过 | Hook · `check_verify.py` |
| **`gate step --step N`** | 上表 + Verify `verify-*-stepN.md` 结论通过 | `step_chain_lib` · `check_pipeline.py` |
| **可以开始 Step N+1** | Step N 全链闭合 | Hook · `validate_can_start_step_dev` |

真源：`scripts/step_chain_lib.py` · 按 **当前 plan 日期目录** 隔离（禁止 W2 Verify 冒充 W3）。

## phase 取值

| phase | 解锁条件（用户关键词） | 允许写入 |
|-------|------------------------|----------|
| `STEP0` | 初始 / 新一轮 | `_factoryos_pipeline/` · `contracts/` · `scripts/` · `.cursor/` · `docs/` · `*.md` |
| `PLANNING` | `可以继续`（Step0 通过） | + `plan/` 落盘 |
| `CAN_TEST` | `确认规划` + **`gate plan` 绿** | + `test/` · `src/tests/**` |
| `CAN_CODE` | `可以开始` | + 业务码 · migration |
| `DELIVERY` | 终轮 Test 通过 | summary；`gate delivery` |

## 变更日志

- 2026-06-26 新增 **确认规划绝对门禁**（`plan_gate_lib` · Hook · gate 机械阻断）
- 2026-06-26 新增 **Dev→Test→Verify 联动门禁**（`step_chain_lib` · plan 目录隔离）
- 2026-06-26 **W3 关单**：`phase: DELIVERY` · 四步 test/verify 路径挂表 · 逐步落盘补录完成
