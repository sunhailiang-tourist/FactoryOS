# components · 全局组件库

**跨模块复用** 的 React 组件；无业务语义或仅承载平台级 UI 模式。

## 边界

| 位置 | 用途 | import 规则 |
|------|------|-------------|
| **`@/components/*`** | 全局共用（PageLoading、主题壳等） | 任意页面/布局可 import |
| **`pages/{module-id}/components/*`** | 模块私有 | **仅** 同模块页面/私有组件 import |
| **`layout/modules/*`** | 域壳布局 | 非页面组件；不放业务表单 |

## 反冗余

- 同一 UI **≥2 个模块** 使用 → 提升到 `@/components/`，删除模块内重复
- 仅单模块使用 → 留在 `pages/{id}/components/`，**禁止** 放入全局库
- 禁止在页面内复制粘贴与全局库等价的组件

## MUI · Tailwind · CSS Modules

- MUI 路径导入：`import Box from "@mui/material/Box"`
- Tailwind 布局类与 MUI 组件混用（见 `pages/studio-shell` 示例）
- 模块样式：`pages/{id}/styles/*.module.css`
- 主题/token：`components/theme.ts` · `syncThemeVars.ts` · `styles/tokens.css`

## charts · motion

- 图表：`@/components/charts`（LineChart · BarChart）
- 动效：`@/styles/motion`（MotionContainer · MOTION_PRESETS）

## 导出

优先路径导入：`import { PageLoading } from "@/components/PageLoading"`  
 barrel：`@/components`（仅稳定、少变的入口）

## 门禁

`pnpm check` · `bash scripts/py.sh scripts/check_harness.py`（sector contracts 对账）

## 变更纪律

- 结构变更须 **用户确认** + `contracts/directory-readmes.yaml`
- 改 registry/契约须同步 `contracts/README.md` 追踪链

## 相关文档

- [ARCHITECTURE.md](../../ARCHITECTURE.md) · [ENGINEERING.md](../../ENGINEERING.md)
