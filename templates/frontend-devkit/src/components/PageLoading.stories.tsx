/**
 * 模块：src/apps/web-admin/src/components/PageLoading.stories.tsx
 * 作用：PageLoading Storybook catalog 条目
 * 怎么用：pnpm storybook 浏览 Global/Feedback
 * 解决：全局 loading 组件可视化回归基座
 * 上游：PageLoading.tsx · AppThemeProvider
 * 下游：Storybook W-08
 * 关联：.storybook/preview.tsx
 */
import type { Meta, StoryObj } from "@storybook/react";
import { PageLoading } from "./PageLoading";

const meta: Meta<typeof PageLoading> = {
  title: "Global/Feedback/PageLoading",
  component: PageLoading,
  tags: ["autodocs"],
};

export default meta;

type Story = StoryObj<typeof PageLoading>;

export const Default: Story = {};

export const CustomLabel: Story = {
  args: { label: "正在加载 Studio…" },
};
