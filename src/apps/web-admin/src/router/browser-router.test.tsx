/**
     * 模块：src/apps/web-admin/src/router/browser-router.test.tsx
     * 作用：createAppRouter 冒烟
     * 怎么用：vitest run
     * 解决：data router 工厂可实例化
     * 上游：createQueryClient
     * 下游：bootstrap
     * 关联：W-06
     */
    import { describe, expect, it } from "vitest";
    import { createQueryClient } from "@/api/query/client";
    import { createAppRouter } from "@/router/browser-router";

    describe("createAppRouter", () => {
      it("creates a data router with studio routes", () => {
        const router = createAppRouter(createQueryClient());
        expect(router.routes.length).toBeGreaterThan(0);
      });
    });
