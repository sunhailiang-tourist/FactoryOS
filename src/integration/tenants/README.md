# Tenants（配置枢纽 · 项目级）

> 真源：[配置枢纽与关系模型](../文档/架构/配置枢纽与关系模型.md) · [人工决策 Playbook](../文档/规格说明/人工决策Playbook.md)

每个子目录 = 一个 **tenant**（部署项目单元）。

```text
tenants/
├── _template/              # 复制起点（勿直接 activate）
│   ├── tenant.yaml
│   └── system_relations/
└── {tenant_id}/            # 例：hasen、subsidiary-b
    ├── tenant.yaml
    ├── system_relations/
    ├── cross_relations/    # 可选
    ├── overrides.yaml
    └── packs/
```

**禁止**：在本目录提交明文密钥；使用 `secrets_ref` 指向 Vault / Edge。

**激活**：`system_relations/*.yaml` 经 Studio Connect 或 `factoryos guide` / `factoryos integration connect`（W2+）写入 `connector_instances`。

**新人**：仓库根目录运行 `./scripts/factoryos guide`。
