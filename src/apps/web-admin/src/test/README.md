# test · Vitest 测试基座

## 是什么

**非业务** 测试基础设施：RTL render 封装 · MSW lifecycle · jest-dom。

## 子路径

| 路径 | 说明 |
|------|------|
| `setup.ts` | vitest setupFiles · MSW server |
| `render.tsx` | QueryClient + Router 测试 render |

## 门禁

```bash
pnpm test
pnpm check
```

## 变更纪律

- 业务断言放 `*.test.ts(x)` 同目录或 sector；本目录仅基座
- 改 setup 须跑全量 vitest + e2e smoke

## 相关文档

- [mocks/README.md](../mocks/README.md)
- [ENGINEERING.md](../../ENGINEERING.md) §6
