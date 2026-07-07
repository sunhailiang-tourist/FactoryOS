# store · 板块契约

## 是什么

状态板块根注册表：`store/registry.ts`（glob 聚合 `store/modules/*` + `store/common/`）。

## 登记索引

| module-id | store key | 说明 |
|-----------|-----------|------|
| `studio-shell` | studio/shell | 侧栏折叠等纯 UI 态（Server State → useStudioFlows） |

跨模块无业务语义状态：`store/common/registry.ts`（**非** modules 子表）。

## 变更规则

1. 新增 `store/modules/{id}/registry.ts` → **同步** 本表 + 对应 `pages/{id}/contracts/README.md`（store key 行）。
2. 业务态禁止散落在 `pages/`；统一在 `store/modules/`。
3. 变更后须 `pnpm check` + harness 绿。
