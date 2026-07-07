# form · 板块契约

## 是什么

从 OpenAPI `components.schemas` 生成 **表单 + Zod 校验** 的机器区（`pages/{module-id}/generated/`）。
列表页生成属同一工具链的扩展项；工具目录为 `scripts/form/`（**不**挂在 `codegen/` 下）。

## 登记索引

| 路径 | 职责 |
|------|------|
| `scripts/form/generate.mjs` | CLI：`pnpm form:generate`（S7 实施） |
| `pages/{id}/generated/*.generated.tsx` | 机器区 · 禁止手改 |
| `components/crud/CrudForm.tsx` | 手写薄壳复用的表单 primitive（S7） |

## 追踪链

| 项 | 值 |
|----|-----|
| 输入 SSOT | `vendor/factoryos-contracts/openapi/` |
| 输出 | `api/functions` · `api/query/hooks` · `pages/{id}/generated/` |
| 演示包 | `pages/demo-crud/`（`demo-` 前缀 · 整包可删） |

## 变更规则

1. 生成物变更只跑 `pnpm form:generate` · `pnpm form:check` diff 须为空。
2. 手写页面只组合 `generated` + `@/components/crud`，不复制字段映射逻辑。
