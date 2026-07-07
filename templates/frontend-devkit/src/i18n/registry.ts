/**
 * 模块：src/apps/web-admin/src/i18n/registry.ts
 * 作用：i18n 板块 glob 登记索引（namespace 列表）
 * 怎么用：harness 对账；resources.ts 读 modules 子目录
 * 解决：文案按 namespace 模块化维护
 * 上游：i18n/modules/·zh-CN.json · en-US.json
 * 下游：i18n/core/resources.ts
 * 关联：i18n/contracts/README.md
 */

    /** 平台级 namespace（非 module-id）。 */
    export const I18N_PLATFORM_NAMESPACE = "_platform" as const;

    /** 已登记 namespace（与 modules 子目录名一致）。 */
    export const I18N_NAMESPACES = [
      I18N_PLATFORM_NAMESPACE,
      "studio-shell",
  "studio-connect",
  "studio-discover",
  "studio-map",
  "studio-prove",
  "studio-freeze",
  "studio-export",
] as const;

    export type I18nNamespace = (typeof I18N_NAMESPACES)[number];
