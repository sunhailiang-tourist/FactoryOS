/**
 * 模块：src/apps/web-admin/src/styles/motion/MotionContainer.tsx
 * 作用：animate.css 预设容器 · 尊重 prefers-reduced-motion
 * 怎么用：<MotionContainer preset="enterUp">{children}</MotionContainer>
 * 解决：步骤切换/空状态统一动效入口
 * 上游：styles/motion/presets.ts
 * 下游：pages/* lazy 页面
 * 关联：styles/motion/contracts/README.md
 */
import type { ReactNode } from "react";
import { motionClass, type MotionPreset } from "./presets";

export type MotionContainerProps = {
  children: ReactNode;
  preset?: MotionPreset;
  className?: string;
};

/**
 * 功能：MotionContainer 导出函数。
 * 业务含义：web-admin 模块对外入口。
 * 上游：同文件文件头。
 * 下游：见调用链。
 */
export function MotionContainer({ children, preset = "enter", className }: MotionContainerProps) {
  const classes = [motionClass(preset), className].filter(Boolean).join(" ");
  return <div className={classes}>{children}</div>;
}
