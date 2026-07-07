# mocks · MSW 假数据层

## 是什么

本地 **无后端** 开发/测试用的 API mock（`VITE_MSW=1` · Vitest `server.listen`）。

## 子路径

| 路径 | 说明 |
|------|------|
| `browser.ts` | dev worker 入口 |
| `server.ts` | Vitest node 入口 |
| `handlers/` | 按 module-id 分文件 handlers |
| `handlers/index.ts` | handlers 聚合 |

## 门禁

```bash
VITE_MSW=1 pnpm dev
pnpm test
```

## 变更纪律

- handler 须对齐 `api/functions` 路径；改 API 须同步 mock
- `handlers/` 为实现子目录，无须单独登记 directory-readmes

## 相关文档

- [api/README.md](../api/README.md)
- [test/README.md](../test/README.md)
