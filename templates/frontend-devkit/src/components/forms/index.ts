/**
 * 模块：src/apps/web-admin/src/components/forms/index.ts
 * 作用：表单 primitives barrel 导出
 * 怎么用：import { useAppForm, FormTextField } from '@/components/forms'
 * 解决：RHF+Zod 基座统一出口
 * 上游：forms 各实现文件
 * 下游：pages 业务表单
 * 关联：ARCHITECTURE.md v1.9 · W-09
 */
export { FormTextField } from "./FormTextField";
export { useAppForm } from "./useAppForm";
export { demoTenantSchema, type DemoTenantFormValues } from "./schemas";
