# api/query · 板块契约

## 是什么

TanStack Query Server State 层：`api/query/client.ts` · `keys.ts` · `hooks/use*.ts`。

## 登记索引

| module-id | queryKey | hook | fn |
|-----------|----------|------|-----|
| `studio-shell` | `['studio','flows']` | `useStudioFlows` | `getStudioFlows` |

## 变更规则

1. pages **只** import `@/api/query/hooks/*`；禁止 `@/api/functions` 与 `@tanstack/react-query` 直引。
2. 新增 hook → **同步** 本表 + `pages/{id}/contracts/README.md`（query hook 行）。
3. queryKey 工厂统一在 `keys.ts`。
