# api · API 平面

| 层 | 目录 | 职责 |
|----|------|------|
| HTTP | `request/` | 传输封装 · 拦截器 · 错误 |
| 实体函数 | `functions/{module}/` | 业务语义 API 调用 |
| 登记 | `registry.ts` | 全站 API_REGISTRY（glob 聚合 · `API_MODULE_ENTRIES`） |

调用链：`page → store → functions/*.fn.ts → request/client → /v1/*`

## 门禁

`pnpm check` · `bash scripts/py.sh scripts/check_harness.py`（sector contracts 对账）

## 变更纪律

- 结构变更须 **用户确认** + `contracts/directory-readmes.yaml`
- 改 registry/契约须同步 `contracts/README.md` 追踪链

## 相关文档

- [ARCHITECTURE.md](../../ARCHITECTURE.md) · [ENGINEERING.md](../../ENGINEERING.md)
