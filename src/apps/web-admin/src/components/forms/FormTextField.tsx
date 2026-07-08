/**
 * 模块：src/apps/web-admin/src/components/forms/FormTextField.tsx
 * 作用：MUI TextField + react-hook-form Controller 封装
 * 怎么用：<FormTextField control={form.control} name="tenantId" label="租户" />
 * 解决：表单字段与校验错误展示一致
 * 上游：useAppForm · MUI TextField
 * 下游：业务 pages 表单区
 * 关联：components/forms · W-09
 */
import TextField, { type TextFieldProps } from "@mui/material/TextField";
import { Controller, type Control, type FieldPath, type FieldValues } from "react-hook-form";

type FormTextFieldProps<T extends FieldValues> = {
  control: Control<T>;
  name: FieldPath<T>;
} & Omit<TextFieldProps, "name" | "value" | "onChange" | "onBlur" | "ref" | "error" | "helperText">;

/**
 * 功能：FormTextField 导出函数。
 * 业务含义：web-admin 模块对外入口。
 * 上游：同文件文件头。
 * 下游：见调用链。
 */
export function FormTextField<T extends FieldValues>({
  // 业务：FormTextField 主体编排（见文件头上下游）
  control,
  name,
  label,
  ...rest
}: FormTextFieldProps<T>) {
  return (
    <Controller
      control={control}
      name={name}
      render={({ field, fieldState }) => (
        <TextField
          {...field}
          {...rest}
          label={label}
          error={Boolean(fieldState.error)}
          helperText={fieldState.error?.message}
          fullWidth
          margin="normal"
        />
      )}
    />
  );
}
