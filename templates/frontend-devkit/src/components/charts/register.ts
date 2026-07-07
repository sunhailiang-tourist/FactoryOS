/**
 * 模块：src/apps/web-admin/src/components/charts/register.ts
 * 作用：ECharts 按需注册 chart 类型与组件
 * 怎么用：BaseChart mount 前 import；勿在 pages 直接 import echarts
 * 解决：tree-shake · vendor-echarts 独立分包
 * 上游：echarts npm 包
 * 下游：BaseChart.tsx · LineChart · BarChart
 * 关联：components/charts/contracts/README.md
 */
import { BarChart, LineChart } from "echarts/charts";
import {
  GridComponent,
  LegendComponent,
  TitleComponent,
  TooltipComponent,
} from "echarts/components";
import * as echarts from "echarts/core";
import { CanvasRenderer } from "echarts/renderers";

let registered = false;

export function ensureEchartsRegistered(): void {
  if (registered) {
    return;
  }
  echarts.use([
    LineChart,
    BarChart,
    GridComponent,
    TooltipComponent,
    LegendComponent,
    TitleComponent,
    CanvasRenderer,
  ]);
  registered = true;
}

export { echarts };
