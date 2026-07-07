#!/usr/bin/env python3
"""WEB-PROFILE S5 P1：i18n + rbac 体系化落盘 + form codegen 契约占位。"""
from __future__ import annotations

import json
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "src/apps/web-admin"

STUDIO_MODULES = (
  ("studio-shell", "studio.shell.view", "概览", "Overview"),
  ("studio-connect", "studio.connect.view", "连接", "Connect"),
  ("studio-discover", "studio.discover.view", "发现", "Discover"),
  ("studio-map", "studio.map.view", "映射", "Map"),
  ("studio-prove", "studio.prove.view", "验证", "Prove"),
  ("studio-freeze", "studio.freeze.view", "冻结", "Freeze"),
  ("studio-export", "studio.export.view", "导出", "Export"),
)


def w(rel: str, content: str) -> None:
  path = APP / rel
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(textwrap.dedent(content).strip() + "\n", encoding="utf-8")
  print("wrote", path.relative_to(ROOT))


def patch(rel: str, old: str, new: str) -> None:
  path = APP / rel
  text = path.read_text(encoding="utf-8")
  if old not in text:
    if new.strip() in text:
      return
    raise SystemExit(f"patch miss {rel}: {old[:80]!r}")
  path.write_text(text.replace(old, new, 1), encoding="utf-8")
  print("patched", rel)


def patch_root(rel: str, old: str, new: str) -> None:
  path = ROOT / rel
  text = path.read_text(encoding="utf-8")
  if old not in text:
    if new.strip() in text:
      return
    raise SystemExit(f"patch miss {rel}: {old[:80]!r}")
  path.write_text(text.replace(old, new, 1), encoding="utf-8")
  print("patched", rel)


def header(module_path: str, fields: dict[str, str]) -> str:
  labels = ["模块", "作用", "怎么用", "解决", "上游", "下游", "关联"]
  lines = ["/**"]
  for key in labels:
    val = fields.get(key, "TODO").replace("*/", "·").replace("*", "×")
    lines.append(f" * {key}：{val}")
  lines.append(" */")
  return "\n".join(lines) + "\n"


def main() -> int:
  # ── form 工具轨（S7 占位 · 非 codegen 子目录）──
  w(
    "scripts/form/contracts/README.md",
    """
    # form · 板块契约

    ## 是什么

    从 OpenAPI `components.schemas` 生成 **表单 + Zod 校验** 的机器区（`pages/{module-id}/generated/`）。
    列表页生成属同一工具链的扩展项；工具目录为 `scripts/form/`（**不**挂在 `codegen/` 下）。

    ## 登记索引

    | 路径 | 职责 |
    |------|------|
    | `scripts/form/generate.mjs` | CLI：`pnpm form:generate`（S7 实施） |
    | `pages/{id}/generated/*.generated.tsx` | 机器区 · 禁止手改 |
    | `components/crud/CrudForm.tsx` | 手写薄壳复用的表单 primitive（S7） |

    ## 追踪链

    | 项 | 值 |
    |----|-----|
    | 输入 SSOT | `vendor/factoryos-contracts/openapi/` |
    | 输出 | `api/functions` · `api/query/hooks` · `pages/{id}/generated/` |
    | 演示包 | `pages/demo-crud/`（`demo-` 前缀 · 整包可删） |

    ## 变更规则

    1. 生成物变更只跑 `pnpm form:generate` · `pnpm form:check` diff 须为空。
    2. 手写页面只组合 `generated` + `@/components/crud`，不复制字段映射逻辑。
    """,
  )
  w(
    "scripts/form/README.md",
    """
    # form

    OpenAPI schema → RHF + Zod 表单生成（S7 实施）。契约真源：`contracts/README.md`。

    与 `codegen:api`（OpenAPI 类型）分工不同：**本目录只管表单生成**。

    ```bash
    # 计划命令（S7）
    pnpm form:generate -- --module demo-crud --schema AssetCreate
    pnpm form:check
    ```
    """,
  )

  # ── i18n sector ──
  w(
    "src/i18n/contracts/README.md",
    """
    # i18n · 板块契约

    ## 是什么

    国际化 sector：`i18n/registry.ts` glob 聚合 `i18n/modules/{namespace}/` 文案 JSON。

    ## 登记索引

    | namespace | module-id | 说明 |
    |-----------|-----------|------|
    | `_platform` | — | 壳层 · RBAC 提示 · Studio 导航共用文案 |
    | `studio-shell` | studio-shell | 概览页 |
    | `studio-connect` | studio-connect | 连接步 |
    | `studio-discover` | studio-discover | 发现步 |
    | `studio-map` | studio-map | 映射步 |
    | `studio-prove` | studio-prove | 验证步 |
    | `studio-freeze` | studio-freeze | 冻结步 |
    | `studio-export` | studio-export | 导出步 |

    ## 变更规则

    1. 新增 `pages/{module-id}` → 同步 `i18n/modules/{module-id}/zh-CN.json` + `en-US.json` + 本表。
    2. 页面/布局只经 `@/i18n/core/useT` 消费；禁止直引 `i18next` / `react-i18next`（ESLint）。
    3. `pages/{id}/contracts/README.md` 追踪链须含 `i18n namespace` 行。
    """,
  )

  w(
    "src/i18n/registry.ts",
    header(
      "src/apps/web-admin/src/i18n/registry.ts",
      {
        "模块": "src/apps/web-admin/src/i18n/registry.ts",
        "作用": "i18n 板块 glob 登记索引（namespace 列表）",
        "怎么用": "harness 对账；resources.ts 读 modules 子目录",
        "解决": "文案按 namespace 模块化维护",
        "上游": "i18n/modules/*/zh-CN.json · en-US.json",
        "下游": "i18n/core/resources.ts",
        "关联": "i18n/contracts/README.md",
      },
    )
    + """
    /** 平台级 namespace（非 module-id）。 */
    export const I18N_PLATFORM_NAMESPACE = "_platform" as const;

    /** 已登记 namespace（与 modules 子目录名一致）。 */
    export const I18N_NAMESPACES = [
      I18N_PLATFORM_NAMESPACE,
    """
    + "".join(f'  "{mid}",\n' for mid, _, _, _ in STUDIO_MODULES)
    + """] as const;

    export type I18nNamespace = (typeof I18N_NAMESPACES)[number];
    """,
  )

  w(
    "src/i18n/core/types.ts",
    header(
      "src/apps/web-admin/src/i18n/core/types.ts",
      {
        "模块": "src/apps/web-admin/src/i18n/core/types.ts",
        "作用": "LocaleId · 资源形状类型",
        "怎么用": "useLocale · resources 引用",
        "解决": "首期 zh-CN + en-US 锁死",
        "上游": "i18n/contracts/README.md",
        "下游": "i18n/core/resources.ts · useLocale.ts",
        "关联": "ENGINEERING.md §11 S5",
      },
    )
    + """
    export const SUPPORTED_LOCALES = ["zh-CN", "en-US"] as const;
    export type LocaleId = (typeof SUPPORTED_LOCALES)[number];
    export const DEFAULT_LOCALE: LocaleId = "zh-CN";
    export const LOCALE_STORAGE_KEY = "fos-locale";
    """,
  )

  w(
    "src/i18n/core/resources.ts",
    header(
      "src/apps/web-admin/src/i18n/core/resources.ts",
      {
        "模块": "src/apps/web-admin/src/i18n/core/resources.ts",
        "作用": "glob 聚合 modules JSON → i18next resources",
        "怎么用": "i18n.ts init 时调用 buildI18nResources()",
        "解决": "文案文件分散在 modules 子目录",
        "上游": "i18n/modules/*/zh-CN.json · en-US.json",
        "下游": "i18n/core/i18n.ts",
        "关联": "i18n/registry.ts",
      },
    )
    + """
    import type { LocaleId } from "@/i18n/core/types";

    type JsonModule = { default: Record<string, unknown> };

    const zhModules = import.meta.glob<JsonModule>("../modules/*/zh-CN.json", { eager: true });
    const enModules = import.meta.glob<JsonModule>("../modules/*/en-US.json", { eager: true });

    function namespaceFromPath(path: string): string {
      const match = path.match(/modules\\/([^/]+)\\//);
      return match?.[1] ?? "_platform";
    }

    function collect(localeFiles: Record<string, JsonModule>) {
      const bucket: Record<string, Record<string, unknown>> = {};
      for (const [path, mod] of Object.entries(localeFiles)) {
        bucket[namespaceFromPath(path)] = mod.default;
      }
      return bucket;
    }

    export function buildI18nResources(): Record<LocaleId, Record<string, Record<string, unknown>>> {
      return {
        "zh-CN": collect(zhModules),
        "en-US": collect(enModules),
      };
    }
    """,
  )

  w(
    "src/i18n/core/i18n.ts",
    header(
      "src/apps/web-admin/src/i18n/core/i18n.ts",
      {
        "模块": "src/apps/web-admin/src/i18n/core/i18n.ts",
        "作用": "i18next 单例初始化",
        "怎么用": "provider.tsx import ./i18n",
        "解决": "应用启动前加载 resources",
        "上游": "i18n/core/resources.ts",
        "下游": "i18n/core/provider.tsx",
        "关联": "i18n/core/types.ts",
      },
    )
    + """
    import i18n from "i18next";
    import { initReactI18next } from "react-i18next";
    import { buildI18nResources } from "@/i18n/core/resources";
    import { DEFAULT_LOCALE, LOCALE_STORAGE_KEY, type LocaleId } from "@/i18n/core/types";
    import { I18N_PLATFORM_NAMESPACE } from "@/i18n/registry";

    function readStoredLocale(): LocaleId {
      const raw = localStorage.getItem(LOCALE_STORAGE_KEY);
      if (raw === "zh-CN" || raw === "en-US") return raw;
      return DEFAULT_LOCALE;
    }

    void i18n.use(initReactI18next).init({
      resources: buildI18nResources(),
      lng: readStoredLocale(),
      fallbackLng: DEFAULT_LOCALE,
      defaultNS: I18N_PLATFORM_NAMESPACE,
      interpolation: { escapeValue: false },
    });

    export { i18n };
    """,
  )

  w(
    "src/i18n/core/provider.tsx",
    header(
      "src/apps/web-admin/src/i18n/core/provider.tsx",
      {
        "模块": "src/apps/web-admin/src/i18n/core/provider.tsx",
        "作用": "I18nextProvider 包装",
        "怎么用": "bootstrap.tsx 包裹 AppThemeProvider 内层",
        "解决": "全局 locale 上下文",
        "上游": "bootstrap.tsx",
        "下游": "pages · layout · rbac/RbacGuard",
        "关联": "i18n/core/i18n.ts",
      },
    )
    + """
    import type { ReactNode } from "react";
    import { I18nextProvider } from "react-i18next";
    import { i18n } from "@/i18n/core/i18n";

    type I18nProviderProps = { children: ReactNode };

    export function I18nProvider({ children }: I18nProviderProps) {
      return <I18nextProvider i18n={i18n}>{children}</I18nextProvider>;
    }
    """,
  )

  w(
    "src/i18n/core/useT.ts",
    header(
      "src/apps/web-admin/src/i18n/core/useT.ts",
      {
        "模块": "src/apps/web-admin/src/i18n/core/useT.ts",
        "作用": "文案唯一 React 消费入口",
        "怎么用": "const { t } = useT('studio-shell')",
        "解决": "禁止业务直引 i18next",
        "上游": "pages · layout · components",
        "下游": "react-i18next useTranslation",
        "关联": "eslint no-restricted-imports",
      },
    )
    + """
    import { useTranslation } from "react-i18next";
    import type { I18nNamespace } from "@/i18n/registry";

    export function useT(namespace: I18nNamespace | (string & {})) {
      return useTranslation(namespace);
    }
    """,
  )

  w(
    "src/i18n/core/useLocale.ts",
    header(
      "src/apps/web-admin/src/i18n/core/useLocale.ts",
      {
        "模块": "src/apps/web-admin/src/i18n/core/useLocale.ts",
        "作用": "切换 zh-CN / en-US",
        "怎么用": "设置页或调试工具调用 setLocale",
        "解决": "locale 持久化 localStorage",
        "上游": "i18n/core/i18n.ts",
        "下游": "未来设置页",
        "关联": "i18n/core/types.ts",
      },
    )
    + """
    import { useCallback } from "react";
    import { useTranslation } from "react-i18next";
    import { LOCALE_STORAGE_KEY, type LocaleId } from "@/i18n/core/types";

    export function useLocale() {
      const { i18n } = useTranslation();
      const locale = (i18n.language === "en-US" ? "en-US" : "zh-CN") as LocaleId;
      const setLocale = useCallback(
        (next: LocaleId) => {
          void i18n.changeLanguage(next);
          localStorage.setItem(LOCALE_STORAGE_KEY, next);
        },
        [i18n],
      );
      return { locale, setLocale };
    }
    """,
  )

  w(
    "src/i18n/core/useT.test.ts",
    header(
      "src/apps/web-admin/src/i18n/core/useT.test.ts",
      {
        "模块": "src/apps/web-admin/src/i18n/core/useT.test.ts",
        "作用": "i18n 资源 smoke",
        "怎么用": "vitest",
        "解决": "zh/en 平台文案可解析",
        "上游": "i18n/core/resources.ts",
        "下游": "vitest",
        "关联": "WEB-PROFILE S5",
      },
    )
    + """
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
    """,
  )

  w(
    "src/i18n/modules/_platform/zh-CN.json",
    json.dumps(
      {
        "appTitle": "FactoryOS · Integration Studio",
        "studioTitle": "Integration Studio",
        "studioSubtitle": "新客户接入 · 六步向导（零仓库主路径）",
        "studioNavAria": "Studio 六步",
        "studioNavOverview": "概览",
        "openNav": "打开导航",
        "rbacDenied": "Studio 访问被拒绝（角色：{{role}}）",
        "rbacRouteDenied": "无权访问该页面（缺少权限：{{permissions}}）",
      },
      ensure_ascii=False,
      indent=2,
    )
    + "\n",
  )
  w(
    "src/i18n/modules/_platform/en-US.json",
    json.dumps(
      {
        "appTitle": "FactoryOS · Integration Studio",
        "studioTitle": "Integration Studio",
        "studioSubtitle": "New customer onboarding · six-step wizard",
        "studioNavAria": "Studio steps",
        "studioNavOverview": "Overview",
        "openNav": "Open navigation",
        "rbacDenied": "Studio access denied (role: {{role}})",
        "rbacRouteDenied": "You cannot open this page (missing: {{permissions}})",
      },
      ensure_ascii=False,
      indent=2,
    )
    + "\n",
  )

  for module_id, perm, _zh, _en in STUDIO_MODULES:
    key = module_id.removeprefix("studio-").replace("-", "")
    w(
      f"src/i18n/modules/{module_id}/zh-CN.json",
      json.dumps({"title": _zh, "summary": f"{_zh}步骤"}, ensure_ascii=False, indent=2) + "\n",
    )
    w(
      f"src/i18n/modules/{module_id}/en-US.json",
      json.dumps({"title": _en, "summary": f"{_en} step"}, ensure_ascii=False, indent=2) + "\n",
    )

  # ── rbac sector ──
  perm_lines = "\n".join(
    f'  "{mid}": "{perm}",' for mid, perm, _, _ in STUDIO_MODULES
  )
  role_perm_list = ",\n    ".join(f'"{p}"' for _, p, _, _ in STUDIO_MODULES)

  w(
    "src/rbac/contracts/README.md",
    """
    # rbac · 板块契约

    ## 是什么

    权限 sector：`rbac/modules/{domain}/registry.ts` 定义角色→权限；路由 `permissions` 字段消费。

    ## 登记索引

    | domain | 说明 |
    |--------|------|
    | `studio` | Integration Studio 七步 + 壳 |

    ## 追踪链（全链路）

    ```text
    getActorContext().role          # api/request/interceptors
            ↓
    rbac/modules/studio/registry.ts # ROLE_PERMISSIONS · MODULE_PERMISSIONS
            ↓
    rbac/core/evaluate.ts           # can() · canAccessRoute() · canAccessDomain()
            ↓
    router/modules/{id}/registry.ts # permissions: ['studio.xxx.view']
            ↓
    router/registry.ts              # getRoutesByLayout(..., role) 过滤
            ↓
    layout StudioShellSidebar       # 侧栏按 can() 隐藏
    rbac/core/RbacGuard.tsx         # 域级 / 路由级 UI 拦截
            ↓
    rbac/core/usePermissions.ts     # 按钮级预留（二期 can('studio.connect.write')）
    ```

    ## 变更规则

    1. 新增路由须声明 `permissions` 并登记 `MODULE_PERMISSIONS`。
    2. `pages/{id}/contracts/README.md` 追踪链须含 `rbac permission` 行。
    3. 服务端 403 仍为最终权威；前端 RBAC 仅 UX。
    """,
  )

  w(
    "src/rbac/core/types.ts",
    header(
      "src/apps/web-admin/src/rbac/core/types.ts",
      {
        "模块": "src/apps/web-admin/src/rbac/core/types.ts",
        "作用": "Permission · Role · 评估模式类型",
        "怎么用": "evaluate · router/types 引用",
        "解决": "权限字符串 SSOT 形状",
        "上游": "rbac/modules/*/registry.ts",
        "下游": "rbac/core/evaluate.ts",
        "关联": "rbac/contracts/README.md",
      },
    )
    + """
    export type Permission = string;
    export type Role = string;
    export type PermissionMode = "all" | "any";
    """,
  )

  w(
    "src/rbac/modules/studio/registry.ts",
    header(
      "src/apps/web-admin/src/rbac/modules/studio/registry.ts",
      {
        "模块": "src/apps/web-admin/src/rbac/modules/studio/registry.ts",
        "作用": "Studio 域权限子表",
        "怎么用": "registry.ts glob 聚合；evaluate 读取",
        "解决": "module-id ↔ permission 模块化维护",
        "上游": "Integration-Studio规格 · AC-STU-09",
        "下游": "rbac/core/evaluate.ts · router permissions",
        "关联": "rbac/contracts/README.md",
      },
    )
    + f"""
    import type {{ Permission, Role }} from "@/rbac/core/types";

    export const RBAC_DOMAIN = "studio" as const;

    /** module-id → 路由级 view 权限（与 router registry permissions 一致）。 */
    export const MODULE_PERMISSIONS: Record<string, Permission> = {{
    {perm_lines}
    }};

    const ALL_STUDIO_VIEW: Permission[] = [
      {role_perm_list},
    ];

    const STUDIO_VIEW_ROLES: Role[] = [
      "integrator",
      "admin",
      "platform",
      "business_owner",
      "customer_it",
    ];

    /** 角色 → 权限列表（首期路由级 view）。 */
    export const ROLE_PERMISSIONS: Record<Role, readonly Permission[]> = {{
      integrator: ALL_STUDIO_VIEW,
      admin: ALL_STUDIO_VIEW,
      platform: ALL_STUDIO_VIEW,
      business_owner: ALL_STUDIO_VIEW,
      customer_it: ALL_STUDIO_VIEW,
      operator: [],
    }};

    export function studioRolesWithAccess(): Role[] {{
      return STUDIO_VIEW_ROLES;
    }}
    """,
  )

  w(
    "src/rbac/registry.ts",
    header(
      "src/apps/web-admin/src/rbac/registry.ts",
      {
        "模块": "src/apps/web-admin/src/rbac/registry.ts",
        "作用": "rbac 板块 glob 聚合域子表",
        "怎么用": "evaluate.ts import；harness 对账",
        "解决": "多域权限可扩展",
        "上游": "rbac/modules/studio/registry.ts",
        "下游": "rbac/core/evaluate.ts",
        "关联": "rbac/contracts/README.md",
      },
    )
    + """
    import {
      MODULE_PERMISSIONS as STUDIO_MODULE_PERMISSIONS,
      RBAC_DOMAIN as STUDIO_DOMAIN,
      ROLE_PERMISSIONS as STUDIO_ROLE_PERMISSIONS,
    } from "@/rbac/modules/studio/registry";

    export const RBAC_DOMAINS = [STUDIO_DOMAIN] as const;

    /** 合并各域 module-id → permission（首期仅 studio）。 */
    export const MODULE_PERMISSIONS: Record<string, string> = {
      ...STUDIO_MODULE_PERMISSIONS,
    };

    /** 合并各域 role → permissions（首期仅 studio）。 */
    export function getRolePermissions(role: string): readonly string[] {
      return STUDIO_ROLE_PERMISSIONS[role] ?? [];
    }
    """,
  )

  w(
    "src/rbac/core/evaluate.ts",
    header(
      "src/apps/web-admin/src/rbac/core/evaluate.ts",
      {
        "模块": "src/apps/web-admin/src/rbac/core/evaluate.ts",
        "作用": "纯函数权限评估",
        "怎么用": "registry · RbacGuard · usePermissions 调用",
        "解决": "可单测、无 React 依赖",
        "上游": "rbac/registry.ts",
        "下游": "rbac/core/RbacGuard.tsx · usePermissions.ts",
        "关联": "rbac/core/evaluate.test.ts",
      },
    )
    + """
    import { getRolePermissions, MODULE_PERMISSIONS } from "@/rbac/registry";
    import type { Permission, PermissionMode, Role } from "@/rbac/core/types";

    export function permissionsForModule(moduleId: string): Permission[] {
      const perm = MODULE_PERMISSIONS[moduleId];
      return perm ? [perm] : [];
    }

    export function can(role: Role, permission: Permission): boolean {
      const grants = getRolePermissions(role);
      return grants.includes(permission);
    }

    export function canAny(role: Role, permissions: readonly Permission[]): boolean {
      return permissions.some((p) => can(role, p));
    }

    export function canAll(role: Role, permissions: readonly Permission[]): boolean {
      return permissions.length > 0 && permissions.every((p) => can(role, p));
    }

    export function canAccessPermissions(
      role: Role,
      permissions: readonly Permission[],
      mode: PermissionMode = "all",
    ): boolean {
      if (permissions.length === 0) return true;
      return mode === "any" ? canAny(role, permissions) : canAll(role, permissions);
    }

    export function canAccessRoute(
      role: Role,
      permissions: readonly Permission[] | undefined,
      mode: PermissionMode = "all",
    ): boolean {
      return canAccessPermissions(role, permissions ?? [], mode);
    }

    export function canAccessDomain(role: Role, domain: string): boolean {
      const prefix = `${domain}.`;
      const grants = getRolePermissions(role);
      return grants.some((p) => p.startsWith(prefix));
    }
    """,
  )

  w(
    "src/rbac/core/evaluate.test.ts",
    header(
      "src/apps/web-admin/src/rbac/core/evaluate.test.ts",
      {
        "模块": "src/apps/web-admin/src/rbac/core/evaluate.test.ts",
        "作用": "RBAC 纯函数单测",
        "怎么用": "vitest",
        "解决": "角色/路由权限可回归",
        "上游": "rbac/core/evaluate.ts",
        "下游": "vitest",
        "关联": "WEB-PROFILE S5",
      },
    )
    + """
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
    """,
  )

  w(
    "src/rbac/core/usePermissions.ts",
    header(
      "src/apps/web-admin/src/rbac/core/usePermissions.ts",
      {
        "模块": "src/apps/web-admin/src/rbac/core/usePermissions.ts",
        "作用": "按钮级权限 Hook（二期扩展位）",
        "怎么用": "const { can } = usePermissions(); can('studio.connect.write')",
        "解决": "路由级外复用同一 evaluate",
        "上游": "getActorContext · rbac/core/evaluate.ts",
        "下游": "pages 按钮 · 工具栏（二期）",
        "关联": "rbac/contracts/README.md",
      },
    )
    + """
    import { getActorContext } from "@/api/request";
    import {
      can as canPermission,
      canAccessPermissions,
      canAny,
      canAll,
    } from "@/rbac/core/evaluate";
    import type { Permission, PermissionMode } from "@/rbac/core/types";

    /** 首期薄封装；二期在页面按钮直接消费，无需改目录。 */
    export function usePermissions() {
      const role = getActorContext().role;
      return {
        role,
        can: (permission: Permission) => canPermission(role, permission),
        canAny: (permissions: readonly Permission[]) => canAny(role, permissions),
        canAll: (permissions: readonly Permission[]) => canAll(role, permissions),
        canAccess: (permissions: readonly Permission[], mode: PermissionMode = "all") =>
          canAccessPermissions(role, permissions, mode),
      };
    }
    """,
  )

  w(
    "src/rbac/core/RbacGuard.tsx",
    header(
      "src/apps/web-admin/src/rbac/core/RbacGuard.tsx",
      {
        "模块": "src/apps/web-admin/src/rbac/core/RbacGuard.tsx",
        "作用": "域级 / 路由级 RBAC UI 守卫",
        "怎么用": "layout 包 domain；路由包 permissions",
        "解决": "替代 studio-rbac.guard 硬编码",
        "上游": "getActorContext · rbac/core/evaluate.ts",
        "下游": "StudioShellLayout · 未来路由 wrapper",
        "关联": "i18n _platform rbacDenied",
      },
    )
    + """
    import Alert from "@mui/material/Alert";
    import type { ReactNode } from "react";
    import { getActorContext } from "@/api/request";
    import { useT } from "@/i18n/core/useT";
    import { I18N_PLATFORM_NAMESPACE } from "@/i18n/registry";
    import { canAccessDomain, canAccessRoute } from "@/rbac/core/evaluate";
    import type { Permission, PermissionMode } from "@/rbac/core/types";

    type RbacGuardProps = {
      children: ReactNode;
      /** 域级：如 studio → 须拥有任一 studio.* 权限 */
      domain?: string;
      /** 路由级：显式权限列表 */
      permissions?: readonly Permission[];
      permissionsMode?: PermissionMode;
      role?: string;
    };

    export function RbacGuard({
      children,
      domain,
      permissions,
      permissionsMode = "all",
      role: roleProp,
    }: RbacGuardProps) {
      const { t } = useT(I18N_PLATFORM_NAMESPACE);
      const role = roleProp ?? getActorContext().role;

      if (domain && !canAccessDomain(role, domain)) {
        return (
          <Alert severity="error" role="alert">
            {t("rbacDenied", { role })}
          </Alert>
        );
      }

      if (permissions && !canAccessRoute(role, permissions, permissionsMode)) {
        return (
          <Alert severity="error" role="alert">
            {t("rbacRouteDenied", { permissions: permissions.join(", ") })}
          </Alert>
        );
      }

      return <>{children}</>;
    }
    """,
  )

  # ── patches ──
  patch(
    "src/router/types.ts",
    """export type RouteModuleEntry = {
  name: string;
  moduleId: string;
  layoutId: string;
  summary: string;
  path?: string;
  index?: boolean;
  lazy: () => Promise<{ Component: ComponentType }>;
};""",
    """export type RouteModuleEntry = {
  name: string;
  moduleId: string;
  layoutId: string;
  summary: string;
  path?: string;
  index?: boolean;
  /** 路由级 view 权限（rbac/modules 登记须一致）。 */
  permissions?: readonly string[];
  permissionsMode?: "all" | "any";
  lazy: () => Promise<{ Component: ComponentType }>;
};""",
  )

  for module_id, perm, _, _ in STUDIO_MODULES:
    patch(
      f"src/router/modules/{module_id}/registry.ts",
      '    summary: "',
      f'    permissions: ["{perm}"],\n    summary: "',
    )

  patch(
    "src/router/registry.ts",
    'import type { RouteModuleEntry } from "@/router/types";',
    'import type { RouteModuleEntry } from "@/router/types";\nimport { canAccessRoute } from "@/rbac/core/evaluate";',
  )
  patch(
    "src/router/registry.ts",
    """export function getRoutesByLayout(layoutId: string): RouteModuleEntry[] {
  return ROUTE_REGISTRY.filter((entry) => entry.layoutId === layoutId);
}""",
    """export function getRoutesByLayout(layoutId: string, role?: string): RouteModuleEntry[] {
  const routes = ROUTE_REGISTRY.filter((entry) => entry.layoutId === layoutId);
  if (!role) return routes;
  return routes.filter((entry) => canAccessRoute(role, entry.permissions, entry.permissionsMode));
}""",
  )

  patch(
    "src/router/browser-router.tsx",
    'import { getRoutesByLayout } from "@/router/registry";',
    'import { getActorContext } from "@/api/request";\nimport { getRoutesByLayout } from "@/router/registry";',
  )
  patch(
    "src/router/browser-router.tsx",
    "export function createAppRouter(queryClient: QueryClient) {\n  const studioFlowsLoader = createStudioFlowsLoader(queryClient);",
    "export function createAppRouter(queryClient: QueryClient) {\n  const actorRole = getActorContext().role;\n  const studioFlowsLoader = createStudioFlowsLoader(queryClient);",
  )
  patch(
    "src/router/browser-router.tsx",
    "          const routes = getRoutesByLayout(layout.id);",
    "          const routes = getRoutesByLayout(layout.id, actorRole);",
  )

  patch(
    "src/bootstrap.tsx",
    'import { createAppRouter } from "@/router/browser-router";',
    'import { I18nProvider } from "@/i18n/core/provider";\nimport { createAppRouter } from "@/router/browser-router";',
  )
  patch(
    "src/bootstrap.tsx",
    """    <QueryClientProvider client={queryClient}>
      <AppThemeProvider>
        <Suspense fallback={<PageLoading />}>
          <RouterProvider router={router} />
        </Suspense>
      </AppThemeProvider>
    </QueryClientProvider>""",
    """    <QueryClientProvider client={queryClient}>
      <I18nProvider>
        <AppThemeProvider>
          <Suspense fallback={<PageLoading />}>
            <RouterProvider router={router} />
          </Suspense>
        </AppThemeProvider>
      </I18nProvider>
    </QueryClientProvider>""",
  )

  patch(
    "src/layout/modules/studio/StudioShellLayout.tsx",
    ' * 下游：pages studio 系列 · router/guards/studio-rbac.guard',
    " * 下游：pages studio 系列 · rbac/core/RbacGuard",
  )
  patch(
    "src/layout/modules/studio/StudioShellLayout.tsx",
    'import { StudioRbacGuard } from "@/router/guards/studio-rbac.guard";',
    'import { useT } from "@/i18n/core/useT";\nimport { I18N_PLATFORM_NAMESPACE } from "@/i18n/registry";\nimport { RbacGuard } from "@/rbac/core/RbacGuard";\nimport { RBAC_DOMAIN } from "@/rbac/modules/studio/registry";',
  )
  patch(
    "src/layout/modules/studio/StudioShellLayout.tsx",
    '  const actorRole = getActorContext().role;',
    '  const actorRole = getActorContext().role;\n  const { t } = useT(I18N_PLATFORM_NAMESPACE);',
  )
  patch(
    "src/layout/modules/studio/StudioShellLayout.tsx",
    '              <IconButton edge="start" onClick={() => setMobileOpen(true)} aria-label="打开导航">',
    '              <IconButton edge="start" onClick={() => setMobileOpen(true)} aria-label={t("openNav")}>',
  )
  patch(
    "src/layout/modules/studio/StudioShellLayout.tsx",
    '                Integration Studio',
    '                {t("studioTitle")}',
  )
  patch(
    "src/layout/modules/studio/StudioShellLayout.tsx",
    "    <StudioRbacGuard role={actorRole}>",
    '    <RbacGuard domain={RBAC_DOMAIN} role={actorRole}>',
  )
  patch(
    "src/layout/modules/studio/StudioShellLayout.tsx",
    "    </StudioRbacGuard>",
    "    </RbacGuard>",
  )
  patch(
    "src/layout/modules/studio/StudioShellLayout.tsx",
    '          {env.appTitle}',
    '          {t("appTitle")}',
  )

  patch(
    "src/layout/modules/studio/StudioShellSidebar.tsx",
    'import { StudioNavLink } from "@/router/StudioNavLink";',
    'import { useT } from "@/i18n/core/useT";\nimport { I18N_PLATFORM_NAMESPACE } from "@/i18n/registry";\nimport { can } from "@/rbac/core/evaluate";\nimport { permissionsForModule } from "@/rbac/core/evaluate";\nimport { getActorContext } from "@/api/request";\nimport { StudioNavLink } from "@/router/StudioNavLink";',
  )
  patch(
    "src/layout/modules/studio/StudioShellSidebar.tsx",
    "export function StudioShellSidebar() {\n  const location = useLocation();",
    "export function StudioShellSidebar() {\n  const location = useLocation();\n  const { t } = useT(I18N_PLATFORM_NAMESPACE);\n  const role = getActorContext().role;",
  )
  patch(
    "src/layout/modules/studio/StudioShellSidebar.tsx",
    '        {data.title ?? "Integration Studio"}',
    '        {data.title ?? t("studioTitle")}',
  )
  patch(
    "src/layout/modules/studio/StudioShellSidebar.tsx",
    '        新客户接入 · 六步向导（零仓库主路径）',
    '        {t("studioSubtitle")}',
  )
  patch(
    "src/layout/modules/studio/StudioShellSidebar.tsx",
    '      <List component="nav" aria-label="Studio 六步">',
    '      <List component="nav" aria-label={t("studioNavAria")}>',
  )
  patch(
    "src/layout/modules/studio/StudioShellSidebar.tsx",
    """        <StudioNavLink
          to="/studio"
          selected={location.pathname === "/studio"}
          primary="概览"
          secondary="studio.home"
          moduleId="studio-shell"
        />""",
    """        {can(role, "studio.shell.view") ? (
          <StudioNavLink
            to="/studio"
            selected={location.pathname === "/studio"}
            primary={t("studioNavOverview")}
            secondary="studio.home"
            moduleId="studio-shell"
          />
        ) : null}""",
  )
  patch(
    "src/layout/modules/studio/StudioShellSidebar.tsx",
    """        {steps.map((step) => {
          const to = stepHref(step.id, step.path);
          return (
            <StudioNavLink
              key={step.id}
              to={to}
              selected={location.pathname === to}
              primary={`${step.order}. ${step.title}`}
              secondary={step.summary}
              moduleId={STEP_MODULE_IDS[step.id]}
              endAdornment={<ChevronRightIcon fontSize="small" />}
            />
          );
        })}""",
    """        {steps.map((step) => {
          const moduleId = STEP_MODULE_IDS[step.id];
          const perms = permissionsForModule(moduleId);
          if (perms.length && !can(role, perms[0])) return null;
          const to = stepHref(step.id, step.path);
          return (
            <StudioNavLink
              key={step.id}
              to={to}
              selected={location.pathname === to}
              primary={`${step.order}. ${step.title}`}
              secondary={step.summary}
              moduleId={moduleId}
              endAdornment={<ChevronRightIcon fontSize="small" />}
            />
          );
        })}""",
  )

  patch(
    "src/layout/modules/studio/StudioShellLayout.tsx",
    'import { env } from "@/config/env";\n',
    "",
  )

  patch(
    "src/test/render.tsx",
    'import { createQueryClient } from "@/api/query/client";',
    'import { createQueryClient } from "@/api/query/client";\nimport "@/i18n/core/i18n";\nimport { I18nProvider } from "@/i18n/core/provider";',
  )
  patch(
    "src/test/render.tsx",
    """      <QueryClientProvider client={queryClient}>
        <MemoryRouter initialEntries={[route]}>{children}</MemoryRouter>
      </QueryClientProvider>""",
    """      <QueryClientProvider client={queryClient}>
        <I18nProvider>
          <MemoryRouter initialEntries={[route]}>{children}</MemoryRouter>
        </I18nProvider>
      </QueryClientProvider>""",
  )

  patch_root(
    "scripts/devkit/frontend_contract_lib.py",
    'SKIP_INDEX_IDS = frozenset({"module-id", "domain-id", "config-id", "domain", "项"})',
    'SKIP_INDEX_IDS = frozenset({"module-id", "domain-id", "config-id", "domain", "namespace", "项"})',
  )

  import shutil
  shutil.copy2(
    ROOT / "scripts/devkit/frontend_contract_lib.py",
    APP / "scripts/devkit/frontend_contract_lib.py",
  )
  print("synced scripts/devkit/frontend_contract_lib.py → web-admin")

  import shutil
  shutil.copy2(
    ROOT / "scripts/devkit/frontend_contract_lib.py",
    APP / "scripts/devkit/frontend_contract_lib.py",
  )
  print("synced frontend_contract_lib.py → web-admin")

  guard_path = APP / "src/router/guards/studio-rbac.guard.tsx"
  if guard_path.is_file():
    guard_path.unlink()
    print("removed", guard_path.relative_to(ROOT))

  patch(
    "scripts/check_harness.py",
    """SECTOR_REGISTRY_DIRS: tuple[tuple[str, str, str], ...] = (
  ("router", "modules", "module-id"),
  ("store", "modules", "module-id"),
  ("layout", "modules", "domain-id"),
  ("config", "modules", "config-id"),
  ("api", "functions", "module-id"),
)""",
    """SECTOR_REGISTRY_DIRS: tuple[tuple[str, str, str], ...] = (
  ("router", "modules", "module-id"),
  ("store", "modules", "module-id"),
  ("layout", "modules", "domain-id"),
  ("config", "modules", "config-id"),
  ("api", "functions", "module-id"),
  ("i18n", "modules", "namespace"),
  ("rbac", "modules", "domain"),
)""",
  )
  patch(
    "scripts/check_harness.py",
    """    checks: tuple[tuple[str, str, str], ...] = (
      ("module-id", str(route.get("moduleId") or module_id), module_id),
      ("route name", str(route.get("name") or ""), ""),
      ("path", expected_path, ""),
      ("layout", str(route.get("layoutId") or ""), ""),
    )""",
    """    checks: tuple[tuple[str, str, str], ...] = (
      ("module-id", str(route.get("moduleId") or module_id), module_id),
      ("route name", str(route.get("name") or ""), ""),
      ("path", expected_path, ""),
      ("layout", str(route.get("layoutId") or ""), ""),
      ("i18n namespace", module_id, module_id),
      ("rbac permission", str(route.get("permission") or ""), ""),
    )""",
  )
  patch(
    "scripts/check_harness.py",
    """      elif actual != expected:
        errors.append(
          f"pages/{module_id}/contracts/README.md {key} mismatch: "
          f"doc={actual!r} registry={expected!r}"
        )

    store_reg = store_modules / module_id / "registry.ts"
""",
    """      elif actual != expected:
        errors.append(
          f"pages/{module_id}/contracts/README.md {key} mismatch: "
          f"doc={actual!r} registry={expected!r}"
        )

    perm = str(route.get("permission") or "")
    if not perm:
      errors.append(f"router/modules/{module_id}/registry.ts missing permissions")

    store_reg = store_modules / module_id / "registry.ts"
""",
  )
  patch(
    "scripts/check_harness.py",
    """def _validate_codegen_fresh(errors: list[str]) -> None:
  \"\"\"OpenAPI → generated 同步（W-01）。\"\"\"
""",
    """def _validate_i18n_modules(errors: list[str], module_ids: set[str]) -> None:
  \"\"\"每个 pages module-id 须有 i18n/modules/{id}/ 双语文案。\"\"\"
  i18n_modules = SRC / "i18n" / "modules"
  if not i18n_modules.is_dir():
    errors.append("missing src/i18n/modules/")
    return
  if not (SRC / "i18n" / "modules" / "_platform" / "zh-CN.json").is_file():
    errors.append("missing i18n/modules/_platform/zh-CN.json")
  for module_id in sorted(module_ids):
    zh = i18n_modules / module_id / "zh-CN.json"
    en = i18n_modules / module_id / "en-US.json"
    if not zh.is_file():
      errors.append(f"missing i18n/modules/{module_id}/zh-CN.json")
    if not en.is_file():
      errors.append(f"missing i18n/modules/{module_id}/en-US.json")


def _validate_rbac_studio(errors: list[str], module_ids: set[str]) -> None:
  \"\"\"rbac MODULE_PERMISSIONS 与 router module-id 一致。\"\"\"
  reg = SRC / "rbac" / "modules" / "studio" / "registry.ts"
  if not reg.is_file():
    errors.append("missing rbac/modules/studio/registry.ts")
    return
  text = reg.read_text(encoding="utf-8")
  for module_id in sorted(module_ids):
    if f'"{module_id}"' not in text:
      errors.append(f"rbac/modules/studio/registry.ts missing module-id {module_id!r}")


def _validate_codegen_fresh(errors: list[str]) -> None:
  \"\"\"OpenAPI → generated 同步（W-01）。\"\"\"
""",
  )
  patch(
    "scripts/check_harness.py",
    """  _validate_module_contracts(errors, module_ids, pages_dir, router_modules, layout_prefixes)
  _validate_sector_contracts(errors)
""",
    """  _validate_module_contracts(errors, module_ids, pages_dir, router_modules, layout_prefixes)
  _validate_i18n_modules(errors, module_ids)
  _validate_rbac_studio(errors, module_ids)
  _validate_sector_contracts(errors)
""",
  )

  # pages contracts tracking rows
  for module_id, perm, _, _ in STUDIO_MODULES:
    contract = APP / "src/pages" / module_id / "contracts" / "README.md"
    if not contract.is_file():
      continue
    text = contract.read_text(encoding="utf-8")
    if "i18n namespace" in text:
      continue
    if "| layout |" in text:
      text = text.replace(
        "| layout |",
        f"| i18n namespace | `{module_id}` |\n| rbac permission | `{perm}` |\n| layout |",
        1,
      )
      contract.write_text(text, encoding="utf-8")
      print("patched", contract.relative_to(ROOT))

  # package.json deps
  pkg_path = APP / "package.json"
  pkg = json.loads(pkg_path.read_text(encoding="utf-8"))
  deps = pkg.setdefault("dependencies", {})
  deps.setdefault("i18next", "^24.2.3")
  deps.setdefault("react-i18next", "^15.4.1")
  pkg_path.write_text(json.dumps(pkg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
  print("patched package.json")

  patch(
    "eslint.config.js",
    """            {
              name: "@tanstack/react-query",
              message: "pages 禁止直引 react-query；使用 @/api/query/hooks",
            },
          ],""",
    """            {
              name: "@tanstack/react-query",
              message: "pages 禁止直引 react-query；使用 @/api/query/hooks",
            },
            {
              name: "i18next",
              message: "禁止直引 i18next；使用 @/i18n/core/useT",
            },
            {
              name: "react-i18next",
              message: "禁止直引 react-i18next；使用 @/i18n/core/useT",
            },
          ],""",
  )

  patch(
    "devkit.profile.yaml",
    "  - perf_first_paint_shell",
    """  - perf_first_paint_shell
  - i18n_registry_sync
  - rbac_route_permissions""",
  )

  patch_root(
    "contracts/directory-readmes.yaml",
    "  - src/apps/web-admin/src/router\n  - src/apps/web-admin/src/store",
    "  - src/apps/web-admin/src/router\n  - src/apps/web-admin/src/i18n\n  - src/apps/web-admin/src/rbac\n  - src/apps/web-admin/src/store",
  )

  patch(
    "ENGINEERING.md",
    "目标（PC）：LCP P75 < 1.5s · 步间导航感知 < 200ms · CLS < 0.05。",
    """目标（PC）：LCP P75 < 1.5s · 步间导航感知 < 200ms · CLS < 0.05。

## 11. i18n + RBAC（S5 · 锁死）

| sector | 路径 | 消费入口 |
|--------|------|----------|
| i18n | `i18n/modules/{module-id}/` | `useT(namespace)` · 禁止直引 i18next |
| rbac | `rbac/modules/{domain}/` | 路由 `permissions` · `RbacGuard` · `usePermissions`（按钮级预留） |

追踪链：`pages/{id}/contracts` 须含 `i18n namespace` · `rbac permission`。

form 生成（S7）：`scripts/form/` · 契约 `scripts/form/contracts/README.md`。""",
  )

  patch(
    "src/README.md",
    "| `router/` | module-id 路由 registry |",
    "| `i18n/` | 文案 namespace registry（zh-CN · en-US） |\n| `rbac/` | 权限 domain registry |\n| `router/` | module-id 路由 registry |",
  )

  w(
    "src/i18n/README.md",
    """
    # i18n

    ## 是什么

    国际化 sector：按 `module-id` namespace 维护 `zh-CN.json` / `en-US.json`。

    ## 子路径

    | 路径 | 职责 |
    |------|------|
    | `contracts/` | 登记索引与变更规则 |
    | `core/` | Provider · useT · useLocale |
    | `modules/` | 各 namespace 文案 JSON |

    ## 门禁

    - `scripts/check_harness.py` · `i18n_registry_sync`
    - ESLint：业务代码禁止直引 `i18next`

    ## 变更纪律

    新增 module-id 须同步 `modules/{id}/` 双语文案与 `contracts/README.md` 登记索引。

    ## 相关文档

    - [ENGINEERING.md §11](../ENGINEERING.md)
    - [ARCHITECTURE.md](../ARCHITECTURE.md)
    """,
  )

  w(
    "src/rbac/README.md",
    """
    # rbac

    ## 是什么

    权限 sector：角色→权限表 + 路由 `permissions` 全链路对账。

    ## 子路径

    | 路径 | 职责 |
    |------|------|
    | `contracts/` | 追踪链说明 |
    | `core/` | evaluate · RbacGuard · usePermissions |
    | `modules/` | 各 domain 权限子表 |

    ## 门禁

    - `scripts/check_harness.py` · `rbac_route_permissions`
    - 路由 registry 须声明 `permissions`

    ## 变更纪律

    改 `rbac/modules/{domain}/registry.ts` 须同步 router permissions 与 pages contracts。

    ## 相关文档

    - [rbac/contracts/README.md](./contracts/README.md)
    - [ENGINEERING.md §11](../ENGINEERING.md)
    """,
  )

  print("OK: S5 P1 install")
  return 0


if __name__ == "__main__":
  raise SystemExit(main())
