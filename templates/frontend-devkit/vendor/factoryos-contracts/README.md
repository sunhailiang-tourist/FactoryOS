# factoryos-contracts · standalone 只读镜像

> **pin**：`core-v1.0.0`（见 [PIN](./PIN)）  
> **用途**：web-admin 迁出后 OpenAPI / error-registry **只读消费**，不依赖 FactoryOS 父仓 `contracts/`。

## 内容

| 路径 | 说明 |
|------|------|
| `openapi/工厂操作系统-v1.1.yaml` | Platform API v1.1.1 · `pnpm codegen:api` / `codegen:check` |
| `schemas/` | OpenAPI 外引 JSON Schema（codegen bundle 必需） |
| `error-registry.yaml` | 业务错误码 SSOT 镜像 · `scripts/sync_error_registry.py`（App 内自给） |
| `PIN` | 契约包版本钉死 |

## 更新（umbrella 内维护）

```bash
./scripts/sync_vendor_contracts.sh
```

迁出后可通过 git submodule 替换本目录；`devkit.manifest.standalone.yaml` 登记 `pin: core-v1.0.0`。
