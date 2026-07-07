/**
 * 模块：src/apps/web-admin/src/pages/studio-connect/StudioConnectPage.stories.tsx
 * 作用：Connect 步 Storybook catalog
 * 怎么用：pnpm storybook → Pages/Studio/Connect
 * 解决：module-id studio-connect 可视化基线
 * 上游：StudioConnectPage.lazy.tsx
 * 下游：W-08
 * 关联：pages/studio-connect/contracts/README.md
 */
import type { Meta, StoryObj } from "@storybook/react";
import { withPadding } from "../../../.storybook/decorators";
import StudioConnectPage from "./StudioConnectPage.lazy";

const meta: Meta<typeof StudioConnectPage> = {
  title: "Pages/Studio/Connect",
  component: StudioConnectPage,
  decorators: [(Story) => withPadding(<Story />)],
  tags: ["autodocs"],
};

export default meta;

type Story = StoryObj<typeof StudioConnectPage>;

export const Default: Story = {};
