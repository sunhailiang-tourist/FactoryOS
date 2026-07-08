/**
 * 模块：src/apps/web-admin/src/i18n/core/provider.tsx
 * 作用：I18nextProvider 包装
 * 怎么用：bootstrap.tsx 包裹 AppThemeProvider 内层
 * 解决：全局 locale 上下文
 * 上游：bootstrap.tsx
 * 下游：pages · layout · rbac/RbacGuard
 * 关联：i18n/core/i18n.ts
 */

import type { ReactNode } from "react";
import { I18nextProvider } from "react-i18next";
import { i18n } from "@/i18n/core/i18n";

    type I18nProviderProps = { children: ReactNode };

/**
 * 功能：I18nProvider 导出函数。
 * 业务含义：见同文件模块文件头。
 * 上游：见文件头上游。
 * 下游：见文件头下游。
 */
export function I18nProvider({ children }: I18nProviderProps) {
      return <I18nextProvider i18n={i18n}>{children}</I18nextProvider>;
    }
