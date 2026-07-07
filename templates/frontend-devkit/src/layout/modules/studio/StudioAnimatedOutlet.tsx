/**
 * 模块：src/apps/web-admin/src/layout/modules/studio/StudioAnimatedOutlet.tsx
 * 作用：Outlet 内容区过渡 + 嵌套 Suspense
 * 怎么用：StudioShellLayout main 区
 * 解决：步间硬切 → motion + skeleton
 * 上游：MotionContainer · styles/motion
 * 下游：pages lazy
 * 关联：ENGINEERING.md §10 S4
 */
import { Suspense } from "react";
import { Outlet, useLocation } from "react-router-dom";
import { PageContentSkeleton } from "@/components/skeletons";
import { MotionContainer } from "@/styles/motion";

export function StudioAnimatedOutlet() {
  const location = useLocation();
  return (
    <MotionContainer
      key={location.pathname}
      preset="enter"
      className="fos-studio-outlet"
    >
      <Suspense fallback={<PageContentSkeleton />}>
        <Outlet />
      </Suspense>
    </MotionContainer>
  );
}
