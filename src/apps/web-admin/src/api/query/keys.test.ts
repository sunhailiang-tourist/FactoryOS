/**
 * 模块：src/apps/web-admin/src/api/query/keys.test.ts
 * 作用：queryKey 工厂稳定性测试
 * 怎么用：vitest run keys.test.ts
 * 解决：studioKeys / queryKeys 结构不漂移
 * 上游：api/query/keys.ts
 * 下游：useStudioFlows · invalidate
 * 关联：api/query/contracts/README.md
 */
import { describe, expect, it } from "vitest";
import { queryKeys, studioKeys } from "./keys";

describe("query keys", () => {
  it("studioKeys.flows nests under studio namespace", () => {
    expect(studioKeys.flows()).toEqual(["studio", "flows"]);
  });

  it("queryKeys.module scopes by module-id", () => {
    expect(queryKeys.module("studio-connect")).toEqual(["module", "studio-connect"]);
  });
});
