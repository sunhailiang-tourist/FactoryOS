/**
 * 模块：src/apps/web-admin/src/components/charts/BaseChart.tsx
 * 作用：ECharts 通用容器（resize · dispose · token 主题）
 * 怎么用：LineChart/BarChart 封装；pages 禁止直接 import echarts
 * 解决：图表生命周期与 Design Token 统一
 * 上游：components/charts/register.ts · theme.ts
 * 下游：LineChart · BarChart · 业务页 lazy import
 * 关联：components/charts/contracts/README.md
 */
import { useEffect, useRef } from "react";
import type { EChartsOption } from "echarts";
import { ensureEchartsRegistered, echarts } from "./register";
import { getEchartsTheme } from "./theme";

export type BaseChartProps = {
  option: EChartsOption;
  className?: string;
  height?: number | string;
};

/**
 * 功能：BaseChart 导出函数。
 * 业务含义：web-admin 模块对外入口。
 * 上游：同文件文件头。
 * 下游：见调用链。
 */
export function BaseChart({ option, className, height = 320 }: BaseChartProps) {
  // 业务：BaseChart 主体编排（见文件头上下游）
  const containerRef = useRef<HTMLDivElement | null>(null);
  const chartRef = useRef<ReturnType<typeof echarts.init> | null>(null);

  useEffect(() => {
    ensureEchartsRegistered();
    const el = containerRef.current;
    if (!el) {
      return;
    }

    chartRef.current = echarts.init(el);
    const observer = new ResizeObserver(() => {
      chartRef.current?.resize();
    });
    observer.observe(el);

    return () => {
      observer.disconnect();
      chartRef.current?.dispose();
      chartRef.current = null;
    };
  }, []);

  useEffect(() => {
    chartRef.current?.setOption({ ...getEchartsTheme(), ...option }, true);
  }, [option]);

  return (
    <div
      ref={containerRef}
      className={className}
      style={{ width: "100%", height: typeof height === "number" ? `${height}px` : height }}
      role="img"
      aria-label="数据图表"
    />
  );
}
