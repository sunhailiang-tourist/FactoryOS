# config · 板块契约

## 是什么

Feature flag 板块：`config/registry.ts`（glob 聚合 `config/modules/{domain}/`）。

## 登记索引

| domain | config-id | enabled | 说明 |
|--------|-----------|---------|------|
| `studio` | studio.wizard | true | Integration Studio 六步向导 |

运行时查询：`isConfigEnabled(configId)`。

## 变更规则

1. 新增 `config/modules/{domain}/registry.ts` → **同步** 本表。
2. 关闭功能须 `enabled: false` 并在路由/布局消费处调用 `isConfigEnabled`（后续 Step 接线）。
3. 环境变量仍用 `config/env.ts`（非 registry 子表）。
