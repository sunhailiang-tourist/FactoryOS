# Step N 单步验收 · Test 硬性验收报告

- **对照 plan**：`_factoryos_pipeline/<date>/plan/plan-*.md` · Step N
- **命名**：`test-<HHmm>-stepN-regression.md`（HHmm=落盘当下本地时间）
- **口令**：`【Test·Step N 验收】`（Dev step-stop 之后 · Verify 之前）

## 1. git diff 改动面（本 Step）

```bash
git diff --name-only <base>...HEAD
```

| 路径 | 变更 | plan 预期落位 | 实际落位 | 结论 |
|------|------|---------------|----------|------|
| | | | | |

## 2. 本 Step 硬性验收计划（执行记录）

| AC ID | 验收项（业务一句话） | pytest / 证据 | 结果 |
|-------|----------------------|---------------|------|
| | | | PASS/FAIL |

```bash
./scripts/gate step --step N -k '<AC-ID>'
# 附加回归（按改动面，不得省略已受影响存量）：
uv run pytest src/tests/workflow/ src/tests/contract/ -q
# 若触及 integration 域：
uv run pytest src/tests/integration/ -q
```

## 3. 代码落位合理性

| 维度 | 检查 | 结论 |
|------|------|------|
| 分层 | apps/api 薄路由；业务在 os_core | |
| 写路径 | 唯一写 Legacy 经 execution_service | |
| 红线 | R-01–R-11 本步不涉及项已排除 | |
| 注释 | 文件头 + 函数/字段四要素 | |
| 模块治理 | 新目录有 README；无重复逻辑 | |

## 4. 已改动代码测试报告（本 Step）

| 用例ID | AC/接口 | 步骤 | 结果 |
|--------|---------|------|------|

（触及 HTTP 时：每接口 **入参 JSON** + **出参 JSON**，禁止 `...`）

## 5. 架构与代码质量评估（本 Step）

结论子项：分层 · 落位 · 耦合 · 可维护性

## 6. 结论

**结论：通过** | **需改进** | **阻断**

- 阻断 → Dev 回修 · 禁止 Verify / `gate step` / `可以继续`
- 需改进 → 列 1–3 条可执行项；你 `风险接受并继续` 后方可进入 Verify
- 通过 → 进入 **Verify 新会话**
