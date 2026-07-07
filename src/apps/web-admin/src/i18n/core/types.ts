/**
 * 模块：src/apps/web-admin/src/i18n/core/types.ts
 * 作用：LocaleId · 资源形状类型
 * 怎么用：useLocale · resources 引用
 * 解决：首期 zh-CN + en-US 锁死
 * 上游：i18n/contracts/README.md
 * 下游：i18n/core/resources.ts · useLocale.ts
 * 关联：ENGINEERING.md §11 S5
 */

    export const SUPPORTED_LOCALES = ["zh-CN", "en-US"] as const;
    export type LocaleId = (typeof SUPPORTED_LOCALES)[number];
    export const DEFAULT_LOCALE: LocaleId = "zh-CN";
    export const LOCALE_STORAGE_KEY = "fos-locale";
