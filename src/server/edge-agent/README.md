# server/edge-agent · 边缘代理

## 是什么

部署在客户私网的 **独立进程**：出站 WSS 隧道，代 `connector_sdk` 访问不可公网直达的 ERP。

## 主要功能

- 与云端 `server/api` 建立安全通道
- 转发 Connector 读写至内网 `base_url`
- 凭证本地解密（`secrets_ref`），禁止明文进 Git

## 不负责什么

- DSL 执行、Graph/Rule（仍在云端 `os_core`）
- 替代完整 MES/ERP 客户端

## 上下游

- **上游**：云端 `execution_service` → Connector 实例（`edge_agent_id`）
- **下游**：客户内网 ERP HTTP

## 落位说明（架构闭合 #6）

- **P1 PoC**：单租户、单 ERP 隧道
- 与 `integration/tools/connector-agent` 文档对齐；生产镜像独立发布

## 相关文档

- [配置枢纽与关系模型](../../文档/架构/配置枢纽与关系模型.md)
- SystemRelation `spec.instance.edge_agent_id`
