/**
 * 模块：src/apps/web-admin/src/components/theme.ts
 * 作用：MUI appTheme 定义
 * 怎么用：AppThemeProvider import appTheme
 * 解决：Design token 单点
 * 上游：MUI theming
 * 下游：AppThemeProvider
 * 关联：components/README.md
 */
import { createTheme } from "@mui/material/styles";

export const appTheme = createTheme({
  palette: {
    mode: "light",
    primary: { main: "#1565c0", light: "#1e88e5" },
    success: { main: "#2e7d32" },
    warning: { main: "#ed6c02" },
    error: { main: "#d32f2f" },
    background: { default: "#f5f6f8", paper: "#ffffff" },
    text: {
      primary: "rgba(0, 0, 0, 0.87)",
      secondary: "rgba(0, 0, 0, 0.6)",
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", "PingFang SC", "Microsoft YaHei", sans-serif',
  },
});