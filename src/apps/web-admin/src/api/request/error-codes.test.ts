/**
 * 模块：src/apps/web-admin/src/api/request/error-codes.test.ts
 * 作用：ERROR_MESSAGES_ZH · formatErrorLabel 回归
 * 怎么用：Vitest：pnpm test error-codes.test.ts
 * 解决：锁死 code + 中文 mirror 与 SSOT 一致
 * 上游：error-codes.ts · sync_error_registry.py
 * 下游：CI pnpm check
 * 关联：状态码与错误约定.md
 */
import { describe, expect, it } from "vitest";
import {
  ERROR_CODES,
  ERROR_MESSAGES_ZH,
  formatErrorLabel,
  getErrorMessageZh,
} from "./error-codes";

describe("error-codes message_zh mirror", () => {
  it("every ERROR_CODES has non-empty Chinese message", () => {
    for (const code of Object.values(ERROR_CODES)) {
      expect(ERROR_MESSAGES_ZH[code].length).toBeGreaterThan(0);
    }
  });

  it("getErrorMessageZh returns SSOT text", () => {
    expect(getErrorMessageZh(ERROR_CODES.AUTH_STUDIO_FORBIDDEN)).toBe(
      "Studio 访问被拒绝：当前角色无权限",
    );
  });

  it("formatErrorLabel combines code and Chinese", () => {
    expect(formatErrorLabel(ERROR_CODES.MAPPING_ERROR)).toBe(
      "MAPPING_ERROR · 字段映射或参数校验失败",
    );
  });

  it("falls back to UNKNOWN_ERROR message for unknown code", () => {
    expect(getErrorMessageZh("NOT_A_REAL_CODE")).toBe(ERROR_MESSAGES_ZH.UNKNOWN_ERROR);
  });
});
