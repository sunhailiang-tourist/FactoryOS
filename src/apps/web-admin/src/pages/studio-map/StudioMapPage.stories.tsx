/**
 * 模块：src/apps/web-admin/src/pages/studio-map/StudioMapPage.stories.tsx
 * 作用：Map 步 Storybook catalog
 * 怎么用：pnpm storybook → Pages/Studio/Map
 * 解决：module-id studio-map 可视化基线
 * 上游：StudioMapPage.lazy.tsx
 * 下游：W-08
 * 关联：pages/studio-map/contracts/README.md
 */
import type { Meta, StoryObj } from "@storybook/react";
import { withPadding } from "../../../.storybook/decorators";
import StudioMapPage from "./StudioMapPage.lazy";

const meta: Meta<typeof StudioMapPage> = {
  title: "Pages/Studio/Map",
  component: StudioMapPage,
  decorators: [(Story) => withPadding(<Story />)],
  tags: ["autodocs"],
};

export default meta;

type Story = StoryObj<typeof StudioMapPage>;

export const Default: Story = {};
