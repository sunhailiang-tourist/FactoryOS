# Integration Layer（GIP）

> ADR-004 · [17-集成平台化战略(GIP)](../../docs/准备/2026-06-16/17-集成平台化战略(GIP).md) · [16 §2](../../docs/准备/2026-06-16/16-OS核心基座架构设计方案.md)

本目录为 **集成团队主战场**（平台研发视角）。Core 1.0 冻结（`core-v1.0.0`）后，Pack 与 Connector 扩展仍在此演进。

> **对外实施主路径** = Integration Studio（管理台 UI），见 [UI-FIRST-CONFIG-PRINCIPLE](../../.cursor/factoryos/UI-FIRST-CONFIG-PRINCIPLE.md)。  
> **运行时真源** = PostgreSQL Registry（`pack_registry` · `system_relations` · ADR-008）；本目录 YAML 为 **export/import 镜像** 与 **pytest fixture**。

## 目录约定（与 `16` §2 一致）

```text
integration/
├── catalog/               # Connector Blueprint YAML（Runtime 加载真源）
│   └── {system}/{vendor}/ # 例：erp/kingdee-write/blueprint.yaml
├── packs/                 # Pack bundle（graph / ruleset / skill / conn 引用）
├── tenants/               # per-tenant 配置枢纽（见 配置枢纽与关系模型）
│   ├── _template/         # 新客户复制起点
│   └── {tenant_id}/
│       ├── tenant.yaml
│       ├── system_relations/
│       ├── cross_relations/   # 可选
│       └── overrides.yaml
└── tools/
    └── connector-agent/   # AI 生成 Blueprint CLI（P1）
```

## 与 `文档/连接器/` 的边界

| 路径 | 用途 | 谁读 |
|------|------|------|
| **`integration/catalog/`** | **export 镜像** Blueprint（bootstrap → `pack_registry`） | Pack Loader / contract tests |
| **`文档/连接器/catalog/`** | **文档侧**认证样例、Silver 分级参考 YAML | 规格、Studio discover、人工评审 |
| **`文档/连接器/{system}/`** | 厂商调研、request/response **样例 JSON** | Connector-Agent、Contract Test 编写 |

Studio **export** 与 Connector-Agent **产出** 默认写入 `integration/catalog/`；文档侧样例可同步至 `文档/连接器/catalog/` 作认证归档。

**CI**：本目录变更 → Pack contract tests + API smoke；不触发 Core 全量 AC。

**禁止**：import `os_core/*` 非公开 API（见 [os_core-public-api.md](../../docs/文档/架构/os_core-public-api.md)）。

开发前链路：[PRE-DEV-CHAIN](../../.cursor/factoryos/PRE-DEV-CHAIN.md) · 配置轨：[INTEGRATION-CHAIN](../../.cursor/factoryos/INTEGRATION-CHAIN.md)
