/**
 * 模块：src/apps/web-admin/.storybook/decorators.tsx
 * 作用：Storybook 共享 decorator — Query 预置数据
 * 怎么用：pages stories import withStudioFlows
 * 解决：依赖 useStudioFlows 的页面 stories 无需 MSW
 * 上游：api/query/keys.ts
 * 下游：StudioHomePage.stories.tsx
 * 关联：W-08
 */
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import type { Decorator } from "@storybook/react";
import type { ReactNode } from "react";
import { studioKeys } from "../src/api/query/keys";

const FLOWS_FIXTURE = {
  version: "1.0.0",
  title: "Integration Studio 六步向导",
  steps: [
    { id: "connect", order: 1, title: "连通", summary: "凭证 ref、ping" },
    { id: "discover", order: 2, title: "发现", summary: "Blueprint 校验" },
    { id: "map", order: 3, title: "映射", summary: "字段映射" },
    { id: "prove", order: 4, title: "验证", summary: "Shadow 证明" },
    { id: "freeze", order: 5, title: "冻结", summary: "Graph freeze" },
    { id: "export", order: 6, title: "导出", summary: "Package export" },
  ],
};

export function withStudioFlows(): Decorator {
  return (Story) => {
    const client = new QueryClient({
      defaultOptions: { queries: { retry: false } },
    });
    client.setQueryData(studioKeys.flows(), FLOWS_FIXTURE);
    return (
      <QueryClientProvider client={client}>
        <Story />
      </QueryClientProvider>
    );
  };
}

export function withPadding(children: ReactNode) {
  return <div style={{ padding: 24 }}>{children}</div>;
}
