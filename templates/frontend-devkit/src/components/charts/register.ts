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

/**
 * 功能：ensureEchartsRegistered 导出函数。
 * 业务含义：web-admin 模块对外入口。
 * 上游：同文件文件头。
 * 下游：见调用链。
 */
export function ensureEchartsRegistered(): void {
  // 业务：ensureEchartsRegistered 主体编排（见文件头上下游）
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
