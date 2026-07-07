/**
 * 模块：src/apps/web-admin/src/i18n/core/useT.test.ts
 * 作用：i18n 资源 smoke
 * 怎么用：vitest
 * 解决：zh/en 平台文案可解析
 * 上游：i18n/core/resources.ts
 * 下游：vitest
 * 关联：WEB-PROFILE S5
 */

    import { describe, expect, it } from "vitest";
    import { buildI18nResources } from "@/i18n/core/resources";

    describe("i18n resources", () => {
      it("loads platform zh-CN studio nav label", () => {
        const resources = buildI18nResources();
        expect(resources["zh-CN"]._platform.studioNavOverview).toBe("概览");
      });

      it("loads platform en-US studio nav label", () => {
        const resources = buildI18nResources();
        expect(resources["en-US"]._platform.studioNavOverview).toBe("Overview");
      });
    });
