/**
 * 模块：src/apps/web-admin/src/pages/studio-shell/StudioHomePage.lazy.tsx
 * 作用：Studio 概览 lazy 页面入口
 * 怎么用：router/modules/studio-shell/registry.ts lazy import
 * 解决：flows 已由 layout loader 预取，直接渲染卡片
 * 上游：useStudioFlowsSuspense
 * 下游：store/modules/studio-shell
 * 关联：pages/studio-shell/contracts/README.md
 */
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import { Suspense } from "react";
import { useStudioFlowsSuspense } from "@/api/query/hooks/useStudioFlowsSuspense";
import { PageContentSkeleton } from "@/components/skeletons";
import { MotionContainer } from "@/styles/motion";
import styles from "./styles/home.module.css";

function StudioHomeContent() {
  const { data } = useStudioFlowsSuspense();
  const title = data.title ?? "Integration Studio";
  const stepCount = data.steps?.length ?? 0;

  return (
    <MotionContainer preset="enterUp" className={`${styles.pageShell} mx-auto p-6`}>
      <Card variant="outlined" className="shadow-fos-sm">
        <CardContent>
          <Typography variant="h4" gutterBottom className={styles.heroTitle}>
            {title}
          </Typography>
          <Typography variant="body1" color="text.secondary" paragraph>
            从左侧选择六步向导步骤，完成新客户零仓库接入。
          </Typography>
          <span className={styles.stepBadge}>已注册 {stepCount} 个向导步骤</span>
        </CardContent>
      </Card>
    </MotionContainer>
  );
}

export default function StudioHomePage() {
  return (
    <Suspense fallback={<PageContentSkeleton />}>
      <StudioHomeContent />
    </Suspense>
  );
}
