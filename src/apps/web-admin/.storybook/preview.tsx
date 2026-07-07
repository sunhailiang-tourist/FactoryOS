/**
 * 模块：src/apps/web-admin/.storybook/preview.tsx
 * 作用：Storybook 全局 decorator — MUI Theme
 * 怎么用：storybook dev/build 自动加载
 * 解决：组件 stories 与生产 Theme 一致
 * 上游：AppThemeProvider
 * 下游：*.stories.tsx
 * 关联：W-08
 */
import type { Preview } from "@storybook/react";
import { AppThemeProvider } from "../src/components/AppThemeProvider";

const preview: Preview = {
  decorators: [
    (Story) => (
      <AppThemeProvider>
        <Story />
      </AppThemeProvider>
    ),
  ],
};

export default preview;
