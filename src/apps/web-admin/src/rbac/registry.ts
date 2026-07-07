/**
 * 模块：src/apps/web-admin/src/rbac/registry.ts
 * 作用：rbac 板块 glob 聚合域子表
 * 怎么用：evaluate.ts import；harness 对账
 * 解决：多域权限可扩展
 * 上游：rbac/modules/studio/registry.ts
 * 下游：rbac/core/evaluate.ts
 * 关联：rbac/contracts/README.md
 */

    import {
      MODULE_PERMISSIONS as STUDIO_MODULE_PERMISSIONS,
      RBAC_DOMAIN as STUDIO_DOMAIN,
      ROLE_PERMISSIONS as STUDIO_ROLE_PERMISSIONS,
    } from "@/rbac/modules/studio/registry";

    export const RBAC_DOMAINS = [STUDIO_DOMAIN] as const;

    /** 合并各域 module-id → permission（首期仅 studio）。 */
    export const MODULE_PERMISSIONS: Record<string, string> = {
      ...STUDIO_MODULE_PERMISSIONS,
    };

    /** 合并各域 role → permissions（首期仅 studio）。 */
    export function getRolePermissions(role: string): readonly string[] {
      return STUDIO_ROLE_PERMISSIONS[role] ?? [];
    }
