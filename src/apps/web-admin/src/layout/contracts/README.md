# layout · 板块契约

## 是什么

域壳布局板块：`layout/registry.ts`（glob 聚合 `layout/modules/{domain}/`）。

## 登记索引

| domain-id | pathPrefix | 组件 |
|-----------|------------|------|
| `studio` | /studio | StudioShellLayout |

## 变更规则

1. 新增域 → 创建 `layout/modules/{domain}/` + 本表一行 + `config/modules/{domain}/`（若需 feature flag）。
2. 修改 `pathPrefix` → **同步** 所有关联 `pages/*/contracts/README.md` 的 path 行。
3. 域壳不放业务表单；业务 UI 在 `pages/{module-id}/`。
