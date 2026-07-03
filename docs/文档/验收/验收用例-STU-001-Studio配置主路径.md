# 验收用例 STU-001：Studio 配置主路径

| 版本 | v1.0.0 |
|------|--------|
| 范围 | Integration Studio（`src/apps/web-admin` `/studio/*`）· Platform Registry（ADR-008） |
| 通过标准 | **P0 全绿**；且 [Integration-Studio 规格 §0 铁律](../规格说明/Integration-Studio规格.md) STU-R1～R5 无例外 |
| 关联 | [UI-FIRST 宪法](../../../.cursor/factoryos/UI-FIRST-CONFIG-PRINCIPLE.md) · [INTEGRATION-CHAIN](../../../.cursor/factoryos/INTEGRATION-CHAIN.md) · [04-工厂实施手册](../../准备/2026-06-16/04-工厂实施手册.md) |

**说明**：本用例验证 **「配置极」**——SaaS/托管与私有化下，实施与客户 IT **仅通过 Studio** 完成接入与复制。内核门禁仍以 [BASE-001](./验收用例-BASE-001-平台底座.md) 为准；终端体验以 [UX-001](./验收用例-UX-001-终端体验与多模态.md) 为准；垂直闭环以 [MVP-001](./验收用例-MVP-001-报工垂直闭环.md) 为准。**D1 四 Gate 缺一不可**。

---

## 一、Studio 主路径（P0）

| ID | 用例 | 步骤 | 期望 |
|----|------|------|------|
| STU-01 | onboard 零仓库 | 实施顾问在 **仅** Studio + 浏览器环境下走完 connect→map→prove→freeze→export | **无需** 打开 Git、编辑 `integration/tenants/*.yaml`、运行 `factoryos guide` |
| STU-02 | Registry 写入经 API | 完成 connect 后查 DB `system_relations` / `connector_instances` | 记录存在；`lifecycle` 符合 Studio 操作；**非** 手灌 fixture 独有 |
| STU-03 | Prove 与 Shadow | Studio Prove 步开启 shadow、跑 Contract Test、对账样例 | `tenant.shadow_mode=true`；未批准前 L2 写 Legacy **403 或 simulated** |
| STU-04 | 开写双签 | Studio 完成 G-WRITE-APPROVE | Audit 含 `integration.write_approved`；`write_approved=true` 后方可生产写 |
| STU-05 | Graph freeze 上屏 | 业务负责人在 Studio freeze | Audit 含 `GRAPH_FREEZE`；**无** API 直调 freeze 绕过 UI 的生产路径 |
| STU-06 | Package export | Studio export Implementation Package | 可下载 JSON；含 Graph/Rule/Pack 引用；与 P-01～P-03 一致 |

---

## 二、复制与禁止项（P0）

| ID | 用例 | 步骤 | 期望 |
|----|------|------|------|
| STU-07 | 第二家 import | 新 tenant 在 Studio 选路径模板 + import Package + 填 Override | **主要** 在界面完成；首家→第二家步骤数 **减少**（UI-FIRST U5 KPI） |
| STU-08 | 禁止 Git 日常配置 | 检查 D1 交付 Runbook 与实施记录 | 无「改 YAML 上线」步骤；`integration/` 变更仅为 export 快照 |
| STU-09 | integrator 权限 | `role:operator` 访问 `/studio/*` | **403**；`role:integrator` 可走完六步 |

---

## 三、与 Path 无关的共性（P0）

| ID | 用例 | 步骤 | 期望 |
|----|------|------|------|
| STU-10 | Path A/B/C 模板 | Studio 创建 tenant 时选择 path-a / path-b / path-c 模板 | 预填 Pack 组合；差异仅在 Connector 与账本落点（ADR-005） |
| STU-11 | 凭证不进 Registry 明文 | Connect 步提交凭证 | Registry 仅存 `secrets_ref`；无明文密钥字段 |

---

## 四、优先级与 Gate 关系

| 优先级 | 条目 |
|--------|------|
| **P0** | STU-01～STU-11（D1 硬 Gate） |
| P1 | drift 仪表盘、Override 可视化（Y2 Studio v2） |

```text
D1 结案 = BASE-001 P0 绿 + UX-001 P0 绿 + MVP-001 P0 绿 + STU-001 P0 绿
```

---

## 五、参考

- [Integration-Studio 规格 §0 铁律](../规格说明/Integration-Studio规格.md)
- [ADR-008 配置平面 DB 化](../架构/架构决策记录-008-配置与契约平面DB化.md)
