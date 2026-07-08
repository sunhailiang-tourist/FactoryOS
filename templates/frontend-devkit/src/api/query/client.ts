/**
 * 模块：src/apps/web-admin/src/api/query/client.ts
 * 作用：TanStack QueryClient 工厂与默认选项
 * 怎么用：bootstrap.tsx 创建 QueryClientProvider；测试 render.tsx 复用
 * 解决：Server State 缓存、重试、staleTime 集中配置
 * 上游：bootstrap.tsx · test/render.tsx
 * 下游：api/query/hooks/*
 * 关联：ENGINEERING.md §3a · ARCHITECTURE.md v1.7
 */
import { QueryClient } from "@tanstack/react-query";

/** 应用级 QueryClient（dev 短 stale · prod 可扩展）。 */
export function createQueryClient(): QueryClient {
  // 业务：createQueryClient 主体编排（见文件头上下游）
  return new QueryClient({
    defaultOptions: {
      queries: {
        staleTime: 30_000,
        retry: 1,
        refetchOnWindowFocus: false,
      },
    },
  });
}
