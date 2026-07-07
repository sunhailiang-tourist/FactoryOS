# api · 板块契约

## 是什么

HTTP 实体函数板块：`api/registry.ts`（glob 聚合 `api/functions/*/registry.ts`）。

## 登记索引

| module-id | api id | fn | path |
|-----------|--------|-----|------|
| `studio-connect` | studio.connect.test | postConnectTest | POST /v1/integration/connect/test |
| `studio-shell` | studio.flows.list | getStudioFlows | GET /v1/studio/flows |

传输层唯一出口：`api/request/client.ts`。  
Server State 唯一入口：`api/query/hooks/*`（pages 禁直引 `api/functions`）。

## 变更规则

1. 新增 `api/functions/{id}/*.fn.ts` + `API_MODULE_ENTRIES` → **同步** 本表 + `pages/{id}/contracts/README.md`（api id 行）。
2. registry 中 `fn` 必须在同目录 `*.fn.ts` 导出（harness 校验）。
3. 禁止 pages 直接 `fetch`。
