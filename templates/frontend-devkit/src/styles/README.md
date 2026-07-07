# styles · 全局样式与 Design Token

**真源**：MUI `components/theme.ts` → `syncThemeVars()` → `:root` CSS Variables → Tailwind `@theme`。

## 文件

| 文件 | 职责 |
|------|------|
| `tokens.css` | `:root` 默认值（首屏/SSR） |
| `global.css` | Tailwind v4 + animate 子集；**无** preflight |
| `contracts/README.md` | 样式分层契约 |
| `motion/` | animate 白名单 · MotionContainer |

## 分层（与 ARCHITECTURE §8 一致）

1. **MUI** — 表单/表格/Dialog 组件语义
2. **Tailwind** — 布局原子类（`flex` · `gap-*` · `p-*`）
3. **CSS Modules** — `pages/{module-id}/styles/*.module.css` 模块私有

## 禁止

- 页面内硬编码 hex 色值（须用 token 或 MUI theme）
- 全局裸 CSS 选择器（除本目录与 `.module.css`）

## 门禁

`pnpm check` · `bash scripts/py.sh scripts/check_harness.py`（sector contracts 对账）

## 变更纪律

- 结构变更须 **用户确认** + `contracts/directory-readmes.yaml`
- 改 registry/契约须同步 `contracts/README.md` 追踪链

## 相关文档

- [ARCHITECTURE.md](../../ARCHITECTURE.md) · [ENGINEERING.md](../../ENGINEERING.md)
