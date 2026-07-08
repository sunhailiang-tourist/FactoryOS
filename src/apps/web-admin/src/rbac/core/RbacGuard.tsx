/**
 * 模块：src/apps/web-admin/src/rbac/core/RbacGuard.tsx
 * 作用：域级 / 路由级 RBAC UI 守卫
 * 怎么用：layout 包 domain；路由包 permissions
 * 解决：替代 studio-rbac.guard 硬编码
 * 上游：getActorContext · rbac/core/evaluate.ts
 * 下游：StudioShellLayout · 未来路由 wrapper
 * 关联：i18n _platform rbacDenied
 */

import Alert from "@mui/material/Alert";
import type { ReactNode } from "react";
import { getActorContext } from "@/api/request";
import { useT } from "@/i18n/core/useT";
import { I18N_PLATFORM_NAMESPACE } from "@/i18n/registry";
import { canAccessDomain, canAccessRoute } from "@/rbac/core/evaluate";
import type { Permission, PermissionMode } from "@/rbac/core/types";

type RbacGuardProps = {
  children: ReactNode;
  /** 域级：如 studio → 须拥有任一 studio.* 权限 */
  domain?: string;
  /** 路由级：显式权限列表 */
  permissions?: readonly Permission[];
  permissionsMode?: PermissionMode;
  role?: string;
};

/**
 * 功能：按 domain 或 permissions 渲染子树或拒绝提示。
 * 业务含义：layout/路由 RBAC UI 守卫。
 * 上游：getActorContext · canAccessDomain · canAccessRoute。
 * 下游：StudioShellLayout · 路由 wrapper。
 */
export function RbacGuard({
  children,
  domain,
  permissions,
  permissionsMode = "all",
  role: roleProp,
}: RbacGuardProps) {
  // 业务：解析角色并依次校验域级、路由级权限
  const { t } = useT(I18N_PLATFORM_NAMESPACE);
  const role = roleProp ?? getActorContext().role;

  if (domain && !canAccessDomain(role, domain)) {
    return (
      <Alert severity="error" role="alert">
        {t("rbacDenied", { role })}
      </Alert>
    );
  }

  if (permissions && !canAccessRoute(role, permissions, permissionsMode)) {
    return (
      <Alert severity="error" role="alert">
        {t("rbacRouteDenied", { permissions: permissions.join(", ") })}
      </Alert>
    );
  }

  return <>{children}</>;
}
