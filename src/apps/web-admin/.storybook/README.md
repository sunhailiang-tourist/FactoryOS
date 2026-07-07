# .storybook · Storybook 配置

## 是什么

组件隔离文档与视觉基座（W-08）；与 Vite 共用 alias。

## 子路径

| 路径 | 说明 |
|------|------|
| `main.ts` | stories glob · Vite 插件 |
| `preview.ts` | 全局 decorator |
| `../src/**/*.stories.tsx` | story 源文件 |

## 门禁

```bash
pnpm storybook
pnpm storybook:build
pnpm check
```

## 变更纪律

- 改 main.ts glob 须同步 harness storybook_config
- 结构扩展须用户确认

## 相关文档

- [ENGINEERING.md](../ENGINEERING.md)
