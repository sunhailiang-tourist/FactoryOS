# motion · 动效预设（`styles/` 子目录）

## 是什么

全局 **animate.css 白名单** 与 `MotionContainer`；隶属 [styles](../README.md) 域，非独立一级 sector。

**克制动效**：仅使用 `styles/motion/presets.ts` 白名单；禁止页面随意拼 `animate__*` class。

## 预设

| preset | class | 用途 |
|--------|-------|------|
| `enter` | fadeIn | 步骤切换 |
| `enterUp` | fadeInUp | 卡片入场 |
| `pulse` | pulse | Gate 结果提示 |

## 无障碍

`styles/global.css` 对 `prefers-reduced-motion: reduce` 缩短动画时长。

## 门禁

`pnpm check` · `bash scripts/py.sh scripts/check_harness.py`（sector contracts 对账）

## 变更纪律

- 结构变更须 **用户确认** + `contracts/directory-readmes.yaml`
- 改 registry/契约须同步 `contracts/README.md` 追踪链

## 相关文档

- [ARCHITECTURE.md](../../../ARCHITECTURE.md) · [ENGINEERING.md](../../../ENGINEERING.md)
