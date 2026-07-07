/**
 * 模块：src/apps/web-admin/src/components/forms/useAppForm.ts
 * 作用：RHF + Zod resolver 统一工厂
 * 怎么用：const form = useAppForm(schema, defaults)
 * 解决：表单校验与 TS 类型一处定义
 * 上游：react-hook-form · zod · @hookform/resolvers
 * 下游：FormTextField 等 primitives
 * 关联：ARCHITECTURE.md v1.9 · W-09
 */
import { zodResolver } from "@hookform/resolvers/zod";
import { useForm, type DefaultValues, type FieldValues, type UseFormReturn } from "react-hook-form";
import type { ZodType } from "zod";

export function useAppForm<TFieldValues extends FieldValues>(
  schema: ZodType<TFieldValues>,
  defaultValues?: DefaultValues<TFieldValues>,
): UseFormReturn<TFieldValues> {
  return useForm<TFieldValues>({
    resolver: zodResolver(schema),
    defaultValues,
    mode: "onBlur",
  });
}
