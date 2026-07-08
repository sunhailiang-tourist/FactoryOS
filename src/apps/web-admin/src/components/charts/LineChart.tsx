/**
 * 模块：src/apps/web-admin/src/components/charts/LineChart.tsx
 * 作用：折线图封装（Shadow 趋势 · 执行量）
 * 怎么用：lazy import { LineChart } from '@/components/charts/LineChart'
 * 解决：业务页不直接接触 echarts API
 * 上游：BaseChart · api 数据
 * 下游：pages/studio-prove 等
 * 关联：components/charts/contracts/README.md
 */
import type { EChartsOption } from "echarts";
import { BaseChart } from "./BaseChart";

export type LineChartProps = {
  categories: string[];
  series: Array<{ name: string; data: number[] }>;
  title?: string;
  height?: number;
  className?: string;
};

/**
 * 功能：LineChart 导出函数。
 * 业务含义：web-admin 模块对外入口。
 * 上游：同文件文件头。
 * 下游：见调用链。
 */
export function LineChart({ categories, series, title, height, className }: LineChartProps) {
  // 业务：LineChart 主体编排（见文件头上下游）
  const option: EChartsOption = {
    title: title ? { text: title, left: "center" } : undefined,
    tooltip: { trigger: "axis" },
    legend: series.length > 1 ? { bottom: 0 } : undefined,
    grid: { left: 48, right: 24, top: title ? 48 : 24, bottom: series.length > 1 ? 40 : 24 },
    xAxis: { type: "category", data: categories, boundaryGap: false },
    yAxis: { type: "value" },
    series: series.map((item) => ({
      name: item.name,
      type: "line",
      smooth: true,
      data: item.data,
    })),
  };

  return <BaseChart option={option} height={height} className={className} />;
}
