#!/usr/bin/env python3
"""WEB-PROFILE S4 性能优化一步到位落盘（P0～P2 + P3 无 SSR）。"""
from __future__ import annotations

import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "src/apps/web-admin"


def w(rel: str, content: str) -> None:
  path = APP / rel
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")
  print("wrote", path.relative_to(ROOT))


def patch(rel: str, old: str, new: str) -> None:
  path = APP / rel
  text = path.read_text(encoding="utf-8")
  if old not in text:
    if new.strip() in text:
      return
    raise SystemExit(f"patch miss {rel}: {old[:60]!r}")
  path.write_text(text.replace(old, new, 1), encoding="utf-8")
  print("patched", rel)


def main() -> int:
  # ── P0: 首屏壳 ──
  w(
    "index.html",
    """
    <!doctype html>
    <html lang="zh-CN">
      <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>FactoryOS · Integration Studio</title>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
        <link
          rel="stylesheet"
          href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap"
        />
        <style>
          :root {
            --fos-boot-bg: #f4f6f8;
            --fos-boot-sidebar: #ffffff;
            --fos-boot-primary: #1565c0;
            --fos-boot-muted: #5c6b7a;
          }
          html, body { margin: 0; min-height: 100%; background: var(--fos-boot-bg); }
          #fos-boot-shell {
            display: flex;
            min-height: 100vh;
            font-family: Roboto, system-ui, sans-serif;
          }
          #fos-boot-shell .fos-boot-sidebar {
            width: 280px;
            background: var(--fos-boot-sidebar);
            border-right: 1px solid #e0e6ed;
            padding: 16px;
            box-sizing: border-box;
          }
          #fos-boot-shell .fos-boot-title {
            height: 20px;
            width: 70%;
            border-radius: 4px;
            background: linear-gradient(90deg, #e8edf2 25%, #f5f7fa 50%, #e8edf2 75%);
            background-size: 200% 100%;
            animation: fos-shimmer 1.2s ease-in-out infinite;
            margin-bottom: 12px;
          }
          #fos-boot-shell .fos-boot-line {
            height: 12px;
            border-radius: 4px;
            margin: 10px 0;
            background: linear-gradient(90deg, #e8edf2 25%, #f5f7fa 50%, #e8edf2 75%);
            background-size: 200% 100%;
            animation: fos-shimmer 1.2s ease-in-out infinite;
          }
          #fos-boot-shell .fos-boot-main {
            flex: 1;
            padding: 24px;
          }
          #fos-boot-shell .fos-boot-card {
            max-width: 720px;
            height: 160px;
            border-radius: 8px;
            border: 1px solid #e0e6ed;
            background: #fff;
          }
          #fos-boot-shell .fos-boot-brand {
            font-size: 13px;
            color: var(--fos-boot-muted);
            margin-bottom: 16px;
          }
          @keyframes fos-shimmer {
            0% { background-position: 200% 0; }
            100% { background-position: -200% 0; }
          }
          @media (max-width: 900px) {
            #fos-boot-shell .fos-boot-sidebar { width: 0; padding: 0; overflow: hidden; }
          }
        </style>
      </head>
      <body>
        <div id="root">
          <div id="fos-boot-shell" aria-hidden="true">
            <aside class="fos-boot-sidebar">
              <div class="fos-boot-brand">FactoryOS</div>
              <div class="fos-boot-title"></div>
              <div class="fos-boot-line" style="width:90%"></div>
              <div class="fos-boot-line" style="width:80%"></div>
              <div class="fos-boot-line" style="width:85%"></div>
              <div class="fos-boot-line" style="width:75%"></div>
            </aside>
            <main class="fos-boot-main">
              <div class="fos-boot-card"></div>
            </main>
          </div>
        </div>
        <script type="module" src="/src/main.tsx"></script>
      </body>
    </html>
    """,
  )

  w(
    ".env.development",
    """
    # 本地零后端默认启 MSW（WEB-PROFILE S4 · P0）
    VITE_MSW=1
    """,
  )

  # ── P0: Skeletons + Route error ──
  w(
    "src/components/skeletons/StudioSidebarSkeleton.tsx",
    """
    /**
     * 模块：src/apps/web-admin/src/components/skeletons/StudioSidebarSkeleton.tsx
     * 作用：Studio 侧栏骨架 — 固定尺寸防 CLS
     * 怎么用：StudioShellLayout Suspense fallback
     * 解决：侧栏加载转圈 → 布局级骨架
     * 上游：layout/modules/studio
     * 下游：useStudioFlowsSuspense
     * 关联：ENGINEERING.md §10 S4
     */
    import Skeleton from "@mui/material/Skeleton";
    import Stack from "@mui/material/Stack";

    export function StudioSidebarSkeleton() {
      return (
        <Stack spacing={1.5} sx={{ px: 2, py: 1 }} aria-label="加载侧栏">
          <Skeleton variant="text" width="70%" height={28} />
          <Skeleton variant="text" width="90%" />
          {Array.from({ length: 6 }).map((_, i) => (
            <Skeleton key={i} variant="rounded" height={48} />
          ))}
        </Stack>
      );
    }
    """,
  )

  w(
    "src/components/skeletons/PageContentSkeleton.tsx",
    """
    /**
     * 模块：src/apps/web-admin/src/components/skeletons/PageContentSkeleton.tsx
     * 作用：主内容区卡片骨架
     * 怎么用：Outlet Suspense fallback · 页面 isLoading
     * 解决：内容区白屏/转圈 → 卡片轮廓
     * 上游：StudioAnimatedOutlet
     * 下游：pages/*
     * 关联：ENGINEERING.md §10 S4
     */
    import Card from "@mui/material/Card";
    import CardContent from "@mui/material/CardContent";
    import Skeleton from "@mui/material/Skeleton";
    import Stack from "@mui/material/Stack";

    export function PageContentSkeleton() {
      return (
        <Card variant="outlined" sx={{ maxWidth: 720 }} aria-label="加载页面内容">
          <CardContent>
            <Stack spacing={1.5}>
              <Skeleton variant="text" width="55%" height={40} />
              <Skeleton variant="text" width="90%" />
              <Skeleton variant="text" width="80%" />
              <Skeleton variant="rounded" height={36} width={160} />
            </Stack>
          </CardContent>
        </Card>
      );
    }
    """,
  )

  w(
    "src/components/skeletons/index.ts",
    """
    /**
     * 模块：src/apps/web-admin/src/components/skeletons/index.ts
     * 作用：骨架组件统一导出
     * 怎么用：import { PageContentSkeleton } from '@/components/skeletons'
     * 解决：加载态组件单点
     * 上游：skeletons/*
     * 下游：layout · pages
     * 关联：ENGINEERING.md §10
     */
    export { PageContentSkeleton } from "./PageContentSkeleton";
    export { StudioSidebarSkeleton } from "./StudioSidebarSkeleton";
    """,
  )

  w(
    "src/components/RouteErrorFallback.tsx",
    """
    /**
     * 模块：src/apps/web-admin/src/components/RouteErrorFallback.tsx
     * 作用：路由 errorElement — lazy/load 失败降级
     * 怎么用：browser-router Route errorElement
     * 解决：chunk 失败白屏 → 可重试 UI
     * 上游：react-router useRouteError
     * 下游：用户重试导航
     * 关联：ENGINEERING.md §10 S4
     */
    import Alert from "@mui/material/Alert";
    import Box from "@mui/material/Box";
    import Button from "@mui/material/Button";
    import Typography from "@mui/material/Typography";
    import { isRouteErrorResponse, useRouteError } from "react-router-dom";

    export function RouteErrorFallback() {
      const error = useRouteError();
      const message = isRouteErrorResponse(error)
        ? `${error.status} ${error.statusText}`
        : error instanceof Error
          ? error.message
          : "页面加载失败";

      return (
        <Box p={3} maxWidth={560}>
          <Alert severity="error" sx={{ mb: 2 }}>
            {message}
          </Alert>
          <Typography variant="body2" color="text.secondary" paragraph>
            可能是网络中断或代码分包加载失败。请重试或返回 Studio 概览。
          </Typography>
          <Button variant="contained" onClick={() => window.location.assign("/studio")}>
            返回概览
          </Button>
          <Button sx={{ ml: 1 }} onClick={() => window.location.reload()}>
            重新加载
          </Button>
        </Box>
      );
    }
    """,
  )

  # ── P1: loaders + prefetch ──
  w(
    "src/router/loaders.ts",
    """
    /**
     * 模块：src/apps/web-admin/src/router/loaders.ts
     * 作用：RR loader 工厂 — QueryClient ensureQueryData
     * 怎么用：browser-router studio layout loader
     * 解决：进壳前预取 flows，减少侧栏 spinner
     * 上游：QueryClient · getStudioFlows
     * 下游：StudioShellLayout
     * 关联：ENGINEERING.md §10 S4
     */
    import type { QueryClient } from "@tanstack/react-query";
    import { getStudioFlows } from "@/api/functions/studio-shell";
    import { studioKeys } from "@/api/query/keys";

    export function createStudioFlowsLoader(queryClient: QueryClient) {
      return async () => {
        await queryClient.ensureQueryData({
          queryKey: studioKeys.flows(),
          queryFn: getStudioFlows,
        });
        return null;
      };
    }
    """,
  )

  w(
    "src/router/prefetch.ts",
    """
    /**
     * 模块：src/apps/web-admin/src/router/prefetch.ts
     * 作用：导航意图预取 — Query + route chunk
     * 怎么用：StudioNavLink onMouseEnter / onFocus
     * 解决：切页 P95 感知延迟
     * 上游：ROUTE_REGISTRY · QueryClient
     * 下游：侧栏 Link
     * 关联：ENGINEERING.md §10 S4
     */
    import type { QueryClient } from "@tanstack/react-query";
    import { getStudioFlows } from "@/api/functions/studio-shell";
    import { studioKeys } from "@/api/query/keys";
    import { ROUTE_REGISTRY } from "@/router/registry";

    export function prefetchStudioFlows(queryClient: QueryClient): void {
      void queryClient.prefetchQuery({
        queryKey: studioKeys.flows(),
        queryFn: getStudioFlows,
      });
    }

    export function prefetchRouteChunk(moduleId: string): void {
      const entry = ROUTE_REGISTRY.find((r) => r.moduleId === moduleId);
      if (entry) {
        void entry.lazy();
      }
    }

    export function prefetchStudioNavigation(
      queryClient: QueryClient,
      moduleId?: string,
    ): void {
      prefetchStudioFlows(queryClient);
      if (moduleId) {
        prefetchRouteChunk(moduleId);
      }
    }
    """,
  )

  w(
    "src/router/StudioNavLink.tsx",
    """
    /**
     * 模块：src/apps/web-admin/src/router/StudioNavLink.tsx
     * 作用：侧栏导航 Link + hover/focus 预取
     * 怎么用：StudioShellLayout 步骤列表
     * 解决：意图预取 flows 与 lazy chunk
     * 上游：prefetch.ts · QueryClient
     * 下游：react-router Link
     * 关联：ENGINEERING.md §10 S4
     */
    import ListItemButton from "@mui/material/ListItemButton";
    import ListItemText from "@mui/material/ListItemText";
    import type { ReactNode } from "react";
    import { Link } from "react-router-dom";
    import { useQueryClient } from "@tanstack/react-query";
    import { prefetchStudioNavigation } from "@/router/prefetch";

    type StudioNavLinkProps = {
      to: string;
      selected: boolean;
      primary: ReactNode;
      secondary?: ReactNode;
      moduleId?: string;
      endAdornment?: ReactNode;
      disabled?: boolean;
    };

    export function StudioNavLink({
      to,
      selected,
      primary,
      secondary,
      moduleId,
      endAdornment,
      disabled,
    }: StudioNavLinkProps) {
      const queryClient = useQueryClient();
      const prefetch = () => prefetchStudioNavigation(queryClient, moduleId);

      return (
        <ListItemButton
          component={Link}
          to={to}
          selected={selected}
          disabled={disabled}
          onMouseEnter={prefetch}
          onFocus={prefetch}
        >
          <ListItemText primary={primary} secondary={secondary} />
          {endAdornment}
        </ListItemButton>
      );
    }
    """,
  )

  w(
    "src/layout/modules/studio/StudioAnimatedOutlet.tsx",
    """
    /**
     * 模块：src/apps/web-admin/src/layout/modules/studio/StudioAnimatedOutlet.tsx
     * 作用：Outlet 内容区过渡 + 嵌套 Suspense
     * 怎么用：StudioShellLayout main 区
     * 解决：步间硬切 → motion + skeleton
     * 上游：MotionContainer · styles/motion
     * 下游：pages lazy
     * 关联：ENGINEERING.md §10 S4
     */
    import { Suspense } from "react";
    import { Outlet, useLocation } from "react-router-dom";
    import { PageContentSkeleton } from "@/components/skeletons";
    import { MotionContainer } from "@/styles/motion";

    export function StudioAnimatedOutlet() {
      const location = useLocation();
      return (
        <MotionContainer
          key={location.pathname}
          preset="enter"
          className="fos-studio-outlet"
        >
          <Suspense fallback={<PageContentSkeleton />}>
            <Outlet />
          </Suspense>
        </MotionContainer>
      );
    }
    """,
  )

  w(
    "src/api/query/hooks/useStudioFlowsSuspense.ts",
    """
    /**
     * 模块：src/apps/web-admin/src/api/query/hooks/useStudioFlowsSuspense.ts
     * 作用：Studio flows Suspense Query hook
     * 怎么用：layout Suspense 边界内组件
     * 解决：壳先出 + 数据流式填
     * 上游：getStudioFlows · studioKeys
     * 下游：StudioShellSidebar
     * 关联：ENGINEERING.md §10 S4
     */
    import { useSuspenseQuery } from "@tanstack/react-query";
    import { getStudioFlows } from "@/api/functions/studio-shell";
    import { studioKeys } from "@/api/query/keys";

    export function useStudioFlowsSuspense() {
      return useSuspenseQuery({
        queryKey: studioKeys.flows(),
        queryFn: getStudioFlows,
      });
    }
    """,
  )

  w(
    "src/layout/modules/studio/StudioShellSidebar.tsx",
    """
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

    export function StudioShellSidebar() {
      const location = useLocation();
      const { data } = useStudioFlowsSuspense();
      const steps = data.steps ?? [];

      return (
        <>
          <Typography variant="h6" component="div" sx={{ px: 2, pt: 1 }} noWrap>
            {data.title ?? "Integration Studio"}
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ px: 2, pb: 1 }}>
            新客户接入 · 六步向导（零仓库主路径）
          </Typography>
          <List component="nav" aria-label="Studio 六步">
            <StudioNavLink
              to="/studio"
              selected={location.pathname === "/studio"}
              primary="概览"
              secondary="studio.home"
              moduleId="studio-shell"
            />
            {steps.map((step) => {
              const to = stepHref(step.id, step.path);
              return (
                <StudioNavLink
                  key={step.id}
                  to={to}
                  selected={location.pathname === to}
                  primary={`${step.order}. ${step.title}`}
                  secondary={step.summary}
                  moduleId={STEP_MODULE_IDS[step.id]}
                  endAdornment={<ChevronRightIcon fontSize="small" />}
                />
              );
            })}
          </List>
        </>
      );
    }
    """,
  )

  w(
    "src/layout/modules/studio/StudioShellLayout.tsx",
    """
    /**
     * 模块：src/apps/web-admin/src/layout/modules/studio/StudioShellLayout.tsx
     * 作用：Integration Studio 壳布局（响应式侧栏 + 动画 Outlet）
     * 怎么用：layout/modules/studio/registry 登记 component
     * 解决：六步向导统一导航 · 移动端 drawer · 预取
     * 上游：router/loaders · StudioAnimatedOutlet
     * 下游：pages studio 系列 · router/guards/studio-rbac.guard
     * 关联：ENGINEERING.md §10 S4
     */
    import MenuIcon from "@mui/icons-material/Menu";
    import Alert from "@mui/material/Alert";
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
    import { StudioRbacGuard } from "@/router/guards/studio-rbac.guard";

    const DRAWER_WIDTH = 280;

    export function StudioShellLayout() {
      const theme = useTheme();
      const isMobile = useMediaQuery(theme.breakpoints.down("md"));
      const [mobileOpen, setMobileOpen] = useState(false);
      const actorRole = getActorContext().role;

      const drawer = (
        <Box role="presentation" onClick={() => isMobile && setMobileOpen(false)}>
      <Toolbar>
        <Typography variant="h6" component="div" noWrap>
          FactoryOS
        </Typography>
      </Toolbar>
          <Suspense fallback={<StudioSidebarSkeleton />}>
            <StudioShellSidebar />
          </Suspense>
        </Box>
      );

      return (
        <StudioRbacGuard role={actorRole}>
          <Box display="flex" minHeight="100vh">
            {isMobile ? (
              <AppBar position="fixed" color="default" elevation={0} sx={{ zIndex: theme.zIndex.drawer + 1 }}>
                <Toolbar>
                  <IconButton edge="start" onClick={() => setMobileOpen(true)} aria-label="打开导航">
                    <MenuIcon />
                  </IconButton>
                  <Typography variant="h6" noWrap component="div">
                    Integration Studio
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
        </StudioRbacGuard>
      );
    }
    """,
  )

  # Fix LayoutFlowsError - using useRouteError outside error boundary is wrong. Remove that hack.
  # I'll patch StudioShellLayout to remove LayoutFlowsError - loader handles data, sidebar suspense handles loading

  layout_content = (APP / "src/layout/modules/studio/StudioShellLayout.tsx").read_text(encoding="utf-8")
  layout_content = layout_content.replace(
    """    import { Suspense, useState } from "react";
    import { useRouteError } from "react-router-dom";
""",
    """    import { Suspense, useState } from "react";
""",
  )
  layout_content = layout_content.replace(
    """    function LayoutFlowsError() {
      const error = useRouteError();
      const message = error instanceof Error ? error.message : "无法加载向导";
      return (
        <Alert severity="error" sx={{ mx: 2, mb: 1 }}>
          无法加载向导：{message}
        </Alert>
      );
    }

    """,
    "",
  )
  layout_content = layout_content.replace(
    """              <Suspense fallback={null}>
                <LayoutFlowsError />
              </Suspense>
              <StudioAnimatedOutlet />
""",
    """              <StudioAnimatedOutlet />
""",
  )
  layout_content = layout_content.replace('import Alert from "@mui/material/Alert";\n', "")
  (APP / "src/layout/modules/studio/StudioShellLayout.tsx").write_text(layout_content, encoding="utf-8")

  w(
    "src/router/browser-router.tsx",
    """
    /**
     * 模块：src/apps/web-admin/src/router/browser-router.tsx
     * 作用：createBrowserRouter 工厂 — loader · errorElement · lazy
     * 怎么用：bootstrap createAppRouter(queryClient)
     * 解决：数据预取 + 路由错误降级 + Route.lazy
     * 上游：layout/registry · router/registry · loaders
     * 下游：bootstrap.tsx
     * 关联：ENGINEERING.md §10 S4
     */
    import type { QueryClient } from "@tanstack/react-query";
    import {
      createBrowserRouter,
      createRoutesFromElements,
      Navigate,
      Route,
    } from "react-router-dom";
    import { RouteErrorFallback } from "@/components/RouteErrorFallback";
    import { RootLayout } from "@/layout/RootLayout";
    import { LAYOUT_REGISTRY } from "@/layout/registry";
    import { createStudioFlowsLoader } from "@/router/loaders";
    import { getRoutesByLayout } from "@/router/registry";

    export function createAppRouter(queryClient: QueryClient) {
      const studioFlowsLoader = createStudioFlowsLoader(queryClient);
      return createBrowserRouter(
        createRoutesFromElements(
          <Route element={<RootLayout />} errorElement={<RouteErrorFallback />}>
            <Route path="/" element={<Navigate to="/studio" replace />} />
            {LAYOUT_REGISTRY.map((layout) => {
              const LayoutComponent = layout.component;
              const routes = getRoutesByLayout(layout.id);
              const layoutLoader = layout.id === "studio" ? studioFlowsLoader : undefined;
              return (
                <Route
                  key={layout.id}
                  path={layout.pathPrefix}
                  element={<LayoutComponent />}
                  loader={layoutLoader}
                  errorElement={<RouteErrorFallback />}
                >
                  {routes.map((route) =>
                    route.index ? (
                      <Route
                        key={route.name}
                        index
                        lazy={route.lazy}
                        errorElement={<RouteErrorFallback />}
                      />
                    ) : (
                      <Route
                        key={route.name}
                        path={route.path}
                        lazy={route.lazy}
                        errorElement={<RouteErrorFallback />}
                      />
                    ),
                  )}
                </Route>
              );
            })}
          </Route>,
        ),
      );
    }
    """,
  )

  w(
    "src/bootstrap.tsx",
    """
    /**
     * 模块：src/apps/web-admin/src/bootstrap.tsx
     * 作用：Provider 树 + RouterProvider（Query 与 router 同生命周期）
     * 怎么用：main.tsx 唯一 import
     * 解决：loader 可访问 QueryClient；全局 Suspense
     * 上游：main.tsx
     * 下游：AppThemeProvider · createAppRouter
     * 关联：ENGINEERING.md §10 S4
     */
    import { QueryClientProvider } from "@tanstack/react-query";
    import { Suspense, useState } from "react";
    import { RouterProvider } from "react-router-dom";
    import { AppThemeProvider } from "@/components/AppThemeProvider";
    import { PageLoading } from "@/components/PageLoading";
    import { createQueryClient } from "@/api/query/client";
    import { createAppRouter } from "@/router/browser-router";

    export function Bootstrap() {
      const [queryClient] = useState(() => createQueryClient());
      const [router] = useState(() => createAppRouter(queryClient));

      return (
        <QueryClientProvider client={queryClient}>
          <AppThemeProvider>
            <Suspense fallback={<PageLoading />}>
              <RouterProvider router={router} />
            </Suspense>
          </AppThemeProvider>
        </QueryClientProvider>
      );
    }
    """,
  )

  w(
    "src/AppShell.tsx",
    """
    /**
     * 模块：src/apps/web-admin/src/AppShell.tsx
     * 作用：兼容导出 — 路由已迁至 bootstrap（S4）
     * 怎么用：测试/Storybook 可继续 import createAppRouter
     * 解决：避免双 RouterProvider
     * 上游：bootstrap.tsx
     * 下游：browser-router.test
     * 关联：ARCHITECTURE.md §2
     */
    export { Bootstrap as AppShell } from "@/bootstrap";
    """,
  )

  w(
    "src/main.tsx",
    """
    /**
     * 模块：src/apps/web-admin/src/main.tsx
     * 作用：Vite 应用入口，挂载 React 根
     * 怎么用：pnpm dev（.env.development 默认 VITE_MSW=1）
     * 解决：首屏 boot shell → React 接管无白屏
     * 上游：index.html · Vite · mocks/browser.ts
     * 下游：bootstrap.tsx
     * 关联：ENGINEERING.md §10 S4
     */
    import { StrictMode } from "react";
    import { createRoot } from "react-dom/client";
    import "@/styles/global.css";
    import { Bootstrap } from "@/bootstrap";

    async function enableMswWhenRequested(): Promise<void> {
      if (import.meta.env.VITE_MSW !== "1") {
        return;
      }
      const { worker } = await import("@/mocks/browser");
      await worker.start({ onUnhandledRequest: "bypass", quiet: true });
    }

    function clearBootShell(): void {
      document.getElementById("fos-boot-shell")?.remove();
    }

    function mountApp(): void {
      const root = document.getElementById("root");
      if (!root) {
        throw new Error("root element #root not found");
      }
      clearBootShell();
      createRoot(root).render(
        <StrictMode>
          <Bootstrap />
        </StrictMode>,
      );
    }

    async function bootstrap(): Promise<void> {
      await enableMswWhenRequested();
      mountApp();
    }

    void bootstrap();
    """,
  )

  w(
    "src/pages/studio-shell/StudioHomePage.lazy.tsx",
    """
    /**
     * 模块：src/apps/web-admin/src/pages/studio-shell/StudioHomePage.lazy.tsx
     * 作用：Studio 概览 lazy 页面入口
     * 怎么用：router/modules/studio-shell/registry.ts lazy import
     * 解决：flows 已由 layout loader 预取，直接渲染卡片
     * 上游：useStudioFlowsSuspense
     * 下游：store/modules/studio-shell
     * 关联：pages/studio-shell/contracts/README.md
     */
    import Card from "@mui/material/Card";
    import CardContent from "@mui/material/CardContent";
    import Typography from "@mui/material/Typography";
    import { Suspense } from "react";
    import { useStudioFlowsSuspense } from "@/api/query/hooks/useStudioFlowsSuspense";
    import { PageContentSkeleton } from "@/components/skeletons";
    import { MotionContainer } from "@/styles/motion";
    import styles from "./styles/home.module.css";

    function StudioHomeContent() {
      const { data } = useStudioFlowsSuspense();
      const title = data.title ?? "Integration Studio";
      const stepCount = data.steps?.length ?? 0;

      return (
        <MotionContainer preset="enterUp" className={`${styles.pageShell} mx-auto p-6`}>
          <Card variant="outlined" className="shadow-fos-sm">
            <CardContent>
              <Typography variant="h4" gutterBottom className={styles.heroTitle}>
                {title}
              </Typography>
              <Typography variant="body1" color="text.secondary" paragraph>
                从左侧选择六步向导步骤，完成新客户零仓库接入。
              </Typography>
              <span className={styles.stepBadge}>已注册 {stepCount} 个向导步骤</span>
            </CardContent>
          </Card>
        </MotionContainer>
      );
    }

    export default function StudioHomePage() {
      return (
        <Suspense fallback={<PageContentSkeleton />}>
          <StudioHomeContent />
        </Suspense>
      );
    }
    """,
  )

  w(
    "src/mocks/handlers/studio-connect.ts",
    """
    /**
     * 模块：src/apps/web-admin/src/mocks/handlers/studio-connect.ts
     * 作用：studio-connect MSW — POST connect/test
     * 怎么用：handlers/index.ts 聚合
     * 解决：零后端 Connect 步可演示
     * 上游：api/functions/studio-connect/connect.fn.ts
     * 下游：mocks/server.ts
     * 关联：pages/studio-connect/contracts/README.md
     */
    import { http, HttpResponse } from "msw";

    export const studioConnectHandlers = [
      http.post("/v1/integration/connect/test", async () => {
        return HttpResponse.json({ ok: true, message: "MSW: connect ping ok" });
      }),
    ];
    """,
  )

  w(
    "src/mocks/handlers/studio-stubs.ts",
    """
    /**
     * 模块：src/apps/web-admin/src/mocks/handlers/studio-stubs.ts
     * 作用：Studio 其余步骤占位 MSW（待业务 API 落地替换）
     * 怎么用：handlers/index.ts 聚合
     * 解决：dev 未实现端点 bypass 前占位 501
     * 上游：pages studio-discover..export
     * 下游：mocks/server.ts
     * 关联：ENGINEERING.md §10
     */
    import { http, HttpResponse } from "msw";

    const STUB_PATHS = [
      "/v1/integration/discover/validate",
      "/v1/integration/map/preview",
      "/v1/integration/prove/run",
      "/v1/integration/freeze/submit",
      "/v1/integration/export/package",
    ];

    export const studioStubHandlers = STUB_PATHS.map((path) =>
      http.all(path, () =>
        HttpResponse.json(
          { ok: true, stub: true, message: `MSW stub for ${path}` },
          { status: 200 },
        ),
      ),
    );
    """,
  )

  w(
    "src/mocks/handlers/index.ts",
    """
    /**
     * 模块：src/apps/web-admin/src/mocks/handlers/index.ts
     * 作用：MSW handlers 聚合入口
     * 怎么用：mocks/server.ts import handlers
     * 解决：按 module-id 扩展 handler 文件
     * 上游：handlers/studio-*.ts
     * 下游：mocks/server.ts · mocks/browser.ts
     * 关联：ENGINEERING.md §10 S4
     */
    import { studioConnectHandlers } from "./studio-connect";
    import { studioShellHandlers } from "./studio-shell";
    import { studioStubHandlers } from "./studio-stubs";

    export const handlers = [
      ...studioShellHandlers,
      ...studioConnectHandlers,
      ...studioStubHandlers,
    ];
    """,
  )

  w(
    "src/components/charts/index.ts",
    """
    /**
     * 模块：src/apps/web-admin/src/components/charts/index.ts
     * 作用：charts 懒加载导出（S4 · 重组件分包）
     * 怎么用：import { LineChart } from '@/components/charts'（React.lazy）
     * 解决：未用图表时不拉 vendor-echarts
     * 上游：LineChart · BarChart lazy
     * 下游：业务 pages
     * 关联：components/charts/contracts/README.md
     */
    import { lazy } from "react";

    export const LineChart = lazy(() =>
      import("./LineChart").then((m) => ({ default: m.LineChart })),
    );
    export const BarChart = lazy(() =>
      import("./BarChart").then((m) => ({ default: m.BarChart })),
    );
    export type { BarChartProps } from "./BarChart";
    export type { BaseChartProps } from "./BaseChart";
    export type { LineChartProps } from "./LineChart";
    export { BaseChart } from "./BaseChart";
    export { ensureEchartsRegistered } from "./register";
    """,
  )

  w(
    "scripts/check_resource_chain.py",
    """
    #!/usr/bin/env python3
    # web-admin 资源链路三角对账 — module-id · route.name · api.id · MSW path
    from __future__ import annotations

    import re
    import sys
    from pathlib import Path

    APP = Path(__file__).resolve().parents[1]
    SRC = APP / "src"

    API_ENTRY = re.compile(
      r'id:\\s*"([^"]+)".*?module:\\s*"([^"]+)".*?routeName:\\s*"([^"]+)".*?path:\\s*"([^"]+)"',
      re.DOTALL,
    )
    ROUTE_ENTRY = re.compile(
      r'name:\\s*"([^"]+)".*?moduleId:\\s*"([^"]+)"',
      re.DOTALL,
    )
    CONTRACT_API = re.compile(r"api id\\s*\\|\\s*`([^`]+)`")
    CONTRACT_ROUTE = re.compile(r"route name\\s*\\|\\s*`([^`]+)`")
    MSW_PATH = re.compile(r'http\\.(?:get|post|put|patch|delete|all)\\(\\s*"([^"]+)"')


    def _read_api_entries() -> list[tuple[str, str, str, str]]:
      entries: list[tuple[str, str, str, str]] = []
      for reg in (SRC / "api/functions").glob("*/registry.ts"):
        text = reg.read_text(encoding="utf-8")
        for m in API_ENTRY.finditer(text):
          entries.append((m.group(1), m.group(2), m.group(3), m.group(4)))
      return entries

    def _read_route_entries() -> dict[str, str]:
      mapping: dict[str, str] = {}
      for reg in (SRC / "router/modules").glob("*/registry.ts"):
        text = reg.read_text(encoding="utf-8")
        for m in ROUTE_ENTRY.finditer(text):
          mapping[m.group(2)] = m.group(1)
      return mapping

    def _read_msw_paths() -> set[str]:
      paths: set[str] = set()
      for f in (SRC / "mocks/handlers").glob("*.ts"):
        if f.name == "index.ts":
          continue
        text = f.read_text(encoding="utf-8")
        paths.update(MSW_PATH.findall(text))
      return paths

    def main() -> int:
      errors: list[str] = []
      routes = _read_route_entries()
      msw = _read_msw_paths()

      for api_id, module_id, route_name, path in _read_api_entries():
        if routes.get(module_id) != route_name:
          errors.append(
            f"api registry {api_id}: routeName {route_name!r} != router {routes.get(module_id)!r} for {module_id}"
          )
        contract = SRC / "pages" / module_id / "contracts/README.md"
        if contract.is_file():
          text = contract.read_text(encoding="utf-8")
          cm = CONTRACT_API.search(text)
          cr = CONTRACT_ROUTE.search(text)
          if cm and cm.group(1) != api_id:
            errors.append(f"{module_id} contracts api id {cm.group(1)!r} != registry {api_id!r}")
          if cr and cr.group(1) != route_name:
            errors.append(f"{module_id} contracts route {cr.group(1)!r} != registry {route_name!r}")
        if path not in msw and not any(p.startswith(path.rsplit("/", 1)[0]) for p in msw):
          errors.append(f"MSW missing handler path for api {api_id}: {path}")

      if errors:
        print("resource_chain FAIL:", file=sys.stderr)
        for e in errors:
          print(f"  - {e}", file=sys.stderr)
        return 1
      print("OK: resource chain aligned (api registry · router · contracts · MSW)")
      return 0


    if __name__ == "__main__":
      sys.exit(main())
    """,
  )

  # vite.config.ts patch
  patch(
    "vite.config.ts",
    """        manualChunks(id) {
          if (id.includes("node_modules/@mui") || id.includes("node_modules/@emotion")) {
            return "vendor-mui";
          }""",
    """        manualChunks(id) {
          if (
            id.includes("node_modules/react/")
            || id.includes("node_modules/react-dom/")
            || id.includes("node_modules/react-router")
            || id.includes("node_modules/@tanstack/react-query")
            || id.includes("node_modules/scheduler/")
          ) {
            return "vendor-react";
          }
          if (id.includes("node_modules/@mui") || id.includes("node_modules/@emotion")) {
            return "vendor-mui";
          }""",
  )

  # check_bundle_size.py
  w(
    "scripts/check_bundle_size.py",
    """
    #!/usr/bin/env python3
    # web-admin 构建产物体积门禁（W-07 + S4 vendor-react/index）
    from __future__ import annotations

    import json
    import sys
    from pathlib import Path

    APP_ROOT = Path(__file__).resolve().parents[1]
    DIST = APP_ROOT / "dist" / "assets"

    LIMITS: dict[str, int] = {
      "vendor-react": 260_000,
      "vendor-mui": 650_000,
      "vendor-echarts": 1_000_000,
      "vendor-animate": 120_000,
      "index": 120_000,
    }
    DEFAULT_MAX = 1_500_000


    def _chunk_limit(name: str) -> int:
      for prefix, limit in LIMITS.items():
        if name.startswith(prefix) or f"-{prefix}" in name or prefix in name:
          return limit
      return DEFAULT_MAX


    def main() -> int:
      if not DIST.is_dir():
        print("FAIL: dist/assets missing — run pnpm build first", file=sys.stderr)
        return 1

      js_files = sorted(DIST.glob("*.js"))
      if not js_files:
        print("FAIL: no JS assets in dist/assets", file=sys.stderr)
        return 1

      report: list[dict[str, int | str]] = []
      errors: list[str] = []

      for path in js_files:
        size = path.stat().st_size
        limit = _chunk_limit(path.name)
        report.append({"file": path.name, "bytes": size, "limit": limit})
        if size > limit:
          errors.append(f"{path.name}: {size} > {limit} bytes")

      print(json.dumps({"chunks": report}, ensure_ascii=False, indent=2))

      if errors:
        print("bundle size FAIL:", file=sys.stderr)
        for err in errors:
          print(f"  - {err}", file=sys.stderr)
        return 1

      print("OK: bundle size within limits")
      return 0


    if __name__ == "__main__":
      sys.exit(main())
    """,
  )

  # global.css view transition
  patch(
    "src/styles/global.css",
    """@media (prefers-reduced-motion: reduce) {
  .animate__animated {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}""",
    """.fos-studio-outlet {
  min-height: 40vh;
}

@supports (view-transition-name: root) {
  .fos-studio-outlet {
    view-transition-name: fos-studio-main;
  }
}

@media (prefers-reduced-motion: reduce) {
  .animate__animated {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
  .fos-studio-outlet {
    view-transition-name: none;
  }
}""",
  )

  # playwright - e2e 禁用 MSW（用 page.route mock）
  patch(
    "playwright.config.ts",
    'command: "pnpm dev --host 127.0.0.1 --port 5173",',
    'command: "pnpm dev --host 127.0.0.1 --port 5173",',
  )
  pw = APP / "playwright.config.ts"
  pwt = pw.read_text(encoding="utf-8")
  if "VITE_MSW" not in pwt:
    pwt = pwt.replace(
      "    timeout: 120_000,\n  },",
      """    timeout: 120_000,
    env: {
      ...process.env,
      VITE_MSW: "0",
    },
  },""",
    )
    pw.write_text(pwt, encoding="utf-8")
    print("patched playwright.config.ts env")

  # patch check_harness for resource chain
  harness = APP / "scripts/check_harness.py"
  ht = harness.read_text(encoding="utf-8")
  if "_validate_resource_chain" not in ht:
    insert = '''

def _validate_resource_chain(errors: list[str]) -> None:
  """api.id · route.name · module-id · MSW 三角对账（S4）。"""
  import subprocess
  import sys

  script = APP_ROOT / "scripts" / "check_resource_chain.py"
  if not script.is_file():
    errors.append("missing scripts/check_resource_chain.py")
    return
  result = subprocess.run(
    _script_python_argv(script),
    cwd=APP_ROOT,
    capture_output=True,
    text=True,
  )
  if result.returncode != 0:
    msg = (result.stderr or result.stdout or "resource chain failed").strip().splitlines()[-1]
    errors.append(msg)
'''
    ht = ht.replace(
      "def _validate_directory_readmes(errors: list[str]) -> None:",
      insert + "\ndef _validate_directory_readmes(errors: list[str]) -> None:",
    )
    ht = ht.replace(
      "  _validate_directory_readmes(errors)\n",
      "  _validate_directory_readmes(errors)\n  _validate_resource_chain(errors)\n",
    )
    harness.write_text(ht, encoding="utf-8")
    print("patched check_harness.py")

  # devkit.profile
  prof = APP / "devkit.profile.yaml"
  pt = prof.read_text(encoding="utf-8")
  if "resource_chain_sync" not in pt:
    pt = pt.replace(
      "  - directory_readme\n",
      "  - directory_readme\n  - resource_chain_sync\n  - perf_first_paint_shell\n",
    )
    prof.write_text(pt, encoding="utf-8")
    print("patched devkit.profile.yaml")

  # browser-router test update
  brt = APP / "src/router/browser-router.test.tsx"
  if brt.is_file():
    brt.write_text(
      """
    /**
     * 模块：src/apps/web-admin/src/router/browser-router.test.tsx
     * 作用：createAppRouter 冒烟
     * 怎么用：vitest run
     * 解决：data router 工厂可实例化
     * 上游：createQueryClient
     * 下游：bootstrap
     * 关联：W-06
     */
    import { describe, expect, it } from "vitest";
    import { createQueryClient } from "@/api/query/client";
    import { createAppRouter } from "@/router/browser-router";

    describe("createAppRouter", () => {
      it("creates a data router with studio routes", () => {
        const router = createAppRouter(createQueryClient());
        expect(router.routes.length).toBeGreaterThan(0);
      });
    });
    """.strip()
      + "\n",
      encoding="utf-8",
    )
    print("wrote router/browser-router.test.tsx")

  # ENGINEERING S4 section append
  eng = APP / "ENGINEERING.md"
  et = eng.read_text(encoding="utf-8")
  s4 = """
## 10. 性能基准 S4（锁死 · 无 SSR）

| 能力 | 落点 | 门禁 |
|------|------|------|
| 首屏占位壳 | `index.html#fos-boot-shell` | 人工 + Lighthouse |
| 默认 MSW | `.env.development` `VITE_MSW=1` | `pnpm dev` |
| 骨架屏 | `@/components/skeletons` | RTL |
| 路由错误降级 | `RouteErrorFallback` + `errorElement` | 路由测试 |
| 数据预取 | `router/loaders` + `StudioNavLink` prefetch | harness |
| 切屏动画 | `StudioAnimatedOutlet` + `styles/motion` | e2e |
| 响应式壳 | `StudioShellLayout` md↓ temporary drawer | RTL |
| vendor-react | `vite.config.ts` manualChunks | `check_bundle_size.py` |
| 资源三角 | `check_resource_chain.py` | harness |

目标（PC）：LCP P75 < 1.5s · 步间导航感知 < 200ms · CLS < 0.05。
"""
  if "## 10. 性能基准 S4" not in et:
    eng.write_text(et.rstrip() + "\n" + s4, encoding="utf-8")
    print("patched ENGINEERING.md")

  template_readme = ROOT / "templates/frontend-devkit/src/README.md"
  if template_readme.is_file():
    (APP / "src/README.md").write_text(template_readme.read_text(encoding="utf-8"), encoding="utf-8")
    print("restored src/README.md")

  w(
    "src/components/charts/charts.test.ts",
    """
    /**
     * 模块：src/apps/web-admin/src/components/charts/charts.test.ts
     * 作用：Vitest：charts 懒加载导出冒烟
     * 怎么用：pnpm test charts.test
     * 解决：LineChart/BarChart 为 React.lazy
     * 上游：components/charts/index.ts
     * 下游：CI pnpm check
     * 关联：ENGINEERING.md §10 S4
     */
    import { describe, expect, it } from "vitest";
    import { BarChart, BaseChart, LineChart } from "@/components/charts";

    describe("charts exports", () => {
      it("exports BaseChart eagerly and chart views lazily", () => {
        expect(typeof BaseChart).toBe("function");
        expect(LineChart).toBeTruthy();
        expect(BarChart).toBeTruthy();
        expect(typeof LineChart).toBe("object");
        expect(typeof BarChart).toBe("object");
      });
    });
    """,
  )

  return 0


if __name__ == "__main__":
  raise SystemExit(main())
