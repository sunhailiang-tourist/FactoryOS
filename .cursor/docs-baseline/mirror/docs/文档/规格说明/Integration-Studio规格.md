# 规格说明·Integration Studio

| 版本 | v1.0.0 |
|------|--------|
| 范围 | GIP 实施 UI/API（P1 MVP） |
| 决策 | ADR-004 · ADR-006 · [17-GIP](../../准备/2026-06-16/17-集成平台化战略(GIP).md) |
| 应用 | `src/apps/web-admin`（`/studio/*`，P1）；Y2 可拆 `apps/integration-studio/` 独立构建 |
| 人工 Gate | [人工决策 Playbook](./人工决策Playbook.md) · [配置枢纽与关系模型](../架构/配置枢纽与关系模型.md) |

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

## 6. 验收

- Prove 步与 AC-BASE-001 T-01、K-01 联动
- Export 与 P-01～P-03 联动
