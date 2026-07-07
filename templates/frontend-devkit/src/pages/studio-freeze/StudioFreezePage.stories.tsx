/**
 * 模块：src/apps/web-admin/src/pages/studio-freeze/StudioFreezePage.stories.tsx
 * 作用：Freeze 步 Storybook catalog
 * 怎么用：pnpm storybook → Pages/Studio/Freeze
 * 解决：module-id studio-freeze 可视化基线
 * 上游：StudioFreezePage.lazy.tsx
 * 下游：W-08
 * 关联：pages/studio-freeze/contracts/README.md
 */
import type { Meta, StoryObj } from "@storybook/react";
import { withPadding } from "../../../.storybook/decorators";
import StudioFreezePage from "./StudioFreezePage.lazy";

const meta: Meta<typeof StudioFreezePage> = {
  title: "Pages/Studio/Freeze",
  component: StudioFreezePage,
  decorators: [(Story) => withPadding(<Story />)],
  tags: ["autodocs"],
};

export default meta;

type Story = StoryObj<typeof StudioFreezePage>;

export const Default: Story = {};
