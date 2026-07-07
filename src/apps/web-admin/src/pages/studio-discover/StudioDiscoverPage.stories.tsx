/**
 * 模块：src/apps/web-admin/src/pages/studio-discover/StudioDiscoverPage.stories.tsx
 * 作用：Discover 步 Storybook catalog
 * 怎么用：pnpm storybook → Pages/Studio/Discover
 * 解决：module-id studio-discover 可视化基线
 * 上游：StudioDiscoverPage.lazy.tsx
 * 下游：W-08
 * 关联：pages/studio-discover/contracts/README.md
 */
import type { Meta, StoryObj } from "@storybook/react";
import { withPadding } from "../../../.storybook/decorators";
import StudioDiscoverPage from "./StudioDiscoverPage.lazy";

const meta: Meta<typeof StudioDiscoverPage> = {
  title: "Pages/Studio/Discover",
  component: StudioDiscoverPage,
  decorators: [(Story) => withPadding(<Story />)],
  tags: ["autodocs"],
};

export default meta;

type Story = StoryObj<typeof StudioDiscoverPage>;

export const Default: Story = {};
