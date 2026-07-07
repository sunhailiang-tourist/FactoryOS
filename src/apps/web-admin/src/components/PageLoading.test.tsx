/**
 * 模块：src/apps/web-admin/src/components/PageLoading.test.tsx
 * 作用：PageLoading 无障碍与文案测试
 * 怎么用：vitest run PageLoading.test.tsx
 * 解决：Suspense fallback 默认可测
 * 上游：PageLoading.tsx
 * 下游：AppShell Suspense
 * 关联：PageLoading.stories.tsx
 */
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { PageLoading } from "./PageLoading";

describe("PageLoading", () => {
  it("renders default label and progress", () => {
    render(<PageLoading />);
    expect(screen.getByText("加载中")).toBeInTheDocument();
    expect(screen.getByLabelText("加载中")).toBeInTheDocument();
  });

  it("accepts custom label", () => {
    render(<PageLoading label="正在加载 Studio…" />);
    expect(screen.getByText("正在加载 Studio…")).toBeInTheDocument();
  });
});
