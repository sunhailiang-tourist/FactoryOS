/**
 * 模块：src/apps/web-admin/src/pages/studio-map/StudioMapPage.lazy.tsx
 * 作用：Map 映射 lazy 页面入口
 * 怎么用：router/modules/studio-map/registry.ts lazy import；业务逻辑后续 Step 实现
 * 解决：字段映射配置 UI 与路由解耦，支持 code-split
 * 上游：router/modules/studio-map/registry.ts
 * 下游：api/functions/studio-map · store/modules/studio-map
 * 关联：pages/studio-map/contracts/README.md
 */
import Typography from "@mui/material/Typography";

export default function StudioMapPage() {
  return (
    <>
      <Typography variant="h5" gutterBottom>
        Map · 映射
      </Typography>
      <Typography variant="body2" color="text.secondary">
        route studio.map · 阶段 1 Step 4 实现
      </Typography>
    </>
  );
}