# router · 路由板块

各业务模块在 `router/modules/{module-id}/registry.ts` 自登记 lazy 页面（`@/pages/{module-id}/*.lazy`），**无** pages 侧 registry、**无**统一 module 描述符。

`router/registry.ts` 通过 **`import.meta.glob`** 自动聚合子目录，**禁止** 手工 import 子表。

模块契约：`pages/{module-id}/contracts/README.md`

聚合：`router/registry.ts` · 组装：`router/compose.tsx`

## 门禁

`pnpm check` · `bash scripts/py.sh scripts/check_harness.py`（sector contracts 对账）

## 变更纪律

- 结构变更须 **用户确认** + `contracts/directory-readmes.yaml`
- 改 registry/契约须同步 `contracts/README.md` 追踪链

## 相关文档

- [ARCHITECTURE.md](../../ARCHITECTURE.md) · [ENGINEERING.md](../../ENGINEERING.md)
