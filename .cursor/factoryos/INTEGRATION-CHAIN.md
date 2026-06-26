# 接入与扩展链 · INTEGRATION-CHAIN（配置平面）

> **硬性规定**：[UI-FIRST-CONFIG-PRINCIPLE.md](./UI-FIRST-CONFIG-PRINCIPLE.md)  
> **产品核心不变**；本链描述 **对外表现形态**：管理台界面 + AI，不是 CLI/改仓库。

---

## 一、谁走这条链

| 角色 | 做什么 | **不走** |
|------|--------|----------|
| 实施顾问 | Studio 向导：接入 · 扩展 · import | `factoryos guide` 作主路径 |
| 客户 IT | Connect · 凭据 · 连通确认 | 手改 `integration/tenants/` |
| 业务负责人 | Graph 工作坊 · freeze 签字 · UAT | 读 Playbook 长文代替系统 |
| 平台研发 | 实现 API + Studio 页面 | 把 YAML 当客户配置真源 |

---

## 二、五条业务流（界面呈现）

与 `flows.json` 一一对应；**界面显示 Gate 状态 + 下一步表单**。

| flow | 场景 | 界面入口（规划） |
|------|------|------------------|
| `onboard` | 第一家 D1 全链路 | Studio → 新客户向导 |
| `import` | 第二家起 S1 Package | Studio → 导入 + 差异表单 |
| `extend-vendor` | 新 ERP/MES 厂商 | Studio → 扩展 Connector |
| `extend-d2` | D2 定制 Pack 化 | Studio → 扩展能力 |
| `ops` | drift / revert / 熔断 | Studio → 运维台 |

命令 `./scripts/factoryos guide <flow>`：**仅平台内部调试**，见 UI-FIRST §U4。

---

## 三、人审 Gate（必须在界面完成）

来自 Playbook；**禁止** 仅靠文档或 CLI 跳过。

| Gate | 界面行为 | Audit |
|------|----------|-------|
| G-FREEZE | 业务负责人签字冻结 Graph | `graph.frozen` |
| G-WRITE-APPROVE | admin + 业务双签开写 | `integration.write_approved` |
| G-BRONZE-REVIEW | platform 审 Blueprint | 审阅记录 |
| G-UAT | 试点签字 | UAT 附件/签字 |

半自动（映射 AI 建议）仍须在 UI 点「确认」后落库。

---

## 四、与研发轨的关系

```text
配置轨（本文件）  实施/客户在 Studio 操作 · 沉淀 UX
研发轨（PRE-DEV-CHAIN）  平台团队写 src/server/os_core · src/server/api · Studio · SH-步步流
```

Gate 0 完成 = 内核 API 就绪 → Studio v1 接真数据；**Studio v0 可与 W1 并行 mock**。

---

## 五、机器真源（ADR-008 · 避免 AI 误读 Git 路径）

| 类型 | published / 运行时真源 | export / 辅助镜像 |
|------|------------------------|-------------------|
| Pack / Tenant / Relation / Override | PostgreSQL Registry + `/v1/registry/*` | `src/integration/` |
| OpenAPI / Schema / CMV / AC | Contract Registry publish/frozen | `contracts/` |
| Gate 状态机（实施） | Playbook 语义 + Studio API | `flows.json` · `studio_flows.json` |
| 源码 / DDL | Git · `src/server/db/migrations/` | — |
| Studio UI | `src/apps/web-admin` `/studio/*` | 规格见 docs |

---

## 六、验收口径（产品）

- [ ] 实施顾问 **无需** 打开仓库即可走完 onboard 故事（界面或演示环境）  
- [ ] 每个人审 Gate 有 UI 动作 + Audit 可查  
- [ ] 第二家 import 主要在界面完成（D1 后 KPI）  
- [ ] `guide` 文档明确标注「内部/调试」
