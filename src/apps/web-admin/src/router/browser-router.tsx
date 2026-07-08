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
import { getActorContext } from "@/api/request";
import { getRoutesByLayout } from "@/router/registry";

/**
 * 功能：createAppRouter 导出函数。
 * 业务含义：web-admin 模块对外入口。
 * 上游：同文件文件头。
 * 下游：见调用链。
 */
export function createAppRouter(queryClient: QueryClient) {
  // 业务：createAppRouter 主体编排（见文件头上下游）
  const actorRole = getActorContext().role;
  const studioFlowsLoader = createStudioFlowsLoader(queryClient);
  return createBrowserRouter(
    createRoutesFromElements(
      <Route element={<RootLayout />} errorElement={<RouteErrorFallback />}>
        <Route path="/" element={<Navigate to="/studio" replace />} />
        {LAYOUT_REGISTRY.map((layout) => {
          const LayoutComponent = layout.component;
          const routes = getRoutesByLayout(layout.id, actorRole);
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
