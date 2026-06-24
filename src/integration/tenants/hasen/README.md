# 哈森灯塔租户（Path A）

## 是什么

Gate 0' **灯塔工厂**配置草案：ERP 写+读 + 钉钉；`shadow_mode: true` 直至人工批准写。

## 主要功能

- `tenant.yaml`：租户画像、授权 Pack、Path A
- `system_relations/`：金蝶 ERP SystemRelation（draft）

## 不负责什么

- 明文凭证（仅用 `secrets_ref`）
- 自动 activate（须 `factoryos integration` / 人工 Playbook）

## 上下游

- **上游**：集成工程师 Git PR
- **下游**：activate 后 → `connector_instances`（W2+ API）

## 相关文档

- [人工决策Playbook](../../文档/规格说明/人工决策Playbook.md)
- [SystemRelation.schema.json](../../文档/数据结构/SystemRelation.schema.json)
