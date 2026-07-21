# WEB-步步流 v1.1（web-admin 独立研发总纲 · L4）

> **真源**：`.cursor/INDEX.md` · `WEB-GATES.md` · `contracts/WEB-ARCHITECTURE-LOCK.yaml`  
> **验收盘**：`./scripts/activate.sh` + **`./scripts/web_gate`**（**非** FactoryOS `./scripts/gate` · **非** pytest）

## 与 FactoryOS 步步流的对齐与切割

| 对齐 | 切割 |
|------|------|
| 材料→stamp→plan→分 Step→Test/Verify→eval/GC | 不用 `./scripts/gate` / `_factoryos_pipeline` |
| 反黑盒 `_web_pipeline/` + `.gates` | 不用后端 materials.ok |
| AC 对账（WEB-PROFILE） | 不用 STU / `src/tests/**` |
| Harness 全绿才宣称通过 | 用 `check_harness` + `web_gate harness-eval` |

## 单轮节拍

```text
【WebDev模式启动】
  → 新功能：材料准入 →「材料已齐」→ ./scripts/web_gate materials
  → Step0（WEB-STEP0.md）→「可以继续」
  → 规划落盘 plan →「确认规划」→ ./scripts/web_gate plan
  → 【WebTest模式启动】failing test → ./scripts/web_gate test
  → 每 Step N：
      「可以开始」→ ./scripts/web_gate start --step N
      → 仅本 Step 实现 → step-stop（含运行时证据）
      → 【WebTest·Step N 验收】→ 【WebVerify回合】Step N
      → ./scripts/web_gate step --step N 绿 →「可以继续」
  → summary → 【WebTest·终轮回归】→ activate 全绿
```

## 绝对门禁

1. **独立边界** / **架构锁**（WEB-00 / WEB-01）
2. **无 materials.ok** → 禁止写 `plan-*.md`
3. **无 plan.ok / test.ok / code.ok** → 禁止写 `src/**` 业务（Hook 机械拦截）
4. **Test 禁止改业务**

## Step 验收盘

```bash
./scripts/web_gate step --step N
python scripts/check_boundary_lock.py
python scripts/check_harness.py
pnpm lint && pnpm test
```

## L4 外环

```bash
./scripts/web_gate harness-eval
./scripts/web_gate harness-gc
```
