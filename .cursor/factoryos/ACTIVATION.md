# FactoryOS 工作流完全激活清单

> **唯一激活命令**：仓库根 [README.md §激活开发环境](../../README.md#激活开发环境) · `./scripts/activate_dev_env.sh`  
> 开发前全链路：[PRE-DEV-CHAIN.md](./PRE-DEV-CHAIN.md) · 机器入口：`./scripts/gate` · `./scripts/harness`

---

## 一、一次性配置（每位开发者 / 每台机器）

```bash
# 首次若无 uv
curl -LsSf https://astral.sh/uv/install.sh | sh && source $HOME/.local/bin/env

./scripts/activate_dev_env.sh
```

| # | 步骤 | `activate_dev_env.sh` 内 | 你额外做 |
|---|------|--------------------------|----------|
| 1 | uv 引导工具 | 检查 `uv` 在 PATH | 无则先装 uv（上一行） |
| 2 | 依赖封版 | `uv sync --frozen --extra dev` | — |
| 3 | docs 基线 | `docs_baseline refresh` | — |
| 4 | 工作流验收盘 | `gate pr`（含 deptry） | 须绿 |
| 5 | git 钩子 | `pre-commit` + `pre-push`（`.venv`） | — |
| 6 | Cursor Hooks | — | 仓库根打开 · Settings → `protect-paths` · **重启** |
| 7 | 可选 rg | — | `brew install ripgrep`（本地复现 CI 密钥 grep） |

**pull 后**依赖有变：再跑 `./scripts/activate_dev_env.sh`（或至少 `uv sync --frozen --extra dev`）。

**新第三方包**（编码期）：`uv add <pkg>` / `uv add --dev <pkg>` — 禁止 `pip install`；`uv.lock` 与 `pyproject.toml` 同 commit。pre-commit 与 `gate pr` 会自动检查 lock / import 声明。

### Hooks 未生效时

1. 确认打开的是 **本仓库根目录**（非子文件夹）
2. Cursor Settings → Hooks → 查看 Output 通道报错
3. `chmod +x .cursor/hooks/*.py`（仓库已设置则跳过）
4. 仍不行：**完全重启 Cursor**

### 关闭机械闸门（仅调试用）

临时把 `_factoryos_pipeline/workflow_state.md` 中 `phase: CAN_CODE` — **勿提交**。  
或 Cursor Settings 中禁用项目 Hooks。

---

## 二、每轮迭代：关键词 → 更新 state → Gate 命令

Agent **收到用户关键词后必须先改** `_factoryos_pipeline/workflow_state.md`，再写对应目录。

### 强制输出（你每天只看当日目录即可）

每次执行 `./scripts/gate ...`，都会自动创建并写入：

- `_factoryos_pipeline/<YYYY-MM-DD>/dev/HH-MM_*.md`
- `_factoryos_pipeline/<YYYY-MM-DD>/test/HH-MM_*.md`
- `_factoryos_pipeline/<YYYY-MM-DD>/verify/HH-MM_*.md`

其中 `HH-MM` 为 **UTC** 时间前缀，用于排序；文件内容包含 cmd、exit_code、stdout/stderr，作为当日“计划/结论/验收结论”的统一证据。

| 用户关键词 | 更新 state | 建议 Gate |
|------------|------------|-----------|
| `可以继续`（Step0 后） | `phase: PLANNING` | — |
| `确认规划` | `phase: CAN_TEST` + 填 `plan:` 路径 | `./scripts/gate plan` |
| Test 落 test-plan 后 | `agent: test` · 填 `test_plan:` | `./scripts/gate test` |
| `可以开始` Step N | `phase: CAN_CODE` · `step: N` · `agent: dev` | — |
| Step 停机前 | Verify 落盘 + | `./scripts/gate step --step N -k 'G-01'` |
| Step 验收后 | `可以继续` → 下一 Step 前保持 CAN_CODE 或回 PLANNING | 已通过 `gate step`；下一 Step 编码用 `harness --tier auto` |
| 整体交付 | `phase: DELIVERY` | `./scripts/gate pr` |

### 统一命令速查

```bash
./scripts/gate plan                    # 确认规划（写 plan.ok）
./scripts/gate test                    # test-plan 检查
./scripts/gate verify --step 1         # Verify 回合
./scripts/gate step --step 1 -k 'G-01' # Step 停机（全量）
./scripts/gate pr                      # PR 验收盘
./scripts/gate gate0                   # Gate 0 预备
./scripts/harness --tier auto          # 编码中按 diff
./scripts/factoryos harness --tier full
```

---

## 三、L1 / L2 / L3 / Verify 激活状态（T4.5+）

| 层 | 机制 | 状态 |
|----|------|------|
| **L1** | 关键词 + workflow_state + hooks + **plan.ok 闸门** | ✅ |
| **L2** | contracts + **强制 analyze**（`gate plan`） | ✅ |
| **L3** | harness + pytest + **ruff/pyright** + CI `gate pr` | ✅ |
| **Verify** | 新会话只读审阅 + `gate verify` | ✅ |
| **PR** | body 追溯 + diff 策略（CI `pr-policy`） | ✅ |

---

## 四、里程碑附加口令（非通用 · 示例 W1）

> 通用 SH-步步流 **不含** 本节；仅当 plan / 项目规则要求时，在 **`可以开始` 之前**追加。

当前 FactoryOS Core 首轮（W1）约定口令：

```text
确认编码门禁，开始 W1
```

见 [编码绝对门禁](../rules/编码绝对门禁.mdc)。Agent 仍须先走完 Step0 → plan → Test → `gate test` 绿，再说 `可以开始` 写业务码。

---

## 五、Gate 0 升级路径

当 52 P0 实现完成：

1. 去掉 `src/tests/ac/test_base001_registry.py` 中 `@pytest.mark.pending`
2. 取消注释 `.github/workflows/ci.yml` 中 `gate0-ac-full` job
3. `uv run pytest -v` 全绿 → tag `core-v1.0.0`

---

## 六、PR 模板字段

见 `.github/pull_request_template.md` — 须链 plan 路径与 AC ID。

---

## 七、故障排除

| 现象 | 处理 |
|------|------|
| `activate_dev_env.sh` / `uv sync` 失败 | 检查 Python 3.12；`uv python install 3.12` |
| pytest 找不到 `tests` | 必须在仓库根：`uv run pytest src/tests/contract -v` |
| hook 拦截了合法改 contracts | contracts 应在 ALWAYS_OK；检查路径是否写对 |
| `gate plan` 失败无 plan | 先落盘 `_factoryos_pipeline/<date>/plan/plan-*.md` |
| pending AC 导致 CI 红 | CI 已 `-m "not pending"`；本地全量 `pytest` 会红属预期 |
