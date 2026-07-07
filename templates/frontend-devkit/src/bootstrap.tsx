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
import { I18nProvider } from "@/i18n/core/provider";
import { createAppRouter } from "@/router/browser-router";

export function Bootstrap() {
  const [queryClient] = useState(() => createQueryClient());
  const [router] = useState(() => createAppRouter(queryClient));

  return (
    <QueryClientProvider client={queryClient}>
      <I18nProvider>
        <AppThemeProvider>
          <Suspense fallback={<PageLoading />}>
            <RouterProvider router={router} />
          </Suspense>
        </AppThemeProvider>
      </I18nProvider>
    </QueryClientProvider>
  );
}
