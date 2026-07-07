# i18n · 板块契约

## 是什么

国际化 sector：`i18n/registry.ts` glob 聚合 `i18n/modules/{namespace}/` 文案 JSON。

## 登记索引

| namespace | module-id | 说明 |
|-----------|-----------|------|
| `_platform` | — | 壳层 · RBAC 提示 · Studio 导航共用文案 |
| `studio-shell` | studio-shell | 概览页 |
| `studio-connect` | studio-connect | 连接步 |
| `studio-discover` | studio-discover | 发现步 |
| `studio-map` | studio-map | 映射步 |
| `studio-prove` | studio-prove | 验证步 |
| `studio-freeze` | studio-freeze | 冻结步 |
| `studio-export` | studio-export | 导出步 |

## 变更规则

1. 新增 `pages/{module-id}` → 同步 `i18n/modules/{module-id}/zh-CN.json` + `en-US.json` + 本表。
2. 页面/布局只经 `@/i18n/core/useT` 消费；禁止直引 `i18next` / `react-i18next`（ESLint）。
3. `pages/{id}/contracts/README.md` 追踪链须含 `i18n namespace` 行。
