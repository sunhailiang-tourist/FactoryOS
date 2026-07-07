/**
 * 模块：src/apps/web-admin/src/rbac/core/evaluate.ts
 * 作用：纯函数权限评估
 * 怎么用：registry · RbacGuard · usePermissions 调用
 * 解决：可单测、无 React 依赖
 * 上游：rbac/registry.ts
 * 下游：rbac/core/RbacGuard.tsx · usePermissions.ts
 * 关联：rbac/core/evaluate.test.ts
 */

    import { getRolePermissions, MODULE_PERMISSIONS } from "@/rbac/registry";
    import type { Permission, PermissionMode, Role } from "@/rbac/core/types";

    export function permissionsForModule(moduleId: string): Permission[] {
      const perm = MODULE_PERMISSIONS[moduleId];
      return perm ? [perm] : [];
    }

    export function can(role: Role, permission: Permission): boolean {
      const grants = getRolePermissions(role);
      return grants.includes(permission);
    }

    export function canAny(role: Role, permissions: readonly Permission[]): boolean {
      return permissions.some((p) => can(role, p));
    }

    export function canAll(role: Role, permissions: readonly Permission[]): boolean {
      return permissions.length > 0 && permissions.every((p) => can(role, p));
    }

    export function canAccessPermissions(
      role: Role,
      permissions: readonly Permission[],
      mode: PermissionMode = "all",
    ): boolean {
      if (permissions.length === 0) return true;
      return mode === "any" ? canAny(role, permissions) : canAll(role, permissions);
    }

    export function canAccessRoute(
      role: Role,
      permissions: readonly Permission[] | undefined,
      mode: PermissionMode = "all",
    ): boolean {
      return canAccessPermissions(role, permissions ?? [], mode);
    }

    export function canAccessDomain(role: Role, domain: string): boolean {
      const prefix = `${domain}.`;
      const grants = getRolePermissions(role);
      return grants.some((p) => p.startsWith(prefix));
    }
