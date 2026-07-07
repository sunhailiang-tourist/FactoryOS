/**
 * 模块：src/apps/web-admin/src/styles/motion/presets.test.ts
 * 作用：animate 白名单预设单元测试
 * 怎么用：vitest run presets.test.ts
 * 解决：motionClass 与 MOTION_PRESETS 键一致
 * 上游：styles/motion/presets.ts
 * 下游：MotionContainer · harness
 * 关联：styles/motion/contracts/README.md
 */
import { describe, expect, it } from "vitest";
import { MOTION_PRESETS, motionClass, type MotionPreset } from "./presets";

describe("motion presets", () => {
  it("exposes enter / enterUp / pulse animate classes", () => {
    const keys: MotionPreset[] = ["enter", "enterUp", "pulse"];
    for (const key of keys) {
      expect(motionClass(key)).toBe(MOTION_PRESETS[key]);
      expect(motionClass(key)).toMatch(/^animate__animated/);
    }
  });
});
