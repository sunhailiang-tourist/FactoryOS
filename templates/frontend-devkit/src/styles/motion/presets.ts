/**
 * 模块：src/apps/web-admin/src/styles/motion/presets.ts
 * 作用：animate.css 白名单预设
 * 怎么用：MotionContainer preset="enter" 或手动 className={MOTION_PRESETS.enter}
 * 解决：动效可控 · harness 可审计 · 禁止随意 animate class
 * 上游：styles/global.css animate 子集 import
 * 下游：MotionContainer.tsx · 业务页
 * 关联：styles/motion/contracts/README.md
 */
export const MOTION_PRESETS = {
  enter: "animate__animated animate__fadeIn",
  enterUp: "animate__animated animate__fadeInUp",
  pulse: "animate__animated animate__pulse",
} as const;

export type MotionPreset = keyof typeof MOTION_PRESETS;

export function motionClass(preset: MotionPreset): string {
  return MOTION_PRESETS[preset];
}
