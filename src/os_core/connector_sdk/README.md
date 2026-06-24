# connector_sdk · 连接器 SDK

## 是什么

Legacy **读/写** httpx 适配、Blueprint Runtime、Pack Registry 加载。

## 主要功能

- Connector Pack 实例化、mapping、resilience
- 仅被 `execution_service` 调用写路径

## 不负责什么

- 业务规则、租户 `if` 分支
- Pack 源码（在 `integration/packs`）

## 上下游

- **上游**：`execution_service`
- **下游**：Legacy ERP/MES HTTP、Edge Agent 隧道

## 相关文档

- `文档/连接器/` · Connector-Blueprint 规格
