/**
 * 模块：src/apps/web-admin/src/components/charts/theme.ts
 * 作用：ECharts 主题读 CSS Variables（与 MUI token 同源）
 * 怎么用：BaseChart option 合并 getEchartsTheme()
 * 解决：图表颜色与全站 Design Token 一致
 * 上游：styles/tokens.css · syncThemeVars
 * 下游：BaseChart.tsx
 * 关联：styles/contracts/README.md
 */
import { readCssVar } from "@/components/syncThemeVars";

export function getEchartsTheme() {
  return {
    color: [
      readCssVar("--fos-color-primary", "#1565c0"),
      readCssVar("--fos-color-success", "#2e7d32"),
      readCssVar("--fos-color-warning", "#ed6c02"),
      readCssVar("--fos-color-error", "#d32f2f"),
    ],
    backgroundColor: "transparent",
    textStyle: {
      fontFamily: readCssVar("--fos-font-family", "sans-serif"),
      color: readCssVar("--fos-color-text-primary", "#333"),
    },
    title: {
      textStyle: {
        color: readCssVar("--fos-color-text-primary", "#333"),
      },
    },
  };
}
