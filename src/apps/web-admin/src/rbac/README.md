# rbac

## 是什么

权限 sector：角色→权限表 + 路由 `permissions` 全链路对账。

## 子路径

| 路径 | 职责 |
|------|------|
| `contracts/` | 追踪链说明 |
| `core/` | evaluate · RbacGuard · usePermissions |
| `modules/` | 各 domain 权限子表 |

## 门禁

- `scripts/check_harness.py` · `rbac_route_permissions`
- 路由 registry 须声明 `permissions`

## 变更纪律

改 `rbac/modules/{domain}/registry.ts` 须同步 router permissions 与 pages contracts。

## 相关文档

- [rbac/contracts/README.md](./contracts/README.md)
- [ENGINEERING.md §11](../ENGINEERING.md)
