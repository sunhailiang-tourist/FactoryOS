/**
 * 模块：src/apps/web-admin/src/api/query/index.ts
 * 作用：query 层 barrel export
 * 怎么用：import { createQueryClient, studioKeys, useStudioFlows } from '@/api/query'
 * 解决：hooks 与 client 统一入口
 * 上游：client.ts · keys.ts · hooks/*
 * 下游：bootstrap · pages · layout
 * 关联：api/query/contracts/README.md
 */
export { createQueryClient } from "./client";
export { studioKeys } from "./keys";
export { useStudioFlows } from "./hooks/useStudioFlows";
