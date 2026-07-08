/**
 * 模块：src/apps/web-admin/src/layout/modules/studio/StudioShellSidebar.tsx
 * 作用：Studio 侧栏内容（Suspense 内）
 * 怎么用：StudioShellLayout Drawer 内 Suspense child
 * 解决：侧栏与 flows 数据解耦渲染时机
 * 上游：useStudioFlowsSuspense
 * 下游：StudioNavLink
 * 关联：layout/modules/studio
 */
import ChevronRightIcon from "@mui/icons-material/ChevronRight";
import List from "@mui/material/List";
import Typography from "@mui/material/Typography";
import { useLocation } from "react-router-dom";
import { useStudioFlowsSuspense } from "@/api/query/hooks/useStudioFlowsSuspense";
import { useT } from "@/i18n/core/useT";
import { I18N_PLATFORM_NAMESPACE } from "@/i18n/registry";
import { can } from "@/rbac/core/evaluate";
import { permissionsForModule } from "@/rbac/core/evaluate";
import { getActorContext } from "@/api/request";
import { StudioNavLink } from "@/router/StudioNavLink";

function stepHref(stepId: string, explicitPath?: string): string {
  if (explicitPath) return explicitPath;
  return `/studio/${stepId}`;
}

const STEP_MODULE_IDS: Record<string, string> = {
  connect: "studio-connect",
  discover: "studio-discover",
  map: "studio-map",
  prove: "studio-prove",
  freeze: "studio-freeze",
  export: "studio-export",
};

/**
 * 功能：StudioShellSidebar 导出函数。
 * 业务含义：web-admin 模块对外入口。
 * 上游：同文件文件头。
 * 下游：见调用链。
 */
export function StudioShellSidebar() {
  // 业务：StudioShellSidebar 主体编排（见文件头上下游）
  const location = useLocation();
  const { t } = useT(I18N_PLATFORM_NAMESPACE);
  const role = getActorContext().role;
  const { data } = useStudioFlowsSuspense();
  const steps = data.steps ?? [];

  return (
    <>
      <Typography variant="h6" component="div" sx={{ px: 2, pt: 1 }} noWrap>
        {data.title ?? t("studioTitle")}
      </Typography>
      <Typography variant="body2" color="text.secondary" sx={{ px: 2, pb: 1 }}>
        {t("studioSubtitle")}
      </Typography>
      <List component="nav" aria-label={t("studioNavAria")}>
        {can(role, "studio.shell.view") ? (
          <StudioNavLink
            to="/studio"
            selected={location.pathname === "/studio"}
            primary={t("studioNavOverview")}
            secondary="studio.home"
            moduleId="studio-shell"
          />
        ) : null}
        {steps.map((step) => {
          const moduleId = STEP_MODULE_IDS[step.id];
          const perms = permissionsForModule(moduleId);
          if (perms.length && !can(role, perms[0])) return null;
          const to = stepHref(step.id, step.path);
          return (
            <StudioNavLink
              key={step.id}
              to={to}
              selected={location.pathname === to}
              primary={`${step.order}. ${step.title}`}
              secondary={step.summary}
              moduleId={moduleId}
              endAdornment={<ChevronRightIcon fontSize="small" />}
            />
          );
        })}
      </List>
    </>
  );
}
