# 关键词闸门（L1 人机轨 · 不可越级）

| 关键词 | 阶段 | 允许行为 |
|--------|------|----------|
| `可以继续` | Step0 / Step 验收 | 进入规划或下一 Step |
| `确认规划` | 规划关 | plan 落盘后；允许 Test 写 failing test |
| `可以开始` | 编码/跑测关 | **仅当前 Step** 写实现或执行 pytest |
| `风险接受并继续` | 存量风险 | 触及公共链路且评估阻断时 |
| `测试不通过` | Step 失败 | Dev 回当前 Step 修复，禁止下一步 |

## 禁止

- 未收到关键词 → 禁止 ApplyPatch、改业务代码/迁移
- 无 plan 落盘 → 禁止 Step 1 编码
- 无 test-plan → 禁止宣称「已测过」
- pytest + CI 未绿 → 禁止输出「可继续」
- 跳 Step / 超 plan → 立即停机
- Test 改 `os_core`/`apps` 业务 → 违规

## Step 内顺序（L3 Harness）

```text
Test 写 failing test（红）
  → 你：可以开始
  → Dev 实现（绿）
  → Dev step-stop 落盘
  → **Verify 新会话** → `verify/` 落盘
  → `./scripts/gate step --step N -k '<AC-ID>'` 绿
  → 你：可以继续
```

## 落盘路径

```text
_factoryos_pipeline/<YYYY-MM-DD>/
  plan/plan-<HHmm>-<slug>.md
  test/test-<HHmm>-<slug>.md
  step-stop/step-stop-<HHmm>-stepN.md   # 建议每 Step
  verify/verify-<HHmm>-stepN.md         # Verify 回合（gate step 前置）
  summary/change-summary-<HHmm>.md
```

## 违规回滚

立即停止 → 报告越界门禁 → 回到当前阶段 → 重新获得关键词后继续。
