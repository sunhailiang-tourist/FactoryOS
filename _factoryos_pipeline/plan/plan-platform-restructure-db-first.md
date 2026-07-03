# 平台化整改总方案 · B 档最强形态（终稿 v2）

> **状态**：Accepted · 待用户「确认编码门禁，开始 W5」执行代码  
> **日期**：2026-06-26  
> **ADR**：[架构决策记录-008-配置与契约平面DB化.md](../../docs/文档/架构/架构决策记录-008-配置与契约平面DB化.md)  
> **同步清单**：[SYNC-SNAPSHOT-platform-restructure.md](./SYNC-SNAPSHOT-platform-restructure.md)  
> **Migration 草稿**：`artifacts/004_platform_registry.py`

---

## 0. 阅读核实（全量）

| 目录 | 实质文件 | 说明 |
|------|----------|------|
| `.cursor/` | ~100 | factoryos/rules/hooks/baseline（跳过 mirror 重复） |
| `docs/` | ~134 | 排除 `.venv-diagram` `.venv-ppt` |
| `_factoryos_pipeline/` | 446 | plan/test/verify + gate 日志 |
| `src/` | 111 | 全部通读 |
| `scripts/` | 32 | 全部通读 |

---

## 1. 终态裁定（一步到位目标）

```text
L5  Studio + AI（config_change_requests → 人审 → publish）
L4  server/api
L3  server/core（execution 唯一写路径 · ADR-002 不变）
L2  PostgreSQL Registry（18 表 + connector_instances 扩列）
L1  server/db/migrations（Alembic · deployment_schema_audit）
```

**废止编辑真源**：`integration/` · `contracts/`（export/fixture 除外）  
**apps/**：仅 web-admin · h5-worker · 未来终端

---

## 2. 最终项目结构（2026-06-26 修订 · 代码根在 src/）

```text
FactoryOS/
├── src/
│   ├── server/
│   │   ├── os_core/             # 内核 + platform_registry（import: os_core.*）
│   │   ├── api/                 # FastAPI（import: server.api.*）
│   │   ├── edge-agent/
│   │   └── db/migrations/       # 含 004_platform_registry
│   ├── apps/web-admin/ · h5-worker/
│   ├── integration/             # export/fixture 镜像
│   └── tests/
├── contracts/                   # export 镜像 · CI 对账
├── scripts/
├── docs/
└── alembic.ini → src/server/db/migrations
```

---

## 3. B 档数据库（18 新建 + 1 扩列 + 1 审计）

### 已有 8 表（继续）

tenants · connector_instances · tenant_quotas · outbox_events · audit_events · execution_records · business_graphs · rulesets

### 新建 18 表

| # | 表 | 替代原职能 |
|---|-----|-----------|
| 1-6 | contract_sets / artifacts / compatibility_rules / environment_bindings / publish_records / consumer_pins | contracts/ |
| 7-8 | pack_registry / pack_certification_records | integration/catalog |
| 9-13 | system_relations / tenant_profiles / override_documents / tenant_pack_entitlements | integration/tenants |
| 14-16 | config_versions / snapshot_blobs / config_rollback_points | Git 快照 |
| 17-18 | config_change_requests / import_export_jobs | AI+UI 出入库 |

### 扩列 + 审计

- **connector_instances** + relation_id, base_url, secrets_ref, edge_agent_id, environment, mapping_overrides_json  
- **deployment_schema_audit** — Alembic 发版追溯

**合计业务表：8 + 18 = 26**（+ alembic_version）

---

## 4. Agent / Graph（与改造兼容）

- Studio：connect → discover → map → prove → freeze  
- Agent **只读** discover；草案 → config_change_requests / business_graphs(draft)  
- **R-01 R-09 不变**；凭证仅 secrets_ref，不进 Registry 明文  
- 私有化/托管同一 Registry 模型

---

## 5. 工作流影响（已统计）

| 必改 | 数量 |
|------|------|
| `.cursor` | 22 |
| `scripts` | 14 |
| `docs` | 15+ |
| `src`+tests | ~25 |
| pipeline 模板 | 若干 |

**不变**：Dev→Test→Verify 节拍 · 关键词闸门

---

## 6. 落地 PR 序列（代码）

| PR | 内容 | 估时 |
|----|------|------|
| **P0** | ADR-008 + 004 migration + platform_registry 骨架 | 2-3d |
| **P1** | server/ 重组 + import 全局 | 3-5d |
| **P2** | loader 切 DB + seed + Gate | 3-4d |
| **P3** | Studio v0 + 废止 Git 真源 + 全量 SYNC | 5-8d |
| **合计** | | **18-28 人天** |

---

## 7. 业界对标（2025-2026）

- **Salesforce metadata-driven** · **Confluent Schema Registry** · **ServiceNow CMDB**  
- **Agent Registry**：config-as-data · publish audit · version rollback · policy pin  
- **Palantir OMS**：metadata 结构 + indexed 实例 + Actions 写路径分离

---

## 8. 验收

- [ ] 运行时零读 integration/catalog 与 contracts/cmv 文件  
- [ ] gate plan L0 对 published contract_set  
- [ ] W4 回归绿（DB seed conn-mock）  
- [ ] ADR-002 红线测试仍绿  
- [ ] 实施零要求手改 integration/tenants yaml

---

## 9. 当前落盘状态（2026-06-26）

| 项 | 状态 |
|----|------|
| 本 plan v2 | ✅ |
| SYNC-SNAPSHOT | ✅ |
| ADR-008 | ✅ docs |
| 004 migration | ✅ pipeline/artifacts（待复制 src/server/db/migrations/versions/） |
| src 代码改造 | ⏸ 待「确认编码门禁，开始 W5」 |
