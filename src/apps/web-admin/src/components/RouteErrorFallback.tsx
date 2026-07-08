/**
 * 模块：src/apps/web-admin/src/components/RouteErrorFallback.tsx
 * 作用：路由 errorElement — lazy/load 失败降级
 * 怎么用：browser-router Route errorElement
 * 解决：chunk 失败白屏 → 可重试 UI
 * 上游：react-router useRouteError
 * 下游：用户重试导航
 * 关联：ENGINEERING.md §10 S4
 */
import Alert from "@mui/material/Alert";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";
import { isRouteErrorResponse, useRouteError } from "react-router-dom";

/**
 * 功能：RouteErrorFallback 导出函数。
 * 业务含义：web-admin 模块对外入口。
 * 上游：同文件文件头。
 * 下游：见调用链。
 */
export function RouteErrorFallback() {
  // 业务：RouteErrorFallback 主体编排（见文件头上下游）
  const error = useRouteError();
  const message = isRouteErrorResponse(error)
    ? `${error.status} ${error.statusText}`
    : error instanceof Error
      ? error.message
      : "页面加载失败";

  return (
    <Box p={3} maxWidth={560}>
      <Alert severity="error" sx={{ mb: 2 }}>
        {message}
      </Alert>
      <Typography variant="body2" color="text.secondary" paragraph>
        可能是网络中断或代码分包加载失败。请重试或返回 Studio 概览。
      </Typography>
      <Button variant="contained" onClick={() => window.location.assign("/studio")}>
        返回概览
      </Button>
      <Button sx={{ ml: 1 }} onClick={() => window.location.reload()}>
        重新加载
      </Button>
    </Box>
  );
}
