/**
 * 模块：src/apps/web-admin/src/layout/modules/studio/StudioShellLayout.tsx
 * 作用：Integration Studio 壳布局（响应式侧栏 + 动画 Outlet）
 * 怎么用：layout/modules/studio/registry 登记 component
 * 解决：六步向导统一导航 · 移动端 drawer · 预取
 * 上游：router/loaders · StudioAnimatedOutlet
 * 下游：pages studio 系列 · rbac/core/RbacGuard
 * 关联：ENGINEERING.md §10 S4
 */
import MenuIcon from "@mui/icons-material/Menu";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import Drawer from "@mui/material/Drawer";
import IconButton from "@mui/material/IconButton";
import Toolbar from "@mui/material/Toolbar";
import Typography from "@mui/material/Typography";
import useMediaQuery from "@mui/material/useMediaQuery";
import { useTheme } from "@mui/material/styles";
import { Suspense, useState } from "react";
import { getActorContext } from "@/api/request";
import { StudioSidebarSkeleton } from "@/components/skeletons";
import { StudioAnimatedOutlet } from "./StudioAnimatedOutlet";
import { StudioShellSidebar } from "./StudioShellSidebar";
import { useT } from "@/i18n/core/useT";
import { I18N_PLATFORM_NAMESPACE } from "@/i18n/registry";
import { RbacGuard } from "@/rbac/core/RbacGuard";
import { RBAC_DOMAIN } from "@/rbac/modules/studio/registry";

const DRAWER_WIDTH = 280;

export function StudioShellLayout() {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("md"));
  const [mobileOpen, setMobileOpen] = useState(false);
  const actorRole = getActorContext().role;
  const { t } = useT(I18N_PLATFORM_NAMESPACE);

  const drawer = (
    <Box role="presentation" onClick={() => isMobile && setMobileOpen(false)}>
      <Toolbar>
        <Typography variant="h6" component="div" noWrap>
          {t("appTitle")}
        </Typography>
      </Toolbar>
      <Suspense fallback={<StudioSidebarSkeleton />}>
        <StudioShellSidebar />
      </Suspense>
    </Box>
  );

  return (
    <RbacGuard domain={RBAC_DOMAIN} role={actorRole}>
      <Box display="flex" minHeight="100vh">
        {isMobile ? (
          <AppBar position="fixed" color="default" elevation={0} sx={{ zIndex: theme.zIndex.drawer + 1 }}>
            <Toolbar>
              <IconButton edge="start" onClick={() => setMobileOpen(true)} aria-label={t("openNav")}>
                <MenuIcon />
              </IconButton>
              <Typography variant="h6" noWrap component="div">
                {t("studioTitle")}
              </Typography>
            </Toolbar>
          </AppBar>
        ) : null}
        <Drawer
          variant={isMobile ? "temporary" : "permanent"}
          open={isMobile ? mobileOpen : true}
          onClose={() => setMobileOpen(false)}
          ModalProps={{ keepMounted: true }}
          sx={{
            width: DRAWER_WIDTH,
            flexShrink: 0,
            "& .MuiDrawer-paper": { width: DRAWER_WIDTH, boxSizing: "border-box" },
          }}
        >
          {drawer}
        </Drawer>
        <Box
          component="main"
          flexGrow={1}
          p={3}
      sx={isMobile ? { mt: 8, width: "100%" } : undefined}
    >
      <StudioAnimatedOutlet />
    </Box>
      </Box>
    </RbacGuard>
  );
}
