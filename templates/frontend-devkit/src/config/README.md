# config · 配置板块

| 文件 | 职责 |
|------|------|
| `env.ts` | 环境变量 |
| `modules/{domain}/registry.ts` | 域级 feature flags |
| `registry.ts` | 聚合各域子注册表 |

## 门禁

`pnpm check` · `bash scripts/py.sh scripts/check_harness.py`（sector contracts 对账）

## 变更纪律

- 结构变更须 **用户确认** + `contracts/directory-readmes.yaml`
- 改 registry/契约须同步 `contracts/README.md` 追踪链

## 相关文档

- [ARCHITECTURE.md](../../ARCHITECTURE.md) · [ENGINEERING.md](../../ENGINEERING.md)
