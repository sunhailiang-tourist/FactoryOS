# charts · 板块契约

## 是什么

ECharts 按需封装层：`@/components/charts/*`；pages 禁止直接 import `echarts`。

## 登记索引

| 导出 | 文件 | 用途 |
|------|------|------|
| `BaseChart` | `BaseChart.tsx` | 通用容器 |
| `LineChart` | `LineChart.tsx` | 折线图 |
| `BarChart` | `BarChart.tsx` | 柱状图 |
| `getEchartsTheme` | `theme.ts` | token 主题 |
| `ensureEchartsRegistered` | `register.ts` | 按需注册 |

## 变更规则

1. 新增 chart 类型 → 在 `register.ts` 注册 + 新建封装组件 + 更新本表。
2. 业务页仅 lazy import 封装组件，禁止 `import * as echarts`。
3. 颜色/font 须走 `getEchartsTheme()`，禁止硬编码 hex。
