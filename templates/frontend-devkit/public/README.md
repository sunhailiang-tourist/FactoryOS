# public · Vite 静态资源

## 是什么

Vite `public/` 目录：构建时原样复制到站点根路径。

## 子路径

| 文件 | 用途 |
|------|------|
| `mockServiceWorker.js` | MSW 浏览器 worker（`VITE_MSW=1` · `pnpm dev`） |

## 门禁

- 由 `npx msw init public` 生成/更新 worker；勿手改逻辑
- 登记：`contracts/directory-readmes.yaml`

## 变更纪律

1. 增删静态文件 → 同步本 README
2. MSW 版本升级后重新 `msw init public`

## 相关文档

- [src/mocks/README.md](../src/mocks/README.md)
- [ENGINEERING.md](../ENGINEERING.md)
