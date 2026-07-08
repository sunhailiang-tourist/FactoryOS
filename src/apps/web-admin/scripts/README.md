# scripts · web-admin 工程脚本

## 是什么

前端 **验收盘、codegen、standalone 模拟、DevKit 激活** 的 Python/Bash 入口。

## 子路径

| 路径 | 说明 |
|------|------|
| `activate.sh` | 一键激活 · pnpm check · harness |
| `check_harness.py` | DevKit profile 全量门禁 |
| `run_codegen_api.py` | OpenAPI 类型 codegen（`codegen:api`） |
| `form/` | 表单生成工具链（`form:generate` · S7） |
| `sync_error_registry.py` | vendor → error-codes.ts |
| `py.sh` · `requirements.txt` | 脚本 Python 运行时（含 **pre-commit** · CMNT-C） |
| `devkit/` | bootstrap_standalone · frontend_contract_lib · comment_gate_ts_lib |
| `check_comments.py` · `comment_fix.py` | **CMNT-C** staged/full 校验与补齐 |
| `check_comments_commit_hook.py` | commit 交互式注释门禁（pre-commit） |
| `.pre-commit-config.yaml` | standalone git hooks（迁出后自带） |

## 门禁

```bash
./scripts/activate.sh
pnpm check
pnpm test:w11
python scripts/check_comments.py --full   # CMNT-C 全量（与 pre-push 同款）
```

## 变更纪律

- 新脚本同步 ENGINEERING.md · devkit.profile.yaml
- 新 **子目录** 须用户确认 + directory-readmes 登记 + 更新本表
- 禁止硬编码 umbrella 绝对路径

## 相关文档

- [ENGINEERING.md](../ENGINEERING.md) · [ARCHITECTURE.md](../ARCHITECTURE.md)
