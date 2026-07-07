# vendor · 迁出契约镜像根

## 是什么

**standalone 只读依赖区**：钉死 Platform 契约版本，迁出后零父仓仍可 codegen / 错误码对账。

## 子路径

| 路径 | 说明 |
|------|------|
| `factoryos-contracts/` | OpenAPI · schemas · error-registry · PIN |
| `factoryos-contracts/openapi/` | Platform API YAML → `pnpm codegen:api` |
| `factoryos-contracts/scripts/` | vendor 委托脚本（转发 App `scripts/`） |

## 门禁

```bash
pnpm codegen:check
pnpm codegen:registry:check
./scripts/sync_vendor_contracts.sh
```

## 变更纪律

- 迁出后 **必选**；废止须用户确认 + `devkit.manifest.standalone.yaml`
- 改 PIN → `sync_vendor_contracts.sh` 或 submodule 发布
- 同步 `contracts/directory-readmes.yaml`

## 相关文档

- [factoryos-contracts/README.md](./factoryos-contracts/README.md)
- [ENGINEERING.md](../ENGINEERING.md) §5
