/**
 * 模块：src/apps/web-admin/src/rbac/core/types.ts
 * 作用：Permission · Role · 评估模式类型
 * 怎么用：evaluate · router/types 引用
 * 解决：权限字符串 SSOT 形状
 * 上游：rbac/modules/·registry.ts
 * 下游：rbac/core/evaluate.ts
 * 关联：rbac/contracts/README.md
 */

    export type Permission = string;
    export type Role = string;
    export type PermissionMode = "all" | "any";
