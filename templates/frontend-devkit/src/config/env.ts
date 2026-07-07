/**
 * 模块：src/apps/web-admin/src/config/env.ts
 * 作用：Vite 环境变量读取（API base 等）
 * 怎么用：import { env } from '@/config/env'；变量定义在 .env
 * 解决：环境相关常量单点，避免 import.meta 散落
 * 上游：Vite import.meta.env
 * 下游：api/request/client.ts
 * 关联：ENGINEERING.md
 */
export const env = {
  apiBase: "",
  appTitle: "FactoryOS · Integration Studio",
} as const;