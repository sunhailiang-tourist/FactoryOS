/**
 * 模块：src/apps/web-admin/src/components/syncThemeVars.ts
 * 作用：MUI theme → :root CSS Variables 同步
 * 怎么用：AppThemeProvider mount 时调用 syncThemeVars(appTheme)
 * 解决：MUI · Tailwind · ECharts 共用 Design Token 真源
 * 上游：components/theme.ts · MUI ThemeProvider
 * 下游：styles/tokens.css · Tailwind @theme · components/charts/theme.ts
 * 关联：styles/contracts/README.md
 */
import type { Theme } from "@mui/material/styles";

const VAR_MAP: Array<[string, (t: Theme) => string]> = [
  ["--fos-color-primary", (t) => t.palette.primary.main],
  ["--fos-color-primary-light", (t) => t.palette.primary.light ?? t.palette.primary.main],
  ["--fos-color-bg-default", (t) => t.palette.background.default],
  ["--fos-color-bg-paper", (t) => t.palette.background.paper],
  ["--fos-color-text-primary", (t) => t.palette.text.primary],
  ["--fos-color-text-secondary", (t) => t.palette.text.secondary],
  ["--fos-color-success", (t) => t.palette.success.main],
  ["--fos-color-warning", (t) => t.palette.warning.main],
  ["--fos-color-error", (t) => t.palette.error.main],
  [
    "--fos-font-family",
    (t) => (typeof t.typography.fontFamily === "string" ? t.typography.fontFamily : "sans-serif"),
  ],
  ["--fos-spacing-unit", (t) => `${typeof t.spacing === "function" ? t.spacing(1) : 8}px`],
];

export function syncThemeVars(theme: Theme): void {
  if (typeof document === "undefined") {
    return;
  }
  const root = document.documentElement;
  for (const [name, resolve] of VAR_MAP) {
    root.style.setProperty(name, resolve(theme));
  }
}

export function readCssVar(name: string, fallback = ""): string {
  if (typeof document === "undefined") {
    return fallback;
  }
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim() || fallback;
}
