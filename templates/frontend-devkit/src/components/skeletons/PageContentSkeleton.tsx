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

/**
 * 功能：PageContentSkeleton 导出函数。
 * 业务含义：web-admin 模块对外入口。
 * 上游：同文件文件头。
 * 下游：见调用链。
 */
export function PageContentSkeleton() {
  // 业务：PageContentSkeleton 主体编排（见文件头上下游）
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
