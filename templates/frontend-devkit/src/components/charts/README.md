# components/charts · ECharts 封装

**禁止** 在 `pages/**` 直接 `import echarts`；须经本目录组件。

## 组件

| 组件 | 用途 |
|------|------|
| `BaseChart` | 通用容器 · resize · token 主题 |
| `LineChart` | 折线（Shadow 趋势） |
| `BarChart` | 柱状（drift 对比） |

## 分包

Vite `manualChunks` → `vendor-echarts`；页面 lazy import chart 组件。

## Token

颜色/font 读 `:root` CSS Variables（`getEchartsTheme()`）。
