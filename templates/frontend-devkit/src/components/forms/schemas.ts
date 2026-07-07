/**
 * 模块：src/apps/web-admin/src/components/forms/schemas.ts
 * 作用：可复用 Zod schema 片段（架构基座示例）
 * 怎么用：import { demoTenantSchema } from '@/components/forms/schemas'
 * 解决：校验规则与 OpenAPI/业务契约对齐的落点
 * 上游：zod · contracts 字段约定
 * 下游：useAppForm · 业务表单
 * 关联：W-09 · 非生产业务 schema
 */
import { z } from "zod";

/** 示例：租户标识校验（Studio Connect 等可扩展）。 */
export const demoTenantSchema = z.object({
  tenantId: z
    .string()
    .min(3, "租户 ID 至少 3 个字符")
    .regex(/^tn-[a-z0-9-]+$/, "格式须为 tn- 前缀 kebab"),
  displayName: z.string().min(1, "显示名称必填").max(64, "显示名称过长"),
});

export type DemoTenantFormValues = z.infer<typeof demoTenantSchema>;
