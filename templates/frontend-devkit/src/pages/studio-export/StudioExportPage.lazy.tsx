/**
 * 模块：src/apps/web-admin/src/pages/studio-export/StudioExportPage.lazy.tsx
 * 作用：Export 导出 lazy 页面入口
 * 怎么用：router/modules/studio-export/registry.ts lazy import；业务逻辑后续 Step 实现
 * 解决：Package export UI 与路由解耦，支持 code-split
 * 上游：router/modules/studio-export/registry.ts
 * 下游：api/functions/studio-export · store/modules/studio-export
 * 关联：pages/studio-export/contracts/README.md
 */
import Typography from "@mui/material/Typography";

export default function StudioExportPage() {
  return (
    <>
      <Typography variant="h5" gutterBottom>
        Export · 导出
      </Typography>
      <Typography variant="body2" color="text.secondary">
        route studio.export · 阶段 1 Step 4 实现
      </Typography>
    </>
  );
}