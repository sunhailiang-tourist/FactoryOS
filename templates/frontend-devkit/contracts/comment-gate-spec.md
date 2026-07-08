# 注释门禁规格（前端 App · TypeScript · 真源）

> 版本：**v2.0.0-web** · 2026-07-08（CMNT-C 双速双严 · standalone 自给）
> 关联：`ENGINEERING.md` §4c/§4d · `scripts/check_comments.py`

## 初始化依赖

| 组件 | 依赖 | 说明 |
|------|------|------|
| 脚本 | stdlib + `pyyaml` | `scripts/requirements.txt` |
| git hooks | `pre-commit>=4.0` | 同上；`./scripts/activate.sh` 自动 `pre-commit install` |

**一键激活**：`./scripts/activate.sh`（standalone 须 `cp devkit.manifest.standalone.yaml devkit.manifest.yaml`）

## 策略（双速双严）

| 时机 | 命令 | 范围 |
|------|------|------|
| **git commit** | `check_comments.py --staged` | 仅 staged 的 `src/**/*.ts(x)` |
| **本地** | `check_comments.py --changed` | 工作区改动 |
| **git push** | `check_comments.py --full` | App 内全量 `src/` |

## 分层（P0～P3）

| 层 | TypeScript |
|----|------------|
| **P0** | 文件头七标签 + export function JSDoc |
| **P2** | export 函数体 ≥10 行须有 `//` 块注释 |
| **P3** | `throw` JSDoc 含异常/Error |

## 自动补齐

```bash
# commit 时（pre-commit · TTY）：校验 → 必要性说明 → 你确认 → 补骨架 → 再验
python scripts/comment_fix.py --staged --apply
python scripts/check_comments.py --staged
```

## 实现映射

| 组件 | 路径 |
|------|------|
| 统一验收 | `scripts/check_comments.py` |
| commit 交互 | `scripts/check_comments_commit_hook.py` |
| Git 范围 | `scripts/comment_gate_git.py` |
| TS 规则 | `scripts/devkit/comment_gate_ts_lib.py` |
| 自动补齐 | `scripts/comment_fix.py` · `scripts/comment_fix_lib.py` |
| pre-commit | `.pre-commit-config.yaml` |
