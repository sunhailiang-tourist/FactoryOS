# contracts · web-admin 契约

## 文件

| 路径 | 用途 |
|------|------|
| [WEB-ARCHITECTURE-LOCK.yaml](./WEB-ARCHITECTURE-LOCK.yaml) | 架构版图锁 · sector · 技术栈 · 独立边界（机器可读） |

## 变更纪律

1. 改 sector / 技术版图 / 边界 → 用户「确认结构变更」→ bump `version`
2. 校验：`python scripts/check_boundary_lock.py`
