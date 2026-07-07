/**
 * 模块：src/apps/web-admin/src/store/modules/studio-shell/studio-shell.store.ts
 * 作用：studio-shell 纯 UI 态 Zustand store
 * 怎么用：layout import useStudioShellStore；Server State 走 useStudioFlows
 * 解决：侧栏折叠等本地 UI 与 API 缓存分离（v1.7）
 * 上游：pages/studio-shell · layout/modules/studio
 * 下游：StudioShellLayout
 * 关联：pages/studio-shell/contracts/README.md · api/query/hooks/useStudioFlows
 */
import { create } from "zustand";

type StudioShellState = {
  sidebarCollapsed: boolean;
  setSidebarCollapsed: (collapsed: boolean) => void;
  toggleSidebar: () => void;
};

export const useStudioShellStore = create<StudioShellState>((set) => ({
  sidebarCollapsed: false,
  setSidebarCollapsed: (collapsed) => set({ sidebarCollapsed: collapsed }),
  toggleSidebar: () => set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),
}));
