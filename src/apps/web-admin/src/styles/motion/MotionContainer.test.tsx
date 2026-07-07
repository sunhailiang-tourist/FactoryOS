/**
 * 模块：src/apps/web-admin/src/styles/motion/MotionContainer.test.tsx
 * 作用：MotionContainer RTL 冒烟
 * 怎么用：vitest run MotionContainer.test.tsx
 * 解决：preset className 注入与 children 渲染
 * 上游：styles/motion/presets.ts
 * 下游：pages lazy 动效入口
 * 关联：styles/motion/contracts/README.md
 */
import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { MotionContainer } from "./MotionContainer";
import { MOTION_PRESETS } from "./presets";

describe("MotionContainer", () => {
  it("applies preset animate classes", () => {
    const { container } = render(
      <MotionContainer preset="enterUp">
        <span>content</span>
      </MotionContainer>,
    );
    const root = container.firstElementChild;
    expect(root).toHaveClass(...MOTION_PRESETS.enterUp.split(" "));
    expect(screen.getByText("content")).toBeInTheDocument();
  });
});
