/**
 * 模块：src/apps/web-admin/src/components/charts/charts.test.ts
 * 作用：Vitest：charts 懒加载导出冒烟
 * 怎么用：pnpm test charts.test
 * 解决：LineChart/BarChart 为 React.lazy
 * 上游：components/charts/index.ts
 * 下游：CI pnpm check
 * 关联：ENGINEERING.md §10 S4
 */
import { describe, expect, it } from "vitest";
import { BarChart, BaseChart, LineChart } from "@/components/charts";

describe("charts exports", () => {
  it("exports BaseChart eagerly and chart views lazily", () => {
    expect(typeof BaseChart).toBe("function");
    expect(LineChart).toBeTruthy();
    expect(BarChart).toBeTruthy();
    expect(typeof LineChart).toBe("object");
    expect(typeof BarChart).toBe("object");
  });
});
