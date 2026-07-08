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

/**
 * 功能：StudioAnimatedOutlet 导出函数。
 * 业务含义：web-admin 模块对外入口。
 * 上游：同文件文件头。
 * 下游：见调用链。
 */
export function StudioAnimatedOutlet() {
  // 业务：StudioAnimatedOutlet 主体编排（见文件头上下游）
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
