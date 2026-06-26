# os_core/ Public API 边界

> 版本：v1.0.0 | 2026-06-16  
> 用途：`integration/` 仅可调 listed 面；CI import-linter 依据

## 1. 原则

- `os_core/*` 模块间 **禁止** 跨模块 import 私有实现
- `integration/` **禁止** import `os_core/*` 非本表符号
- 扩展 Legacy 接入 **只** 通过 Registry + Blueprint/Pack

## 2. 公开面（integration 可调）

| 模块 | 公开符号 / HTTP |
|------|-----------------|
| `src/server/api` | OpenAPI **v1.1.1** 全部 `/v1/*` 路由 |
| `connector_sdk` | `ConnectorRegistry.register()`, `BlueprintRuntime`（Runtime GA 后） |
| `shared_contracts` | 错误码 enum、Pack ID 常量 |

## 3. 禁止 integration 直接 import

| 模块 | 原因 |
|------|------|
| `execution_service` 内部 | 写路径唯一 |
| `graph_service` 内部 | 须经 API freeze |
| `rule_engine` 内部 | 须经 API evaluate |
| `agent_orchestrator` 内部 | 须经 API plan |

## 4. CI（Coding 启动时启用）

```text
scripts/check_import_boundaries.py
  - os_core/* 无 cross-private import
  - integration/* 无 os_core 非公开 import
```

## 5. 参考

- [命名约定](./命名约定.md)
- ADR-004 §3 `integration/` 物理分离
- [18-基座文档一致性矩阵](../../准备/2026-06-16/18-基座文档一致性矩阵.md)
