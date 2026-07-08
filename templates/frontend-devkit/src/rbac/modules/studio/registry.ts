/**
 * 模块：src/apps/web-admin/src/rbac/modules/studio/registry.ts
 * 作用：Studio 域权限子表
 * 怎么用：registry.ts glob 聚合；evaluate 读取
 * 解决：module-id ↔ permission 模块化维护
 * 上游：Integration-Studio规格 · AC-STU-09
 * 下游：rbac/core/evaluate.ts · router permissions
 * 关联：rbac/contracts/README.md
 */

import type { Permission, Role } from "@/rbac/core/types";

    export const RBAC_DOMAIN = "studio" as const;

    /** module-id → 路由级 view 权限（与 router registry permissions 一致）。 */
    export const MODULE_PERMISSIONS: Record<string, Permission> = {
      "studio-shell": "studio.shell.view",
  "studio-connect": "studio.connect.view",
  "studio-discover": "studio.discover.view",
  "studio-map": "studio.map.view",
  "studio-prove": "studio.prove.view",
  "studio-freeze": "studio.freeze.view",
  "studio-export": "studio.export.view",
    };

    const ALL_STUDIO_VIEW: Permission[] = [
      "studio.shell.view",
    "studio.connect.view",
    "studio.discover.view",
    "studio.map.view",
    "studio.prove.view",
    "studio.freeze.view",
    "studio.export.view",
    ];

    const STUDIO_VIEW_ROLES: Role[] = [
      "integrator",
      "admin",
      "platform",
      "business_owner",
      "customer_it",
    ];

    /** 角色 → 权限列表（首期路由级 view）。 */
    export const ROLE_PERMISSIONS: Record<Role, readonly Permission[]> = {
      integrator: ALL_STUDIO_VIEW,
      admin: ALL_STUDIO_VIEW,
      platform: ALL_STUDIO_VIEW,
      business_owner: ALL_STUDIO_VIEW,
      customer_it: ALL_STUDIO_VIEW,
      operator: [],
    };

/**
 * 功能：studioRolesWithAccess 导出函数。
 * 业务含义：见同文件模块文件头。
 * 上游：见文件头上游。
 * 下游：见文件头下游。
 */
export function studioRolesWithAccess(): Role[] {
      return STUDIO_VIEW_ROLES;
    }
