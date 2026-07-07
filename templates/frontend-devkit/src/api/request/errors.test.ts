/**
 * 模块：src/apps/web-admin/src/api/request/errors.test.ts
 * 作用：api/request/errors 单元测试
 * 怎么用：Vitest：pnpm test errors.test.ts
 * 解决：回归 parseApiErrorBody 与 ErrorCode 映射
 * 上游：errors.ts · error-codes.ts
 * 下游：CI pnpm check
 * 关联：ENGINEERING.md §6
 */
import { describe, expect, it } from "vitest";
import { ERROR_CODES } from "./error-codes";
import { parseApiErrorBody } from "./errors";

describe("parseApiErrorBody", () => {
  it("parses standard FactoryOSError shape", () => {
    const body = parseApiErrorBody(
      {
        code: ERROR_CODES.AUTH_STUDIO_FORBIDDEN,
        message: "Studio 访问被拒绝",
        detail: "Studio 访问被拒绝",
        details: { role: "operator" },
        trace_id: "tr-1",
      },
      403,
    );
    expect(body.code).toBe(ERROR_CODES.AUTH_STUDIO_FORBIDDEN);
    expect(body.message).toBe("Studio 访问被拒绝");
    expect(body.trace_id).toBe("tr-1");
  });

  it("falls back to UNKNOWN_ERROR for non-object body", () => {
    const body = parseApiErrorBody("bad gateway", 502);
    expect(body.code).toBe(ERROR_CODES.UNKNOWN_ERROR);
    expect(body.message).toBe("bad gateway");
  });

  it("uses message_zh when API returns code without message", () => {
    const body = parseApiErrorBody({ code: ERROR_CODES.MAPPING_ERROR }, 422);
    expect(body.message).toBe("字段映射或参数校验失败");
  });
});