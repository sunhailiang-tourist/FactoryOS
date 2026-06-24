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

落盘：`_factoryos_pipeline/<日期>/`（plan · test · step-stop · verify · summary）

### 三个 Agent

| Agent | 口令 | 写什么 | 禁止 |
|-------|------|--------|------|
| **Dev** | `【Dev模式启动】` + 目标 | `src/os_core` · `apps` · `integration` | 不宣称已测过 |
| **Test** | `【Test模式启动】` + plan 路径 | **仅** `src/tests/**` | 改业务代码 |
| **Verify** | `【Verify回合】Step N`（**新对话**） | `verify/` 审阅 | 写实现 |

### 完整工作流

**两轨分离**：跟 Agent **说话**只在 Cursor；**跑命令**只在终端。不要混在一格里。

#### A. Cursor 对话轨（你只发口令，Agent 落盘/写码）

| 顺序 | 在哪说 | 你发 |
|------|--------|------|
| 1 | Dev 对话 | `【Dev模式启动】` + 本轮目标 |
| 2 | Dev 对话 | `可以继续`（Step0 完成后） |
| 3 | Dev 对话 | `确认规划`（plan 落盘后） |
| 4 | **Test 对话** | `【Test模式启动】` + plan 路径 |
| 5 | Dev 对话 | `确认编码门禁，开始 W1`（首轮） |
| 6 | Dev 对话 | `可以开始`（**仅当前 Step**） |
| 7 | Dev 对话 | （Agent 写码并落 step-stop） |
| 8 | **Verify 新对话** | `【Verify回合】Step N` |
| 9 | Dev 对话 | `可以继续`（Step 过关后）或 `测试不通过` |
| 10 | 重复 6–9 | 下一 Step |
| 11 | Dev 对话 | （Agent 落 summary） |

#### B. 终端轨（你自己执行，不对 Agent 念）

| 时机 | 命令 |
|------|------|
| 每台机器一次（激活） | 下方 bash 块 + Cursor Hooks 重启 |
| #3 之后 | `./scripts/gate plan` |
| #4 之后 | `./scripts/gate test` |
| #6–7 编码中（随时） | `./scripts/harness --tier auto` · `git add` · `git commit -m '…'` |
| #8 之后 | `./scripts/gate step --step N -k 'G-01'` |
| #11 之后 | `./scripts/gate pr` · `./scripts/gate docs-sync` · `git push` · 开 PR（body：plan 路径 + AC ID） |

```text
对话：Dev启动 → 可以继续 → 确认规划 ‖ Test启动 → W1总闸 → 可以开始 ⇄ Verify新对话 → 可以继续
终端：gate plan → gate test → (harness+commit)* → gate step → … → gate pr → push → PR
```

### 激活开发环境（终端 · 每台机器一次）

```bash
python3 --version                    # 3.12+
curl -LsSf https://astral.sh/uv/install.sh | sh # 安装
source $HOME/.local/bin/env # 激活
uv sync --extra dev # 安装依赖
./scripts/docs_baseline refresh          # docs 认知基线（首仓 / 大改 docs 后）
uv run python scripts/gate_cli.py pr     # 验证工作流
uv tool install pre-commit     # 安装
source $HOME/.local/bin/env    # 激活
pre-commit install && pre-commit install --hook-type pre-push   # 推荐

```

Cursor 打开**仓库根** → Settings → Hooks 见 `protect-paths` → **重启 Cursor**。  
未说 `可以开始` 时写 `src/os_core/*.py` 应被拦截。排障：[ACTIVATION](.cursor/factoryos/ACTIVATION.md)

### 关键词速查

| 口令 | 何时说 |
|------|--------|
| `可以继续` | Step0 过 / Step 验收后 |
| `确认规划` | plan 落盘后 |
| `可以开始` | 仅当前 Step 写业务码 |
| `测试不通过` | Step 失败，Dev 回修 |
| `确认编码门禁，开始 W1` | W1 首轮业务实现前 |

### 命令速查

| 场景 | 命令 |
|------|------|
| 确认规划 | `./scripts/gate plan` |
| test-plan | `./scripts/gate test` |
| Step 停机 | `./scripts/gate step --step N -k 'G-01'` |
| PR 前 | `./scripts/gate pr` |
| docs 漂移 | `./scripts/gate docs-sync` |
| 编码中 | `./scripts/harness --tier auto` |
| 提交本地 | `git add .` · `git commit -m 'feat(scope): G-01 …'` |
| 推送 PR | `git push` · PR body 写 plan + AC |
| guide 调试（**非实施主路径**） | `./scripts/factoryos guide` |

### 深入阅读

| 用途 | 路径 |
|------|------|
| **UI-First 产品宪法** | [UI-FIRST-CONFIG-PRINCIPLE](.cursor/factoryos/UI-FIRST-CONFIG-PRINCIPLE.md) |
| **接入/扩展链** | [INTEGRATION-CHAIN](.cursor/factoryos/INTEGRATION-CHAIN.md) |
| **开发前全链路** | [PRE-DEV-CHAIN](.cursor/factoryos/PRE-DEV-CHAIN.md) |
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
