/**
 * 模块：src/apps/web-admin/src/layout/RootLayout.tsx
 * 作用：全站根 layout（Outlet 容器）
 * 怎么用：router/compose 最外层 Route element
 * 解决：domain layout 之上的公共壳
 * 上游：router/compose.tsx
 * 下游：layout/modules 各 domain shell
 * 关联：layout/contracts/README.md
 */
import Box from "@mui/material/Box";
import { Outlet } from "react-router-dom";

export function RootLayout() {
  return (
    <Box minHeight="100vh" bgcolor="background.default">
      <Outlet />
    </Box>
  );
}