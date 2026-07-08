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

/**
 * 功能：按 moduleId 查所需 Permission 列表。
 * 业务含义：路由/菜单 RBAC 模块级权限映射。
 * 上游：MODULE_PERMISSIONS 常量。
 * 下游：canAccessRoute · RbacGuard。
 */
export function permissionsForModule(moduleId: string): Permission[] {
  const perm = MODULE_PERMISSIONS[moduleId];
  return perm ? [perm] : [];
}

/**
 * 功能：判断角色是否拥有单项 Permission。
 * 业务含义：RBAC 核心判定。
 * 上游：getRolePermissions(role)。
 * 下游：canAny · canAll。
 */
export function can(role: Role, permission: Permission): boolean {
  const grants = getRolePermissions(role);
  return grants.includes(permission);
}

/**
 * 功能：任一 Permission 满足即 true。
 * 业务含义：mode=any 路由守卫。
 * 上游：can(role, p)。
 * 下游：canAccessPermissions。
 */
export function canAny(role: Role, permissions: readonly Permission[]): boolean {
  return permissions.some((p) => can(role, p));
}

/**
 * 功能：全部 Permission 满足才 true。
 * 业务含义：mode=all 路由守卫。
 * 上游：can(role, p)。
 * 下游：canAccessPermissions。
 */
export function canAll(role: Role, permissions: readonly Permission[]): boolean {
  return permissions.length > 0 && permissions.every((p) => can(role, p));
}

/**
 * 功能：按 mode 聚合 canAny/canAll。
 * 业务含义：统一权限列表评估入口。
 * 上游：canAny · canAll。
 * 下游：canAccessRoute。
 */
export function canAccessPermissions(
  role: Role,
  permissions: readonly Permission[],
  mode: PermissionMode = "all",
): boolean {
  if (permissions.length === 0) return true;
  return mode === "any" ? canAny(role, permissions) : canAll(role, permissions);
}

/**
 * 功能：路由级权限判定（permissions 可选）。
 * 业务含义：router registry permissions 字段对接。
 * 上游：canAccessPermissions。
 * 下游：RbacGuard · router loader。
 */
export function canAccessRoute(
  role: Role,
  permissions: readonly Permission[] | undefined,
  mode: PermissionMode = "all",
): boolean {
  return canAccessPermissions(role, permissions ?? [], mode);
}

/**
 * 功能：域级前缀权限（如 studio.*）。
 * 业务含义：粗粒度 domain guard。
 * 上游：getRolePermissions。
 * 下游：layout guard。
 */
export function canAccessDomain(role: Role, domain: string): boolean {
  const prefix = `${domain}.`;
  const grants = getRolePermissions(role);
  return grants.some((p) => p.startsWith(prefix));
}
