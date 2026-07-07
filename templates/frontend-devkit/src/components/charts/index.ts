/**
 * 模块：src/apps/web-admin/src/components/charts/index.ts
 * 作用：charts 懒加载导出（S4 · 重组件分包）
 * 怎么用：import { LineChart } from '@/components/charts'（React.lazy）
 * 解决：未用图表时不拉 vendor-echarts
 * 上游：LineChart · BarChart lazy
 * 下游：业务 pages
 * 关联：components/charts/contracts/README.md
 */
import { lazy } from "react";

export const LineChart = lazy(() =>
  import("./LineChart").then((m) => ({ default: m.LineChart })),
);
export const BarChart = lazy(() =>
  import("./BarChart").then((m) => ({ default: m.BarChart })),
);
export type { BarChartProps } from "./BarChart";
export type { BaseChartProps } from "./BaseChart";
export type { LineChartProps } from "./LineChart";
export { BaseChart } from "./BaseChart";
export { ensureEchartsRegistered } from "./register";
