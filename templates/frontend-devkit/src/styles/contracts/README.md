# styles · 板块契约

## 是什么

全局样式与 Design Token 真源：`styles/global.css` · `styles/tokens.css`；运行时由 `components/syncThemeVars.ts` 从 MUI theme 同步。

## 登记索引

| 路径 | 职责 | 消费方 |
|------|------|--------|
| `styles/global.css` | Tailwind + animate 子集 | `main.tsx` import |
| `styles/tokens.css` | CSS Variables 默认值 | global.css · ECharts theme |
| `pages/{id}/styles/*.module.css` | 模块私有样式 | 同 module-id 页面/组件 |
| `components/theme.ts` | MUI theme 定义 | AppThemeProvider |
| `components/syncThemeVars.ts` | theme → :root 同步 | AppThemeProvider mount |
| `components/charts/theme.ts` | ECharts 读 token | `@/components/charts/*` |
| `styles/motion/presets.ts` | animate 白名单 | MotionContainer |

## 变更规则

1. 新增 token → 同步 `tokens.css` · `global.css @theme` · `syncThemeVars.ts` · `charts/theme.ts`。
2. 新增 animate 预设 → 仅通过 `styles/motion/presets.ts` 白名单；必要时在 `global.css` 增加 `@import`。
3. 模块样式仅放 `pages/{module-id}/styles/`，禁止跨 module import `.module.css`。
