# layout · 布局板块

按域分子目录 `modules/{domain}/`；各子目录自带 `registry.ts`。

| 子目录 | 布局 |
|--------|------|
| `modules/studio/` | StudioShellLayout |

聚合：`layout/registry.ts`

## 门禁

`pnpm check` · `bash scripts/py.sh scripts/check_harness.py`（sector contracts 对账）

## 变更纪律

- 结构变更须 **用户确认** + `contracts/directory-readmes.yaml`
- 改 registry/契约须同步 `contracts/README.md` 追踪链

## 相关文档

- [ARCHITECTURE.md](../../ARCHITECTURE.md) · [ENGINEERING.md](../../ENGINEERING.md)
