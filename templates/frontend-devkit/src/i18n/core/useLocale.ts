/**
 * 模块：src/apps/web-admin/src/i18n/core/useLocale.ts
 * 作用：切换 zh-CN / en-US
 * 怎么用：设置页或调试工具调用 setLocale
 * 解决：locale 持久化 localStorage
 * 上游：i18n/core/i18n.ts
 * 下游：未来设置页
 * 关联：i18n/core/types.ts
 */

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
