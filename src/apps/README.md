# apps · 应用域

## 是什么

面向用户与部署的 **应用入口**：API、管理端、工人 H5、边缘 Agent。业务规则在 `os_core/`，此处仅适配与展示。

## 主要功能

| 子目录 | 职责 |
|--------|------|
| `api/` | FastAPI 唯一生产 deployable |
| `web-admin/` | PC 管理端 |
| `h5-worker/` | 钉钉/企微工人壳 |
| `edge-agent/` | 私网 ERP 出站代理（P1 PoC） |

## 不负责什么

- DSL 执行、写 Legacy 逻辑（须调 `os_core`）
- Pack / tenant 配置编辑真源（`integration/`）

## 上下游

- **上游**：浏览器、IM、Edge 设备、MCP 客户端
- **下游**：`os_core/*` public API、PostgreSQL（经 api）

## 相关文档

- [FactoryOS完整架构设计](../../docs/文档/架构/FactoryOS完整架构设计.md) §部署
- [编码绝对门禁](../../.cursor/factoryos/DEV-GATES.md) · [PRE-DEV-CHAIN](../../.cursor/factoryos/PRE-DEV-CHAIN.md)
