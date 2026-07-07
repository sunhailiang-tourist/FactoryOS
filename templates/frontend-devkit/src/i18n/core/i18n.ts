/**
 * 模块：src/apps/web-admin/src/i18n/core/i18n.ts
 * 作用：i18next 单例初始化
 * 怎么用：provider.tsx import ./i18n
 * 解决：应用启动前加载 resources
 * 上游：i18n/core/resources.ts
 * 下游：i18n/core/provider.tsx
 * 关联：i18n/core/types.ts
 */

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
