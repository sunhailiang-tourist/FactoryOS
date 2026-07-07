/**
 * 模块：src/apps/web-admin/src/rbac/core/evaluate.test.ts
 * 作用：RBAC 纯函数单测
 * 怎么用：vitest
 * 解决：角色/路由权限可回归
 * 上游：rbac/core/evaluate.ts
 * 下游：vitest
 * 关联：WEB-PROFILE S5
 */

    import { describe, expect, it } from "vitest";
    import { can, canAccessDomain, canAccessRoute } from "@/rbac/core/evaluate";

    describe("rbac evaluate", () => {
      it("allows integrator studio.shell.view", () => {
        expect(can("integrator", "studio.shell.view")).toBe(true);
      });

      it("denies operator studio routes", () => {
        expect(canAccessRoute("operator", ["studio.shell.view"])).toBe(false);
      });

      it("allows integrator studio domain", () => {
        expect(canAccessDomain("integrator", "studio")).toBe(true);
      });
    });
