# WEB-步步流 v1.0（web-admin 独立研发总纲）

> **真源**：`.cursor/INDEX.md` · `contracts/WEB-ARCHITECTURE-LOCK.yaml` · `ARCHITECTURE.md` · `ENGINEERING.md`  
> **验收盘**：`./scripts/activate.sh`（**无** FactoryOS server · **无** pytest）

## 与 FactoryOS 步步流的对齐与切割

| 对齐 | 切割 |
|------|------|
| 关键词停机 · plan 落盘 · 分 Step · Test/Verify 分会话 | 不用 `./scripts/gate plan/start/step` |
| 反黑盒 `_web_pipeline/` | 不用 `_factoryos_pipeline/` |
| AC 对账（WEB-PROFILE） | 不用 STU-001 / `src/tests/**` |
| Harness 全绿才宣称通过 | 不用后端 os_core 写路径 |

## 单轮节拍

```text
【WebDev模式启动】
  → Step0（WEB-STEP0.md）→ 用户「可以继续」
  → 规划落盘 plan → 用户「确认规划」
  → 【WebTest模式启动】failing test 落盘
  → 每 Step N：
      用户「可以开始」→ 仅本 Step 实现（web-admin 内）
      → step-stop 落盘
      → 【WebTest·Step N 验收】新会话
      → 【WebVerify回合】Step N 新会话
      → boundary + harness 绿 → 用户「可以继续」
  → summary → 【WebTest·终轮回归】→ activate 全绿
```

## 绝对门禁（Agent 不得自判放行）

1. **独立边界**：触达 FactoryOS 后端/全局锁 → 停机 → `确认越权`
2. **架构锁**：sector/技术栈/结构变 → 停机 → `确认结构变更`
3. **未确认规划**：禁止写 `src/**` 业务（README/contracts 治理文档除外须用户确认）
4. **未可以开始**：禁止超 Step 实现
5. **Test 禁止改业务**：Test 只写 `*.test.ts(x)` · `e2e/**` · `*.stories.tsx`

## Step 验收盘

```bash
python scripts/check_boundary_lock.py
python scripts/check_harness.py
pnpm lint && pnpm test          # Step 内快反馈
pnpm check                      # 终轮 / 提交前
```

## 禁止

跳 Step · 超 plan · 无落盘写码 · 未绿宣称通过 · 自动 sync 模板 · 自动改 lock · Test 偷改 pages 业务
