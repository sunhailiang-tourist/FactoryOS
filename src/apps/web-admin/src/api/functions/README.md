# api/functions · 实体函数

按 **路由 module** 分子目录；每目录含 `*.fn.ts`（实体函数）+ `registry.ts`（子表）。

**禁止** 直接 `fetch`；**必须** `import { http } from '@/api/request'`。

## 命名

| 项 | 规则 |
|----|------|
| 目录 | 与 `modules/{id}` 一致，如 `studio-connect` |
| 文件 | `{entity}.fn.ts` |
| 函数 | `get/post/put/del` + 实体，如 `getStudioFlows` |
| 子表 | `registry.ts` 导出 **`API_MODULE_ENTRIES`**（glob 自动聚合） |
