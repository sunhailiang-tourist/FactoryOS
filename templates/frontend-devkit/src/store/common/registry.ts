/**
 * 模块：src/apps/web-admin/src/store/common/registry.ts
 * 作用：跨模块 store 公共条目（如 actor/session）
 * 怎么用：登记 key 须在相关 pages/contracts 追踪链出现
 * 解决：避免各模块重复 session 状态
 * 上游：api/request/interceptors
 * 下游：pages 与 layout 模块
 * 关联：store/contracts/README.md
 */
import type { StoreModuleEntry } from "@/store/types";

export const STORE_COMMON_ENTRIES: StoreModuleEntry[] = [];