/**
 * 模块：src/apps/web-admin/src/components/forms/forms.test.tsx
 * 作用：useAppForm + FormTextField 基座冒烟
 * 怎么用：vitest run 自动执行
 * 解决：RHF+Zod 接线可用
 * 上游：forms primitives
 * 下游：W-09
 * 关联：ENGINEERING.md §6
 */
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";
import { FormTextField } from "./FormTextField";
import { demoTenantSchema } from "./schemas";
import { useAppForm } from "./useAppForm";

function DemoForm() {
  const form = useAppForm(demoTenantSchema, { tenantId: "", displayName: "" });
  return (
    <form onSubmit={form.handleSubmit(() => undefined)}>
      <FormTextField control={form.control} name="tenantId" label="租户 ID" />
      <FormTextField control={form.control} name="displayName" label="显示名" />
      <button type="submit">提交</button>
    </form>
  );
}

describe("forms primitives", () => {
  it("shows zod validation on blur", async () => {
    const user = userEvent.setup();
    render(<DemoForm />);
    const tenant = screen.getByLabelText("租户 ID");
    await user.click(tenant);
    await user.tab();
    expect(await screen.findByText(/至少 3 个字符/)).toBeInTheDocument();
  });
});
