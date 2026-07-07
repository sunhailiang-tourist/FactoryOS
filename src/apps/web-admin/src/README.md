# src · 前端源码根

## 是什么

web-admin **运行时源码树**：壳层 bootstrap · sector 注册制 · API 四层 · MSW 假数据。

## 子路径

| 路径 | 说明 |
|------|------|
| `api/` | request · functions · query · generated |
| `components/` | 全局 UI（≥2 模块复用） |
| `config/` | 运行时配置登记 |
| `layout/` | 域布局 modules |
| `i18n/` | 文案 namespace registry（zh-CN · en-US） |
| `rbac/` | 权限 domain registry |
| `router/` | module-id 路由 registry |
| `pages/` | 业务页面（按 module-id） |
| `store/` | Zustand 模块 store |
| `styles/` | Token · global CSS |
| `styles/motion/` | animate 白名单（styles 子目录） |
| `mocks/` | MSW handlers |
| `test/` | Vitest setup · render 工具 |

## 门禁

```bash
pnpm check
bash scripts/py.sh scripts/check_harness.py
```

## 变更纪律

- 新 **一级 sector** 须：README + contracts/README + registry 对账 + 用户确认 + directory-readmes
- 禁止 `src/common/`；禁止 pages 内直接 fetch
- 详见 [ARCHITECTURE.md](../ARCHITECTURE.md)

## 相关文档

- [ARCHITECTURE.md](../ARCHITECTURE.md) · [ENGINEERING.md](../ENGINEERING.md)
