/**
 * 模块：src/apps/web-admin/src/components/ApiErrorBanner.tsx
 * 作用：统一展示 ApiError / 未知错误（MUI Alert）
 * 怎么用：表单提交 catch 后 <ApiErrorBanner error={err} />
 * 解决：业务码文案与 trace 展示一致，避免每页重复 Alert
 * 上游：api/request/errors.ts · 页面/表单 catch
 * 下游：用户可读错误反馈
 * 关联：docs/文档/规格说明/状态码与错误约定.md · W-09
 */
import Alert from "@mui/material/Alert";
import AlertTitle from "@mui/material/AlertTitle";
import Typography from "@mui/material/Typography";
import { formatErrorLabel } from "@/api/request/error-codes";
import { ApiError } from "@/api/request/errors";

type ApiErrorBannerProps = {
  error: unknown;
  title?: string;
  onClose?: () => void;
};

function resolveMessage(error: unknown): { code?: string; message: string; traceId?: string } {
  if (error instanceof ApiError) {
    return {
      code: error.code,
      message: error.message,
      traceId: error.body.trace_id,
    };
  }
  if (error instanceof Error) {
    return { message: error.message };
  }
  return { message: "发生未知错误" };
}

/**
 * 功能：ApiErrorBanner 导出函数。
 * 业务含义：web-admin 模块对外入口。
 * 上游：同文件文件头。
 * 下游：见调用链。
 */
export function ApiErrorBanner({ error, title = "请求失败", onClose }: ApiErrorBannerProps) {
  // 业务：ApiErrorBanner 主体编排（见文件头上下游）
  const { code, message, traceId } = resolveMessage(error);

  return (
    <Alert severity="error" onClose={onClose} sx={{ mb: 2 }}>
      <AlertTitle>{title}</AlertTitle>
      <Typography variant="body2" component="div">
        {message}
      </Typography>
      {code ? (
        <Typography variant="caption" color="text.secondary" display="block">
          {formatErrorLabel(code)}
          {traceId ? ` · trace: ${traceId}` : ""}
        </Typography>
      ) : null}
    </Alert>
  );
}
