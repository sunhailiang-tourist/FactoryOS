/**
 * 模块：src/apps/web-admin/src/pages/studio-shell/StudioHomePage.stories.tsx
 * 作用：Studio 概览页 Storybook catalog
 * 怎么用：pnpm storybook → Pages/Studio/Home
 * 解决：shell 模块可视化基线
 * 上游：StudioHomePage.lazy.tsx · withStudioFlows
 * 下游：W-08 七模块 stories
 * 关联：pages/studio-shell/contracts/README.md
 */
import type { Meta, StoryObj } from "@storybook/react";
import { withPadding, withStudioFlows } from "../../../.storybook/decorators";
import StudioHomePage from "./StudioHomePage.lazy";

const meta: Meta<typeof StudioHomePage> = {
  title: "Pages/Studio/Home",
  component: StudioHomePage,
  decorators: [withStudioFlows(), (Story) => withPadding(<Story />)],
  tags: ["autodocs"],
};

export default meta;

type Story = StoryObj<typeof StudioHomePage>;

export const Default: Story = {};
