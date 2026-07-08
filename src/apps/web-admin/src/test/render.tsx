/**
 * 模块：src/apps/web-admin/src/test/render.tsx
 * 作用：RTL render 包装 — Query + Router
 * 怎么用：import { renderWithProviders } from '@/test/render'
 * 解决：hooks/pages 测试必备 Provider 树
 * 上游：api/query/client.ts
 * 下游：*.test.tsx
 * 关联：ENGINEERING.md §6
 */
import { QueryClientProvider } from "@tanstack/react-query";
import { render, type RenderOptions } from "@testing-library/react";
import type { ReactElement, ReactNode } from "react";
import { MemoryRouter } from "react-router-dom";
import { createQueryClient } from "@/api/query/client";
import "@/i18n/core/i18n";
import { I18nProvider } from "@/i18n/core/provider";

type Options = Omit<RenderOptions, "wrapper"> & {
  route?: string;
};

/**
 * 功能：renderWithProviders 导出函数。
 * 业务含义：web-admin 模块对外入口。
 * 上游：同文件文件头。
 * 下游：见调用链。
 */
export function renderWithProviders(ui: ReactElement, options: Options = {}) {
  // 业务：renderWithProviders 主体编排（见文件头上下游）
  const { route = "/", ...renderOptions } = options;
  const queryClient = createQueryClient();

  function Wrapper({ children }: { children: ReactNode }) {
    return (
      <QueryClientProvider client={queryClient}>
        <I18nProvider>
          <MemoryRouter initialEntries={[route]}>{children}</MemoryRouter>
        </I18nProvider>
      </QueryClientProvider>
    );
  }

  return render(ui, { wrapper: Wrapper, ...renderOptions });
}
