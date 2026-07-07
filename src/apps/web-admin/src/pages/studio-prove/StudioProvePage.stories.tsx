/**
 * 模块：src/apps/web-admin/src/pages/studio-prove/StudioProvePage.stories.tsx
 * 作用：Prove 步 Storybook catalog
 * 怎么用：pnpm storybook → Pages/Studio/Prove
 * 解决：module-id studio-prove 可视化基线
 * 上游：StudioProvePage.lazy.tsx
 * 下游：W-08
 * 关联：pages/studio-prove/contracts/README.md
 */
import type { Meta, StoryObj } from "@storybook/react";
import { withPadding } from "../../../.storybook/decorators";
import StudioProvePage from "./StudioProvePage.lazy";

const meta: Meta<typeof StudioProvePage> = {
  title: "Pages/Studio/Prove",
  component: StudioProvePage,
  decorators: [(Story) => withPadding(<Story />)],
  tags: ["autodocs"],
};

export default meta;

type Story = StoryObj<typeof StudioProvePage>;

export const Default: Story = {};
