# 验收用例 STU-001：Studio 配置主路径

| 版本 | v1.0.0 |
|------|--------|
| 范围 | Integration Studio（`src/apps/web-admin` `/studio/*`）· Platform Registry（ADR-008） |
| 通过标准 | **P0 全绿**；且 [Integration-Studio 规格 §0 铁律](../../docs/文档/规格说明/Integration-Studio规格.md) STU-R1～R5 无例外 |
| 关联 | [UI-FIRST 宪法](../../.cursor/factoryos/UI-FIRST-CONFIG-PRINCIPLE.md) · [INTEGRATION-CHAIN](../../.cursor/factoryos/INTEGRATION-CHAIN.md) |

**说明**：本用例验证 **「配置极」**——实施与客户 IT **仅通过 Studio** 完成接入与复制。D1 须与 BASE-001、UX-001、MVP-001 **四 Gate 同过**。

---

## 一、Studio 主路径（P0）

| ID | 用例 | 步骤 | 期望 |
|----|------|------|------|
| STU-01 | onboard 零仓库 | Studio 走完 connect→map→prove→freeze→export | **无需** Git / 手改 YAML / `factoryos guide` |
| STU-02 | Registry 写入经 API | connect 后查 `system_relations` | 经 Studio API 落库 |
| STU-03 | Prove 与 Shadow | Studio Prove 步 | shadow 未批准前无生产写 |
| STU-04 | 开写双签 | G-WRITE-APPROVE 上屏 | Audit `integration.write_approved` |
| STU-05 | Graph freeze 上屏 | 负责人 Studio freeze | Audit `GRAPH_FREEZE` |
| STU-06 | Package export | Studio export | 符合 P-01～P-03 |

## 二、复制与禁止项（P0）

| ID | 用例 | 步骤 | 期望 |
|----|------|------|------|
| STU-07 | 第二家 import | Studio import + Override | 界面为主；步骤少于首家 |
| STU-08 | 禁止 Git 日常配置 | 交付记录审查 | 无 YAML 手改上线 |
| STU-09 | integrator 权限 | operator 访问 Studio | 403 |

## 三、共性（P0）

| ID | 用例 | 期望 |
|----|------|------|
| STU-10 | Path 模板 | path-a/b/c 预填 Pack |
| STU-11 | 凭证 | 仅 `secrets_ref` |

```text
D1 结案 = BASE-001 + UX-001 + MVP-001 + STU-001（P0 全绿）
```
