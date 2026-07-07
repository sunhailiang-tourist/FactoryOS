# rbac · 板块契约

## 是什么

权限 sector：`rbac/modules/{domain}/registry.ts` 定义角色→权限；路由 `permissions` 字段消费。

## 登记索引

| domain | 说明 |
|--------|------|
| `studio` | Integration Studio 七步 + 壳 |

## 追踪链（全链路）

```text
getActorContext().role          # api/request/interceptors
        ↓
rbac/modules/studio/registry.ts # ROLE_PERMISSIONS · MODULE_PERMISSIONS
        ↓
rbac/core/evaluate.ts           # can() · canAccessRoute() · canAccessDomain()
        ↓
router/modules/{id}/registry.ts # permissions: ['studio.xxx.view']
        ↓
router/registry.ts              # getRoutesByLayout(..., role) 过滤
        ↓
layout StudioShellSidebar       # 侧栏按 can() 隐藏
rbac/core/RbacGuard.tsx         # 域级 / 路由级 UI 拦截
        ↓
rbac/core/usePermissions.ts     # 按钮级预留（二期 can('studio.connect.write')）
```

## 变更规则

1. 新增路由须声明 `permissions` 并登记 `MODULE_PERMISSIONS`。
2. `pages/{id}/contracts/README.md` 追踪链须含 `rbac permission` 行。
3. 服务端 403 仍为最终权威；前端 RBAC 仅 UX。
