/**
 * 模块：src/apps/web-admin/src/api/query/hooks/useStudioFlows.ts
 * 作用：Studio 六步 flows Server State hook
 * 怎么用：layout/pages import { useStudioFlows } from '@/api/query/hooks/useStudioFlows'
 * 解决：pages 禁直引 api/functions；统一 loading/error/data
 * 上游：getStudioFlows · studioKeys.flows
 * 下游：StudioShellLayout · StudioHomePage
 * 关联：pages/studio-shell/contracts/README.md · W-02
 */
import { useQuery } from "@tanstack/react-query";
import { getStudioFlows } from "@/api/functions/studio-shell";
import { studioKeys } from "@/api/query/keys";

/** GET /v1/studio/flows — 六步向导元数据。 */
export function useStudioFlows() {
  return useQuery({
    queryKey: studioKeys.flows(),
    queryFn: getStudioFlows,
  });
}
