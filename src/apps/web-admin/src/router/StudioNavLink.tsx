/**
 * 模块：src/apps/web-admin/src/router/StudioNavLink.tsx
 * 作用：侧栏导航 Link + hover/focus 预取
 * 怎么用：StudioShellLayout 步骤列表
 * 解决：意图预取 flows 与 lazy chunk
 * 上游：prefetch.ts · QueryClient
 * 下游：react-router Link
 * 关联：ENGINEERING.md §10 S4
 */
import ListItemButton from "@mui/material/ListItemButton";
import ListItemText from "@mui/material/ListItemText";
import type { ReactNode } from "react";
import { Link } from "react-router-dom";
import { useQueryClient } from "@tanstack/react-query";
import { prefetchStudioNavigation } from "@/router/prefetch";

type StudioNavLinkProps = {
  to: string;
  selected: boolean;
  primary: ReactNode;
  secondary?: ReactNode;
  moduleId?: string;
  endAdornment?: ReactNode;
  disabled?: boolean;
};

export function StudioNavLink({
  to,
  selected,
  primary,
  secondary,
  moduleId,
  endAdornment,
  disabled,
}: StudioNavLinkProps) {
  const queryClient = useQueryClient();
  const prefetch = () => prefetchStudioNavigation(queryClient, moduleId);

  return (
    <ListItemButton
      component={Link}
      to={to}
      selected={selected}
      disabled={disabled}
      onMouseEnter={prefetch}
      onFocus={prefetch}
    >
      <ListItemText primary={primary} secondary={secondary} />
      {endAdornment}
    </ListItemButton>
  );
}
