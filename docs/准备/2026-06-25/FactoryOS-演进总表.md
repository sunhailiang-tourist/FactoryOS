# FactoryOS 演进总表

> **版本**：v1.0 · **2026-06-25**  
> **用途**：老板看价值与节奏 · 研发看阶段目标与验收 · **编码真源仍以 `contracts/`、`REDLINES.md` 为准**  
> **当前**：**阶段 0**（Gate 0 未完成）

---

## 1. 定位（三句）

| 项 | 内容 |
|----|------|
| **是什么** | ERP/MES **之上**的受治理 AI 运行层：Graph 走流程 + Harness 控写 + Audit/Revert/对账 |
| **不是什么** | 不替 ERP 当账本 · 不做无审计 Agent · 不做 Day1 数仓/全厂自治 |
| **终局** | **Graph（怎么操作）+ Experience（怎么判断）** → 治理内 **Factory Brain**（routine 少人指挥） |

---

## 2. 演进总表（一张表看全阶段）

| 阶段 | 名称 | 时间 | 解决什么 | 沉淀什么 | 老板看什么 | 研发做什么 | 阶段关门 |
|:----:|------|------|----------|----------|------------|------------|----------|
| **0** | 筑基 | **现在** | 没有统一契约与写路径，接厂必乱 | L2 骨架：契约、DB、mock Connector | 「内核可测，能开始接厂」 | W1～W8：Alembic、execution/audit 骨架、边界门禁 | **Gate 0 全绿**（AC-BASE-001 P0） |
| **1** | 会操作 | Gate 0 后 | 人学 ERP 成本高；不敢让 AI 写库 | **L1 Graph + L2 Execution**；Package v1 | **D1 签字 = 能 demo、能收费** | 陀螺匠/灯塔：1 条链 freeze → Shadow → UAT | **D1-1～D1-5 全过** + Shadow≥14 天 + export Package |
| **2** | 能复制 | D1 后～12 月 | 每家从零集成，无法规模化 | Pack import 能力；SaaS 多 tenant | **第二家 2～3 周**；3～5 家 tenant | Registry import/export · RLS · Edge Agent · Studio MVP | 第二家 D1 ≤3 周 · **≥3 tenant** 稳定运行 |
| **3** | 会理解 | Y2 起 | ERP 只有事实，没有「为什么」 | **L3 Experience**（按岗位结构化） | **「人走了经验还在」** | `ExperienceEntry` Schema · 岗位 Pack 采集 UX · 检索 | AC-EXP-001：录入→检索→Agent 引用→Audit 可追溯 |
| **4** | 会决策 | Y3 起 | 排产/采购靠人脑；模型易胡编 | **L4 Decision**；决策 trace | AI **带引用**给方案，人批后写 | Planner：Graph+Experience → 多方案 + `cited_ids` · Rule 白名单试 L3 | 方案必引用 Experience/Graph · Shadow 过才开 L3 |
| **5** | 能自治 | Y4～Y7 | routine 仍要人盯，效率天花板 | **Factory Brain**（治理内跨域编排） | 少人指挥 **白名单场景** | Agent L3/L4 按场景放开 · drift 告警 · 可一键降级 L2 | 自治场景全 Audit/Revert/对账 · **零重大未回滚事故** |
| **→** | 网络复利 | 2030+ | 单厂经验无法跨厂复用 | Learning Graph · 行业 Pack 网络 | 平台叙事 / 资本市场 | Pack 市场 · 跨 tenant 模式迁移（仍 Overlay） | 不设工程硬 Gate，随 3～5 成熟 |

**GPT 三阶段对照**：阶段 1＝操作企业 · 阶段 3＝理解企业 · 阶段 4～5＝经营企业（决策→自治）

---

## 3. 四层架构（全阶段共用内核）

| 层 | 名称 | 阶段激活 | 存什么 | 谁用 |
|----|------|:--------:|--------|------|
| **L1** | Operational | 0～1 建满 | System Map + **Business Graph**（freeze 的业务链） | Execution / Agent 知道「能做什么、走哪条链」 |
| **L2** | Execution | 0～1 建满 | Intent→Graph→Rule→Harness→写 Legacy→Audit/Revert/对账 | 所有写 Legacy **唯一路径** |
| **L3** | Experience | **3** 起 | 事件→判断→原因→措施→结果→置信度→**岗位 Role** | 阶段 4 Planner 检索；Rule 条件 |
| **L4** | Decision | **4** 起 | 多方案、模拟、引用链 | 人批或 L3 白名单自治 |

**写 Legacy 铁律**：仅 `execution_service` · 任何阶段不得绕过 Harness/Rule/Audit。

---

## 4. 双资产（阶段 1 起 Graph，阶段 3 起 Experience）

| 资产 | 回答什么 | 从哪来 | 阶段 |
|------|----------|--------|:----:|
| **Business Graph** | 企业 **怎么操作**（报工、确认、查询…） | 工作坊 freeze + Connector 映射 | 1 |
| **Experience** | 企业 **怎么判断**（为什么、怎么办、适用谁） | 质检/工艺/采购/设备/计划 等岗位 Harness 结构化采集 | 3 |

**Experience 单条结构**：Event → Context → Judgment → Cause → Action → Outcome → Confidence → Scope → **Role** → 关联 `exec_id`/`graph_id`

---

## 5. 各阶段开发清单

### 阶段 0 — 筑基（当前）

| 工作 | 产出 | 验收 |
|------|------|------|
| 契约 + Alembic S-01～S-04 | `shared_contracts`、迁移可跑 | pytest 绿 |
| mock Connector | 不接真实 ERP 生产写 | AC-BASE 子集 |
| execution / audit / graph / rule 骨架 | 模块可 import、边界静态过 | `./scripts/gate step` |
| W6～W8 对账 stub、revert 骨架 | Gate 0 材料齐 | **AC-BASE-001 P0 全绿** |

**禁止**：真实 ERP 生产写 · 为多端 App 分散主力

---

### 阶段 1 — 会操作（D1）

| 工作 | 产出 | 验收 |
|------|------|------|
| 陀螺匠 Connector read/write | 字段映射、样例单据 | D1-1 跨系统只读 |
| Graph 工作坊 → freeze | 5～8 节点，人签字 checksum | 链路与 freeze 一致 |
| Rule + DSL + Harness | 写仅经 DSL+Rule | D1-2 |
| ExecutionRecord + Audit | 每次写可追溯 | D1-3 |
| Revert | WORK_REPORT_REVERT 可演示 | D1-4 |
| 对账 Job | OS vs ERP read-back | D1-5 零 drift 或告警闭环 |
| Shadow ≥14 天 | 写零生产或 dry_run | 实施手册 Gate |
| export | Implementation Package v1 | 供阶段 2 import |

**接厂顺序（强制）**：只读摸底 → Graph freeze → Rule/Harness → Shadow → UAT/Revert → 对账 → D1 签字

**本阶段场景**

| ID | 角色 | 场景 | 入口 |
|----|------|------|------|
| S-01 | 工人 | 报工 WORK_REPORT | API / 简易 H5 / 钉钉 |
| S-02 | 主管 | 确认/驳回 | Harness 待办 |
| S-03 | 文员/计划 | 查工单/历史 | API / 自然语言 |
| S-04 | IT/财务 | 审计/对账/撤回 | 管理台 |

**本阶段不做**：自动财务过账 · 无确认排产写回 · 全厂数仓 · PC/App 齐套（非阻塞）

**Agent 级别**：L0～L2（人确认门）· L3 自动 **不在本阶段**

---

### 阶段 2 — 能复制

| 工作 | 产出 | 验收 |
|------|------|------|
| Pack Registry | export/import JSON + tenant Override | 第二家 **2～3 周** D1 |
| SaaS Pool | 单栈多 tenant + RLS | 隔离测试通过 |
| Edge Agent | 私网 ERP 出站 | ≥1 家私网 PoC |
| Integration Studio | 映射/试跑/证明 | MVP 可演示 |
| MCP Gateway | tools → DslPlan，**禁直写 Legacy** | 内部 GA |

**禁止**：内核 `if tenant_id == xxx` · 未经 ADR 改 Layer 0 写路径

---

### 阶段 3 — 会理解

| 工作 | 产出 | 验收 |
|------|------|------|
| `ExperienceEntry.schema.json` 入 contracts | Role enum、link exec_id | Schema 评审过 |
| 岗位 Pack UX | 质检/工艺/采购/设备/计划 Harness 扩展字段 | 非自由聊天入库 |
| 存储 + 检索 | tenant 隔离、append、supersede 废止 | AC-EXP-001 全绿 |
| Agent cite | 建议时标注引用 Experience ID | Audit 可追溯 |

**岗位 Pack 示例**：`exp-quality-inspector` · `exp-process-engineer` · `exp-purchaser` · `exp-maintenance` · `exp-planner`

---

### 阶段 4 — 会决策

| 工作 | 产出 | 验收 |
|------|------|------|
| Planner | Graph 合法动词 + Experience top-k | 输出多方案 + `cited_experience_ids[]` |
| Rule 扩展 | 置信度≥θ + 场景白名单 → 允许 L3 | ADR-002 合规 |
| Shadow / dry_run | 开 L3 前必过 | 无 wild autowrite |
| Decision trace | 写入 Audit + Evidence | 责任可追 |

**依赖**：单 tenant **≥1 万条**有效 Experience（或行业 Pack 等效）

---

### 阶段 5 — 能自治（Factory Brain）

| 自治级 | 含义 | 典型场景 | 治理 |
|--------|------|----------|------|
| L0～L2 | 人主导 | 阶段 1 报工 | Harness 必确认 |
| **L3** | 单场景无人闭环 | 低风险通知、标准检验通过 | Rule 白名单 + 全 Audit |
| **L4** | 多步编排自治 | 标准插单、标准催料 | Simulation 前置 + drift 告警 |
| **Brain** | 跨域建议+执行 | 排产/采购联动（仍 Policy 内） | 可降级回 L2 |

**关门条件**：自治域内长期 **Audit/Revert/对账** 可用 · 无重大未回滚写库事故

---

## 6. 决策链（阶段 4 起 · 全团队同一图）

```text
事件 → 检索 L1 Graph + L3 Experience
     → Planner 出方案（带引用）
     → Rule 硬约束 + Harness（人批 或 L3 白名单）
     → execution_service 写 Legacy
     → Audit / 对账 / 可 Revert
```

---

## 7. 能力落盘对照（避免「文档有、代码无」）

| 能力 | 阶段 | contracts/代码 |
|------|:----:|:--------------:|
| Business Graph freeze | 1 | ✅ 规划中 · W2+ 实现 |
| Harness / Revert / 对账 | 1 | ✅ REDLINES · W2+ |
| Agent L0～L2 | 1 | ✅ ADR-002 |
| Pack import/export | 2 | 待实现 |
| Experience Schema | 3 | ❌ 待入 contracts |
| Experience 检索 → Planner | 4 | ❌ 待实现 |
| Agent L3 / Factory Brain | 4～5 | ❌ ADR-002 Phase 2+ |

---

## 8. 文档索引（细节查原文，本文不再重复）

| 主题 | 真源 |
|------|------|
| D1 细则、接厂手册 | `docs/准备/2026-06-16/08-平台战略与两次交付模型.md` · `04-工厂实施手册.md` |
| W1～W8、Gate 0 | `16-OS核心基座架构设计方案.md` · `14-一年冲刺路线图与并行研发.md` |
| 红线、Agent 级别 | `.cursor/factoryos/REDLINES.md` · ADR-002 |
| 契约与 AC | `contracts/` · AC-BASE-001 |
