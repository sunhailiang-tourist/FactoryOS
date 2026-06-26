# platform_registry · ADR-008 Registry 平面

## 是什么

Contract / Pack / Tenant 配置的 **DB 真源**访问层与 bootstrap 灌库。

## 模块

| 文件 | 职责 |
|------|------|
| `bootstrap.py` | 幂等 seed（contracts/ + src/integration/ → Registry 表） |
| `contract_store.py` | contract_artifacts 只读 |
| `pack_store.py` | pack_registry Blueprint |
| `tenant_config_store.py` | tenant_profiles · system_relations |
| `change_request_store.py` | config_change_requests 人审写路径 |
| `session.py` | 进程内 Registry Session 绑定 |

## 上下游

- **上游**：conftest · server.api.config.dependencies.db · Studio publish
- **下游**：shared_contracts loaders · connector_sdk.registry · Registry API

## 关联

- [ADR-008](../../../docs/文档/架构/架构决策记录-008-配置与契约平面DB化.md)
