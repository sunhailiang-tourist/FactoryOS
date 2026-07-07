/**
 * 模块：src/apps/web-admin/src/rbac/core/usePermissions.ts
 * 作用：按钮级权限 Hook（二期扩展位）
 * 怎么用：const { can } = usePermissions(); can('studio.connect.write')
 * 解决：路由级外复用同一 evaluate
 * 上游：getActorContext · rbac/core/evaluate.ts
 * 下游：pages 按钮 · 工具栏（二期）
 * 关联：rbac/contracts/README.md
 */

    import { getActorContext } from "@/api/request";
    import {
      can as canPermission,
      canAccessPermissions,
      canAny,
      canAll,
    } from "@/rbac/core/evaluate";
    import type { Permission, PermissionMode } from "@/rbac/core/types";

    /** 首期薄封装；二期在页面按钮直接消费，无需改目录。 */
    export function usePermissions() {
      const role = getActorContext().role;
      return {
        role,
        can: (permission: Permission) => canPermission(role, permission),
        canAny: (permissions: readonly Permission[]) => canAny(role, permissions),
        canAll: (permissions: readonly Permission[]) => canAll(role, permissions),
        canAccess: (permissions: readonly Permission[], mode: PermissionMode = "all") =>
          canAccessPermissions(role, permissions, mode),
      };
    }
