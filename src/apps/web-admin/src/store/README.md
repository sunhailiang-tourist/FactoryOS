# store · 状态板块

| 层 | 路径 | 职责 |
|----|------|------|
| 公共 | `common/registry.ts` | 跨模块可读的无业务语义状态 · **禁止** `common/shared/` |
| 业务 | `modules/{module-id}/` | 与路由 module 同名 · `*.store.ts` + `registry.ts` |

业务态 **禁止** 散落在 `pages/` 页面目录；统一在 `store/modules/` 治理。

聚合：`store/registry.ts`

## 门禁

`pnpm check` · `bash scripts/py.sh scripts/check_harness.py`（sector contracts 对账）

## 变更纪律

- 结构变更须 **用户确认** + `contracts/directory-readmes.yaml`
- 改 registry/契约须同步 `contracts/README.md` 追踪链

## 相关文档

- [ARCHITECTURE.md](../../ARCHITECTURE.md) · [ENGINEERING.md](../../ENGINEERING.md)
