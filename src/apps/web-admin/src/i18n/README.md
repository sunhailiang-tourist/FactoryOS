# i18n

## 是什么

国际化 sector：按 `module-id` namespace 维护 `zh-CN.json` / `en-US.json`。

## 子路径

| 路径 | 职责 |
|------|------|
| `contracts/` | 登记索引与变更规则 |
| `core/` | Provider · useT · useLocale |
| `modules/` | 各 namespace 文案 JSON |

## 门禁

- `scripts/check_harness.py` · `i18n_registry_sync`
- ESLint：业务代码禁止直引 `i18next`

## 变更纪律

新增 module-id 须同步 `modules/{id}/` 双语文案与 `contracts/README.md` 登记索引。

## 相关文档

- [ENGINEERING.md §11](../ENGINEERING.md)
- [ARCHITECTURE.md](../ARCHITECTURE.md)
