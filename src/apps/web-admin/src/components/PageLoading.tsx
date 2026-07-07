/**
 * 模块：src/apps/web-admin/src/components/PageLoading.tsx
 * 作用：路由 lazy Suspense fallback
 * 怎么用：AppShell Suspense fallback 引用
 * 解决：统一加载占位
 * 上游：AppShell.tsx
 * 下游：用户感知加载态
 * 关联：components/README.md
 */
import Box from "@mui/material/Box";
import CircularProgress from "@mui/material/CircularProgress";
import Typography from "@mui/material/Typography";

type PageLoadingProps = {
  label?: string;
};

export function PageLoading({ label = "加载中" }: PageLoadingProps) {
  return (
    <Box display="flex" flexDirection="column" justifyContent="center" alignItems="center" minHeight="40vh" gap={1}>
      <CircularProgress aria-label={label} />
      <Typography variant="body2" color="text.secondary">
        {label}
      </Typography>
    </Box>
  );
}