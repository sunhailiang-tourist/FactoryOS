# 规格说明·Integration Studio

| 版本 | v1.1.0 |
|------|--------|
| 范围 | GIP 实施 UI/API（P1 MVP） |
| 决策 | ADR-004 · ADR-006 · ADR-008 · [UI-FIRST 宪法](../../../.cursor/factoryos/UI-FIRST-CONFIG-PRINCIPLE.md) · [17-GIP](../../准备/2026-06-16/17-集成平台化战略(GIP).md) |
| 应用 | `src/apps/web-admin`（`/studio/*`，P1）；Y2 可拆 `apps/integration-studio/` 独立构建 |
| 人工 Gate | [人工决策 Playbook](./人工决策Playbook.md) · [配置枢纽与关系模型](../架构/配置枢纽与关系模型.md) |
| 验收 | [STU-001](../验收/验收用例-STU-001-Studio配置主路径.md)（D1 **硬 Gate**） |

## 0. 铁律（钉死 · SaaS 可配置主路径）

> **新客户接入、扩系统、开写、freeze、Package 导出/导入——全程在 Studio 完成；禁止以改 Git / 手改 YAML 作为生产实施路径。**

| # | 铁律 | 违反即 |
|---|------|--------|
| **STU-R1** | 租户 `tenant_profiles`、`system_relations`、`connector_instances`、`override_documents` 的 **published 写入** 仅经 Studio UI → `/v1/registry/*` 或 `/v1/integration/*` | 不算 D1 交付完成 |
| **STU-R2** | 实施顾问/客户 IT **无需** clone 仓库、编辑 `integration/tenants/`、执行 `factoryos guide` 完成 onboard | STU-001 不通过 |
| **STU-R3** | `G-FREEZE`、`G-WRITE-APPROVE` 等人审 Gate **必须有** Studio 界面动作 + Audit 事件 | 禁止静默开写 |
| **STU-R4** | Git 中 `integration/`、`contracts/` 仅为 **export/fixture/CI 镜像**；日常配置变更 **不得** 以 PR 改 YAML 替代 Studio publish | ADR-008 废止口径 |
| **STU-R5** | 第二家起 S1 复制：**import 向导** 为主路径；仓库 diff 仅作平台研发 diff 审计 | D1 后 KPI |

**与 SaaS 关系**：托管与私有化 **共用** Registry DB 模型；差异仅在 tenant 数量与 cell 隔离（ADR-008 §2）。Studio 是两种部署形态下 **唯一的配置/实施主入口**。

## 1. 职责

为集成/实施人员提供 **不改 Core 源码** 的接入闭环：连通 → 发现 → 映射 → 验证 → 冻结 → 导出。

**不是**：工人 H5（属 Harness）；**不是** 全功能 Pack 市场（Y2）。

## 2. 六步向导

| 步 | ID | 功能 | API（OpenAPI **v1.1.1**） | 产出 |
|----|-----|------|-------------------|------|
| 1 | **connect** | 凭证 ref、ping、Edge Agent 状态 | `POST /v1/integration/connect/test` | 连通报告 |
| 2 | **discover** | 上传 OpenAPI/Blueprint；列候选 CMV | `POST /v1/integration/discover` · `POST /v1/integration/blueprint/validate` | 动词候选清单 |
| 3 | **map** | 字段映射编辑；AI 建议 confidence | `PUT /v1/integration/mappings/{packId}` | mapping.yaml |
| 4 | **prove** | Shadow 开关；Contract Test；对账样例 | `POST /v1/integration/prove/run` | 开写批准书 |
| 5 | **freeze** | Graph 工作坊提交/冻结 | `POST /v1/graphs/{id}/versions/{version}/submit` · `.../freeze` | frozen Graph |
| 6 | **export** | Implementation Package | `POST /v1/packages/export` | Package JSON |

## 2.1 Platform Registry（ADR-008 · 配置真源）

| 能力 | API | 说明 |
|------|-----|------|
| 读 Pack/Tenant/Contract | `GET /v1/registry/*` | Studio 列表与详情 |
| AI/人提案 | `POST /v1/registry/change-requests` | **pending**，不直接改库 |
| 人审批准 | `POST .../approve` | 写入 `pack_registry` / `system_relations` |
| 人审拒绝 | `POST .../reject` | R-09：AI 不得自动 publish |

`contracts/openapi` 与 `server/api/data/studio_flows.json` 为 export/辅助；**运行时真源 = PostgreSQL Registry**。

## 3. Prove 步硬规则

1. `tenant.shadow_mode=true` 期间 **禁止** 开生产写（见 Shadow 规格）。
2. Contract Test 全绿（Pack 级）。
3. 对账 K-01 样例通过或 drift 可解释。
4. 人工签字记录写入 Audit（`event_type=integration.write_approved`）。

## 4. 权限

| 角色 | 能力 |
|------|------|
| `role:integrator` | Connect～Export |
| `role:admin` | + tenant shadow 开关 |
| `role:operator` | 无 Studio 访问 |

## 5. Phase

| Phase | 范围 |
|-------|------|
| P1 MVP | 六步 API + 最小 Web 四页（Connect/Prove/Freeze/Export） |
| Y2 | Override 可视化、Pack 目录、drift 仪表盘 |

## 6. 验收（硬 Gate）

**D1 / 第二家复制**：须 [STU-001](../验收/验收用例-STU-001-Studio配置主路径.md) **P0 全绿**，且满足上文 **§0 铁律 STU-R1～R5**。

| 联动 | 说明 |
|------|------|
| Prove | AC-BASE-001 T-01、K-01 |
| Export / import | P-01～P-03 + STU-04、STU-05 |
| 内核 | STU-001 与 BASE-001、UX-001、MVP-001 **四 Gate 同过** 方可宣告 D1 结案 |

**未达标**：允许平台研发用 Git/fixture 调试，**不得** 对客户宣称「已 SaaS 可配置交付」。
