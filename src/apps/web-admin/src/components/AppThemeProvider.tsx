/**
 * 模块：src/apps/web-admin/src/components/AppThemeProvider.tsx
 * 作用：MUI ThemeProvider 包装
 * 怎么用：bootstrap 根节点包裹
 * 解决：全站主题/token 一致
 * 上游：bootstrap.tsx · components/theme.ts
 * 下游：AppShell 以下整树
 * 关联：components/README.md
 */
import CssBaseline from "@mui/material/CssBaseline";
import { ThemeProvider } from "@mui/material/styles";
import { useEffect, type ReactNode } from "react";
import { syncThemeVars } from "./syncThemeVars";
import { appTheme } from "./theme";

type AppThemeProviderProps = {
  children: ReactNode;
};

export function AppThemeProvider({ children }: AppThemeProviderProps) {
  useEffect(() => {
    syncThemeVars(appTheme);
  }, []);

  return (
    <ThemeProvider theme={appTheme}>
      <CssBaseline />
      {children}
    </ThemeProvider>
  );
}