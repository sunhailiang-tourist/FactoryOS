/**
 * 模块：src/apps/web-admin/src/registry.harness.test.ts
 * 作用：Vitest：registry glob 完整性冒烟
 * 怎么用：pnpm test registry.harness
 * 解决：聚合 registry 空表/重复 id 回归
 * 上游：各 sector/registry.ts
 * 下游：CI pnpm check
 * 关联：ENGINEERING.md §6 · check_web_admin_harness.py
 */
import { readdirSync, type Dirent } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { describe, expect, it } from "vitest";
import { API_REGISTRY } from "@/api/registry";
import { isConfigEnabled } from "@/config/registry";
import { ROUTE_REGISTRY } from "@/router/registry";
import { STORE_REGISTRY } from "@/store/registry";

const SRC_ROOT = path.dirname(fileURLToPath(import.meta.url));

function listLayoutModuleIds(): string[] {
  return readdirSync(path.join(SRC_ROOT, "layout/modules"), { withFileTypes: true })
    .filter((entry: Dirent) => entry.isDirectory())
    .map((entry: Dirent) => entry.name);
}

describe("sector registries", () => {
  it("auto-aggregates Studio routes with valid layout ids", () => {
    expect(ROUTE_REGISTRY.length).toBeGreaterThanOrEqual(7);
    const layoutIds = new Set(listLayoutModuleIds());
    for (const route of ROUTE_REGISTRY) {
      expect(layoutIds.has(route.layoutId)).toBe(true);
      expect(route.summary.length).toBeGreaterThanOrEqual(8);
    }
  });

  it("registers studio-shell store and flows API", () => {
    expect(STORE_REGISTRY.some((entry) => entry.moduleId === "studio-shell")).toBe(true);
    expect(API_REGISTRY.some((entry) => entry.id === "studio.flows.list")).toBe(true);
    expect(API_REGISTRY.some((entry) => entry.fn === "postConnectTest")).toBe(true);
  });

  it("exposes config feature flags at runtime", () => {
    expect(isConfigEnabled("studio.wizard")).toBe(true);
  });
});