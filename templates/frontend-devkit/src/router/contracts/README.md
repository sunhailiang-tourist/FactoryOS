# router · 板块契约

## 是什么

路由板块根注册表：`router/registry.ts`（glob 聚合 `router/modules/*/registry.ts`）。

## 登记索引

| module-id | route name | path | layout |
|-----------|------------|------|--------|
| `studio-connect` | studio.connect | /studio/connect | studio |
| `studio-discover` | studio.discover | /studio/discover | studio |
| `studio-export` | studio.export | /studio/export | studio |
| `studio-freeze` | studio.freeze | /studio/freeze | studio |
| `studio-map` | studio.map | /studio/map | studio |
| `studio-prove` | studio.prove | /studio/prove | studio |
| `studio-shell` | studio.home | /studio | studio |

页面模块契约真源：`pages/{module-id}/contracts/README.md`（追踪链须与本表一致）。

## 变更规则

1. 新增/修改 `router/modules/{id}/registry.ts` → **同步** 本表 + `pages/{id}/contracts/README.md` 追踪链。
2. 禁止手改 `router/registry.ts` 聚合 import；仅用 glob。
3. `pnpm create:module` 后运行 `./scripts/activate.sh` 或 `scripts/check_harness.py`。
