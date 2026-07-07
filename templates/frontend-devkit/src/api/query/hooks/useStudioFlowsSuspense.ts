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
