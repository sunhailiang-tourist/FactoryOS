# motion · 板块契约

## 是什么

animate.css 子集 + 白名单预设：`styles/motion/presets.ts` · `MotionContainer.tsx`。

## 登记索引

| 导出 | 文件 | 说明 |
|------|------|------|
| `MOTION_PRESETS` | `presets.ts` | 白名单 class 映射 |
| `motionClass` | `presets.ts` | preset → className |
| `MotionContainer` | `MotionContainer.tsx` | 预设容器 |

## 变更规则

1. 新增 preset → 先在 `styles/global.css` import 对应 animate 源文件，再登记 `presets.ts` 与本表。
2. 禁止在 pages 直接使用未登记 `animate__*` class。
3. 动效时长/曲线不在业务页覆盖；统一在 global.css reduced-motion 规则。
