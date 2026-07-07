/**
 * 模块：src/apps/web-admin/src/config/env.test.ts
 * 作用：env 常量冒烟
 * 怎么用：vitest run env.test.ts
 * 解决：应用标题等默认值不漂移
 * 上游：config/env.ts
 * 下游：layout · document title
 * 关联：config/contracts/README.md
 */
import { describe, expect, it } from "vitest";
import { env } from "./env";

describe("env", () => {
  it("exposes Integration Studio app title", () => {
    expect(env.appTitle).toContain("Integration Studio");
    expect(env.apiBase).toBe("");
  });
});
