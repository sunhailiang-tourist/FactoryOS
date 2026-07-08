/**
 * 模块：src/apps/web-admin/src/i18n/core/resources.ts
 * 作用：glob 聚合 modules JSON → i18next resources
 * 怎么用：i18n.ts init 时调用 buildI18nResources()
 * 解决：文案文件分散在 modules 子目录
 * 上游：i18n/modules/·zh-CN.json · en-US.json
 * 下游：i18n/core/i18n.ts
 * 关联：i18n/registry.ts
 */

import type { LocaleId } from "@/i18n/core/types";

    type JsonModule = { default: Record<string, unknown> };

    const zhModules = import.meta.glob<JsonModule>("../modules/*/zh-CN.json", { eager: true });
    const enModules = import.meta.glob<JsonModule>("../modules/*/en-US.json", { eager: true });

    function namespaceFromPath(path: string): string {
      const match = path.match(/modules\/([^/]+)\//);
      return match?.[1] ?? "_platform";
    }

    function collect(localeFiles: Record<string, JsonModule>) {
      const bucket: Record<string, Record<string, unknown>> = {};
      for (const [path, mod] of Object.entries(localeFiles)) {
        bucket[namespaceFromPath(path)] = mod.default;
      }
      return bucket;
    }

/**
 * 功能：buildI18nResources 导出函数。
 * 业务含义：见同文件模块文件头。
 * 上游：见文件头上游。
 * 下游：见文件头下游。
 */
export function buildI18nResources(): Record<LocaleId, Record<string, Record<string, unknown>>> {
      return {
        "zh-CN": collect(zhModules),
        "en-US": collect(enModules),
      };
    }
