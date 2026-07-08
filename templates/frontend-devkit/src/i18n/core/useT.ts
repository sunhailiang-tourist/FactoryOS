/**
 * 模块：src/apps/web-admin/src/i18n/core/useT.ts
 * 作用：文案唯一 React 消费入口
 * 怎么用：const { t } = useT('studio-shell')
 * 解决：禁止业务直引 i18next
 * 上游：pages · layout · components
 * 下游：react-i18next useTranslation
 * 关联：eslint no-restricted-imports
 */

import { useTranslation } from "react-i18next";
import type { I18nNamespace } from "@/i18n/registry";

/**
 * 功能：useT 导出函数。
 * 业务含义：见同文件模块文件头。
 * 上游：见文件头上游。
 * 下游：见文件头下游。
 */
export function useT(namespace: I18nNamespace | (string & {})) {
      return useTranslation(namespace);
    }
