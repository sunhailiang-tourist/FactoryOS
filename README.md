# FactoryOS 制造业 AI 执行平台

Overlay on ERP/MES · 双极：终端多模态 + 内核 Graph/Rule/Revert 门禁。

**产品核心不变**；**接入与扩展**：管理台 **Integration Studio**（界面 + AI）为主路径，非 CLI/改仓库。

**拉仓后看本文即可开工。** 工作流真源：`.cursor/factoryos/` · 契约真源：`contracts/` · 厚文档：`docs/`（可选）

| 你是谁 | 从这里开始 |
|--------|------------|
| **实施 / 客户 IT** | [UI-FIRST 产品宪法](.cursor/factoryos/UI-FIRST-CONFIG-PRINCIPLE.md) · [接入链](.cursor/factoryos/INTEGRATION-CHAIN.md) |
| **平台研发** | [开发前全链路](.cursor/factoryos/PRE-DEV-CHAIN.md) · [ACTIVATION](.cursor/factoryos/ACTIVATION.md) |

---

## 研发工作流（SH-步步流 T4.5+）

步步确认 + 契约先行 + 机器门禁，防止 AI 偷跑、假通过。

| 层 | 作用 | 手段 |
|----|------|------|
| **L1 人机轨** | 你说关键词，Agent 才能写对应代码 | `_factoryos_pipeline/workflow_state.md` + Cursor Hooks |
| **L2 Spec** | plan 与 `contracts/` 对齐后再动刀 | `./scripts/gate plan` |
| **L3 Harness** | 静态检查 + pytest 绿才算过 | `./scripts/gate step` · CI |

落盘：`_factoryos_pipeline/<日期>/`（过程产物：plan · test-plan · step-stop · verify · summary；强制结论：`dev/` · `test/` · `verify/` 见下）

### 三个 Agent

| Agent | 口令 | 写什么 | 禁止 |
|-------|------|--------|------|
| **Dev** | `【Dev模式启动】` + 目标 | `src/os_core` · `apps` · `integration` | 不宣称已测过 |
| **Test** | `【Test模式启动】` + plan 路径 | **仅** `src/tests/**` | 改业务代码 |
| **Verify** | `【Verify回合】Step N`（**新对话**） | `verify/` 审阅 | 写实现 |

### 完整工作流

**按表从上到下做。** **类型**列标明：在 Cursor **对话**里说什么，还是在**终端**里跑什么。同一阶段可能先对话、再终端，顺序不要颠倒。

| # | 场景 | 阶段 | 类型 | 你说 / 你做 | 说明 |
|---|------|------|------|-------------|------|
| **0** | 准备 | 激活环境 | 终端 | `./scripts/activate_dev_env.sh`；然后 Cursor 打开仓库根 → Hooks → **重启** | 每台机器一次；`pull` 后依赖有变时重跑。见下方 [§激活开发环境](#激活开发环境) |
| **1** | 启动 | Step0 对齐 | 对话 | **Dev 对话** · `【Dev模式启动】` + 本轮目标 | Agent 读契约、对齐范围；**不写**业务码 |
| **2** | 启动 | Step0 过关 | 对话 | `可以继续` | Agent 更新 `workflow_state` → `PLANNING` |
| **3** | 规划 | 写 plan | 对话 | （等 Agent 落盘） | 产出 `_factoryos_pipeline/<日期>/plan/`（同时 gate 会强制写结论到 `dev/`） |
| **4** | 规划 | 确认规划 | 对话 | `确认规划` | Agent 更新 state → `CAN_TEST` |
| **5** | 规划 | 规划门禁 | 终端 | `./scripts/gate plan` | plan 与 `contracts/` 一致才绿 |
| **6** | 测试 | 写 failing tests | 对话 | **Test 对话** · `【Test模式启动】` + plan 路径 | Test **只**写 `src/tests/**`，不改业务码 |
| **7** | 测试 | test-plan 门禁 | 终端 | `./scripts/gate test` | test-plan 与 plan 对齐；并强制输出 `test/HH-MM_gate-test_*.md`（pytest 结论在 step/pr） |
| **8** | 编码 | 开始本 Step | 对话 | `可以开始` | **仅当前 Step**；Hooks 才放行写 `src/os_core` 等 |
| **9** | 编码 | 编码与提交 | 终端 | `./scripts/harness --tier auto` · `git add` · `git commit -m 'feat(scope): G-01 …'` | 编码中随时跑；pre-commit 自动检 |
| **10** | 编码 | 停机落盘 | 对话 | （Agent 写 step-stop） | 落盘 `_factoryos_pipeline/…/step-stop/` |
| **11** | 验收 | Step 停机检 | 终端 | `./scripts/gate step --step N -k 'G-01'` | harness + pytest + 静态须全绿；强制输出：`dev/`（harness/static/pipeline）+ `test/`（pytest）+ `verify/`（verify gate） |
| **12** | 验收 | 独立审阅 | 对话 | **Verify 新对话** · `【Verify回合】Step N` | 只读审阅，不写实现 |
| **13** | 验收 | 过关或回修 | 对话 | `可以继续`（过关）或 `测试不通过`（回修） | 过关 → 下一 Step 回到 **#8**；不过 → Dev 回修后再 **#11** |
| **14** | 交付 | 汇总 | 对话 | （Agent 落 summary） | `_factoryos_pipeline/…/summary/` |
| **15** | 交付 | 推 PR | 终端 | `./scripts/gate pr` · `./scripts/gate docs-sync` · `git push` · 开 PR | PR body 写 plan 路径 + AC ID |

**↻** #8–#13 每个 Step 重复，直到 plan 里所有 Step 完成。

**三个 Agent 在哪用：** #1–#5、#8–#10、#13–#14 用 **Dev**；#6–#7 用 **Test**；#12 用 **Verify**（必须**新开对话**）。

**里程碑附加口令**（非通用机制）：若 plan 或 [编码绝对门禁](.cursor/rules/编码绝对门禁.mdc) 要求首轮业务码前多一道总闸，在 **`可以开始` 之前**按 plan 说即可（例：当前 W1 → `确认编码门禁，开始 W1`）。见 [ACTIVATION §四](.cursor/factoryos/ACTIVATION.md)。

**强制结论输出（推荐你每天只看这里）**：每次跑 `./scripts/gate ...`，都会在 `_factoryos_pipeline/<日期>/{dev,test,verify}/` 自动创建并写入 `HH-MM_*.md`（UTC 时间前缀），作为当天的“计划/结论/验收结论”统一汇总。

### 激活开发环境（每台机器一次）

**一条命令**（依赖封版 · gate · pre-commit 已内含；与 [ACTIVATION](.cursor/factoryos/ACTIVATION.md) 一致）：

```bash
# 首次若无 uv：
curl -LsSf https://astral.sh/uv/install.sh | sh && source $HOME/.local/bin/env

# 激活（首仓 · 新机器 · pull 后依赖有变时重跑）
./scripts/activate_dev_env.sh
```

脚本依次执行：`uv sync --frozen --extra dev` → `docs_baseline refresh` → `gate pr`（含 deptry）→ `pre-commit install`（钩子走 `.venv`）。

然后：**Cursor 打开仓库根** → Settings → Hooks 见 `protect-paths` → **重启 Cursor**。  
未说 `可以开始` 时写 `src/os_core/*.py` 应被拦截。

编码期新依赖只用 `uv add <pkg>` / `uv add --dev <pkg>`（**禁止** `pip install`）；`pyproject.toml` 与 `uv.lock` 同 commit。其余由 pre-commit / `gate pr` 机械检查。

### 深入阅读

| 用途 | 路径 |
|------|------|
| **UI-First 产品宪法** | [UI-FIRST-CONFIG-PRINCIPLE](.cursor/factoryos/UI-FIRST-CONFIG-PRINCIPLE.md) |
| **接入/扩展链** | [INTEGRATION-CHAIN](.cursor/factoryos/INTEGRATION-CHAIN.md) |
| **开发前全链路** | [PRE-DEV-CHAIN](.cursor/factoryos/PRE-DEV-CHAIN.md) |
| **ORM · 迁移纪律** | [ORM-MIGRATION-PRINCIPLE](.cursor/factoryos/ORM-MIGRATION-PRINCIPLE.md) |
| 索引 | [.cursor/factoryos/INDEX.md](.cursor/factoryos/INDEX.md) |
| Agent 根 | [.cursor/README.md](.cursor/README.md) |
| Dev / Test / Verify | [DEV-GATES](.cursor/factoryos/DEV-GATES.md) · [TEST-GATES](.cursor/factoryos/TEST-GATES.md) · [VERIFY-GATES](.cursor/factoryos/VERIFY-GATES.md) |
| 红线 | [REDLINES.md](.cursor/factoryos/REDLINES.md) |
| 契约 | [contracts/](contracts/) |
| 脚本 | [scripts/README.md](scripts/README.md) |

---

## 代码布局

```text
src/               代码根（见 src/README.md）
src/os_core/       内核九模块
src/apps/          api · web-admin · h5 · edge-agent
src/integration/   Pack · tenants
src/tests/         AC / 契约测试
contracts/         OpenAPI · Schema · 验收
scripts/           gate · harness · docs_baseline
.cursor/           factoryos 工作流 · docs-baseline · hooks
_factoryos_pipeline/  运行时落盘
```

## Gate 0

```text
□ AC-BASE-001 52 P0 PASS
□ contracts/ + gate pr 绿
□ tag core-v1.0.0
```

## 历史文档

`docs/` 含 ADR 与准备材料（可外迁）；**改契约只改 `contracts/`**。
