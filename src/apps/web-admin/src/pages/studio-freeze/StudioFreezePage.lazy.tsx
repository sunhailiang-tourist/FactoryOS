/**
 * 模块：src/apps/web-admin/src/pages/studio-freeze/StudioFreezePage.lazy.tsx
 * 作用：Freeze 冻结 lazy 页面入口
 * 怎么用：router/modules/studio-freeze/registry.ts lazy import；业务逻辑后续 Step 实现
 * 解决：Graph freeze Gate UI 与路由解耦，支持 code-split
 * 上游：router/modules/studio-freeze/registry.ts
 * 下游：api/functions/studio-freeze · store/modules/studio-freeze
 * 关联：pages/studio-freeze/contracts/README.md
 */
import Typography from "@mui/material/Typography";

export default function StudioFreezePage() {
  return (
    <>
      <Typography variant="h5" gutterBottom>
        Freeze · 冻结
      </Typography>
      <Typography variant="body2" color="text.secondary">
        route studio.freeze · 阶段 1 Step 4 实现
      </Typography>
    </>
  );
}