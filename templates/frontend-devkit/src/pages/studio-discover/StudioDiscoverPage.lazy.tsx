/**
 * 模块：src/apps/web-admin/src/pages/studio-discover/StudioDiscoverPage.lazy.tsx
 * 作用：Discover 发现 lazy 页面入口
 * 怎么用：router/modules/studio-discover/registry.ts lazy import；业务逻辑后续 Step 实现
 * 解决：Graph/资产发现 UI 与路由解耦，支持 code-split
 * 上游：router/modules/studio-discover/registry.ts
 * 下游：api/functions/studio-discover · store/modules/studio-discover
 * 关联：pages/studio-discover/contracts/README.md
 */
import Typography from "@mui/material/Typography";

export default function StudioDiscoverPage() {
  return (
    <>
      <Typography variant="h5" gutterBottom>
        Discover · 发现
      </Typography>
      <Typography variant="body2" color="text.secondary">
        route studio.discover · 阶段 1 Step 4 实现
      </Typography>
    </>
  );
}