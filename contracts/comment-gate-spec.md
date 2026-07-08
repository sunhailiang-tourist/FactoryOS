# 注释门禁规格（Python server + TypeScript 前端 · 真源）

> 版本：**v2.0.0** · 2026-07-08（CMNT-C 双速双严）  
> 关联：`docs/文档/架构/编码绝对门禁.md` §3 · `scripts/check_comments.py` · `scripts/comment_fix.py`

## 初始化依赖（clone / 新机器）

| 组件 | 依赖包 | 说明 |
|------|--------|------|
| 脚本引擎 | **无**（stdlib） | `check_comments*` · `comment_fix*` · `comment_gate_*` |
| git hooks | `pre-commit>=4.0` | `pyproject.toml` → `[dependency-groups] comment-gate` 与 `[project.optional-dependencies] comment-gate` |
| 静态配套 | `ruff` · `pyright` | 已在 `[project.optional-dependencies] dev` |
| 前端 TS 规则 | **无**（stdlib） | `scripts/devkit/comment_gate_ts_lib.py`；standalone App 仅需 `pyyaml`（`scripts/requirements.txt`） |

**一键激活**（仓库根）：`./scripts/activate_dev_env.sh`  
等价于 `uv sync --frozen --extra dev --group dev --group comment-gate` + `pre-commit install` + `pre-push` hooks。

## 策略（双速双严）

| 时机 | 命令 | 范围 | 严格度 |
|------|------|------|--------|
| **git commit** | `check_comments.py --staged` | 仅 `git diff --cached` 内门禁文件 | P0～P3 全开 |
| **本地** | `check_comments.py --changed` | 工作区改动 | 同上 |
| **push / PR** | `check_comments.py --full` | 全量 server + 前端 apps | 同上 |

**原则**：对 staged 文件 **整文件** 严审（非 diff 行）；未 stage 的脏文件 **不拦** commit。

## 分层（P0～P3）

| 层 | Python server | TypeScript web-admin/h5 |
|----|---------------|-------------------------|
| **P0** | 文件头：作用/业务关联/上游/下游 | 文件头七标签 + export function JSDoc |
| **P1** | Pydantic `Field(description=...)` ≥2 字 | （迭代）interface 字段 JSDoc |
| **P2** | 函数体 ≥10 条可执行语句须有 `#` 块注释 | export 函数体 ≥10 行须有 `//` 块注释 |
| **P3** | `raise PlatformError` doc 含异常/ErrorCode | `throw` JSDoc 含异常/Error |

## 自动补齐

```bash
# commit 时（pre-commit）：校验 → 交互提示 → 你确认后自动补骨架 → 再验
# 非 TTY 环境仅拦截，不自动补

# 手动（可选）
uv run python scripts/comment_fix.py --staged --apply
uv run python scripts/check_comments.py --staged
```

- 只补 **缺失** 项，不覆盖合格注释  
- **禁止** CI 静默 `--apply`  
- 补全后须 **二次确认** 才 `git add` 并继续 commit

## 验收盘

```bash
uv run python scripts/check_comments.py --staged
uv run python scripts/check_comments.py --full
uv run pytest src/tests/workflow/test_comment_gate_staged.py -q
uv run pytest src/tests/workflow/test_comment_gate_rules.py -q
./scripts/gate pr
```

## 实现映射

| 组件 | 路径 |
|------|------|
| 统一验收 | `scripts/check_comments.py` |
| commit 交互 | `scripts/check_comments_commit_hook.py` |
| Git 范围 | `scripts/comment_gate_git.py` |
| Python 规则 | `scripts/comment_gate_lib.py` |
| TS 规则 | `scripts/devkit/comment_gate_ts_lib.py` |
| 自动补齐 | `scripts/comment_fix.py` · `scripts/comment_fix_lib.py` |
| pre-commit | `.pre-commit-config.yaml` → `factoryos-comments-staged` |
| pre-push | `factoryos-comments-full` |

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v2.0.0 | 2026-07-08 | CMNT-C staged/changed/full · comment_fix · pre-commit 分层 |
| v1.1.0 | 2026-07-08 | P1～P3 硬化 · 前端 harness 同步 |
| v1.0.0 | 2026-07-08 | 1a.5 存量债闭合 |
