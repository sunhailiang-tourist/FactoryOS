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
