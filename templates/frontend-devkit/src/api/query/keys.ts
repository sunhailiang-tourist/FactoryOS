/**
 * 模块：src/apps/web-admin/src/api/query/keys.ts
 * 作用：queryKey 工厂 — module-id 与 API 对齐
 * 怎么用：hooks 内 queryKey: studioKeys.flows()
 * 解决：invalidate/prefetch 键一致，避免字符串散落
 * 上游：api/query/hooks/*
 * 下游：TanStack Query cache
 * 关联：api/query/contracts/README.md
 */

export const studioKeys = {
  all: ["studio"] as const,
  flows: () => [...studioKeys.all, "flows"] as const,
};

/** 按 module-id 命名空间（create:module 默认）。 */
export const queryKeys = {
  module: (moduleId: string) => ["module", moduleId] as const,
};
