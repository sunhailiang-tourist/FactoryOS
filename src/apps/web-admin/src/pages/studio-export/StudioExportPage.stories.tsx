/**
 * 模块：src/apps/web-admin/src/pages/studio-export/StudioExportPage.stories.tsx
 * 作用：Export 步 Storybook catalog
 * 怎么用：pnpm storybook → Pages/Studio/Export
 * 解决：module-id studio-export 可视化基线
 * 上游：StudioExportPage.lazy.tsx
 * 下游：W-08
 * 关联：pages/studio-export/contracts/README.md
 */
import type { Meta, StoryObj } from "@storybook/react";
import { withPadding } from "../../../.storybook/decorators";
import StudioExportPage from "./StudioExportPage.lazy";

const meta: Meta<typeof StudioExportPage> = {
  title: "Pages/Studio/Export",
  component: StudioExportPage,
  decorators: [(Story) => withPadding(<Story />)],
  tags: ["autodocs"],
};

export default meta;

type Story = StoryObj<typeof StudioExportPage>;

export const Default: Story = {};
