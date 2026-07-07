/**
 * 模块：src/apps/web-admin/src/components/ApiErrorBanner.test.tsx
 * 作用：ApiErrorBanner RTL 冒烟
 * 怎么用：vitest run 自动执行
 * 解决：错误码与 trace 展示契约
 * 上游：ApiErrorBanner · ApiError
 * 下游：W-09 表单基座
 * 关联：ENGINEERING.md §6
 */
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { ApiError } from "@/api/request/errors";
import { ApiErrorBanner } from "./ApiErrorBanner";

describe("ApiErrorBanner", () => {
  it("renders ApiError code and message", () => {
    const err = new ApiError(403, "Studio 访问被拒绝", {
      code: "AUTH_STUDIO_FORBIDDEN",
      message: "Studio 访问被拒绝",
      trace_id: "tr-abc",
    });
    render(<ApiErrorBanner error={err} />);
    expect(screen.getByText("Studio 访问被拒绝")).toBeInTheDocument();
    expect(screen.getByText(/AUTH_STUDIO_FORBIDDEN/)).toBeInTheDocument();
    expect(screen.getByText(/tr-abc/)).toBeInTheDocument();
  });

  it("renders generic Error message", () => {
    render(<ApiErrorBanner error={new Error("network down")} />);
    expect(screen.getByText("network down")).toBeInTheDocument();
  });
});
