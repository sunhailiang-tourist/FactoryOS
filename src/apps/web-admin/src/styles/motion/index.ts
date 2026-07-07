/**
 * 模块：src/apps/web-admin/src/styles/motion/index.ts
 * 作用：motion 板块稳定导出
 * 怎么用：import { MotionContainer, MOTION_PRESETS } from '@/styles/motion'
 * 解决：动效 API 单点
 * 上游：presets.ts · MotionContainer.tsx
 * 下游：pages/*
 * 关联：styles/motion/contracts/README.md
 */
export { MotionContainer } from "./MotionContainer";
export type { MotionContainerProps } from "./MotionContainer";
export { MOTION_PRESETS, motionClass } from "./presets";
export type { MotionPreset } from "./presets";
