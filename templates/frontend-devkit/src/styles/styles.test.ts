/**
 * 模块：src/apps/web-admin/src/styles/styles.test.ts
 * 作用：Vitest：motion 预设与 token 契约冒烟
 * 怎么用：pnpm test styles.test
 * 解决：动效白名单与 preset API 回归
 * 上游：styles/motion/presets.ts
 * 下游：CI pnpm check
 * 关联：styles/motion/contracts/README.md · styles/contracts/README.md
 */
import { describe, expect, it } from "vitest";
import { MOTION_PRESETS, motionClass } from "@/styles/motion/presets";

describe("styles & motion baseline", () => {
  it("exposes animate.css whitelist presets", () => {
    expect(motionClass("enter")).toContain("animate__fadeIn");
    expect(motionClass("enterUp")).toContain("animate__fadeInUp");
    expect(motionClass("pulse")).toContain("animate__pulse");
    expect(Object.keys(MOTION_PRESETS)).toEqual(["enter", "enterUp", "pulse"]);
  });
});
