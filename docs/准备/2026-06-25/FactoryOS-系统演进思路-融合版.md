# FactoryOS 系统演进思路（融合版）

> **版本**：v1.0.0 · **日期**：2026-06-25  
> **读者**：老板（看价值与节奏）· 技术负责人/研发（看做什么、怎么验收）  
> **融合来源**：顶级 Overlay 策略 · ChatGPT 三阶段演进（Execution → Experience → Brain）· 项目已定稿 ADR/`contracts`/`REDLINES`  
> **工程真源（编码以之为准）**：`contracts/` · `.cursor/factoryos/REDLINES.md` · `docs/准备/2026-06-16/08-平台战略与两次交付模型.md`

---

## 一、30 秒读懂

**我们是什么**

> **FactoryOS = 制造业「受治理的企业行动上下文平台」**  
> 不替换 ERP/MES 账本，在其之上提供：**Graph 业务流程 + AI 轻入口 + 受控写回 + 审计/对账/回滚**。

**演进一句话**

> **先冻结并执行 Business Graph（人会操作）→ 再按岗位沉淀 Experience（人走了经验还在）→ 再让模型在 Graph+Experience 上决策参考 → 最后在治理框架内分级自治，演进到 Factory Brain（无人指挥的工厂体系是终局，不是 Day1）**  
> ERP 始终是账本；FactoryOS 沉淀 **两类数字资产：Graph（流程）+ Experience（判断）**。

**当前在哪**

> **阶段 0（进行中）**：工程底座 + 信任内核骨架（契约、迁移、mock Connector，尚未完成 Graph/Execution 全链路）。

---

## 二、演进总览（老板与技术共用）

### 2.1 阶段地图

```text
阶段 0  工程底座期（当前）     ──► Gate 0：内核可测，不接生产写
   │
阶段 1  业务执行层（D1）       ──► 陀螺匠/灯塔：一条业务链写通、可审计、可回滚
   │
阶段 2  复制与 SaaS 规模化     ──► Pack import：第二家 2～3 周；多 tenant 运营
   │
阶段 3  经验上下文层（D2）     ──► **按岗位**沉淀 Experience：质检/工艺/采购/设备…
   │
阶段 4  决策参考层             ──► Graph+Experience → 模型方案/排序/模拟（人批或 L3 自治）
   │
阶段 5  Factory Brain（终局）  ──► **治理内分级自治工厂**；非无规则 autowrite
   │
愿景    2030+                  ──► Legacy 只读沉淀、区域级 Action Context 标准
```

### 2.2 阶段对照表（一张表看清全局）

| 阶段 | 时间预期 | 对外名称（ChatGPT 融合） | 对内技术名称 | 老板看什么 | 技术验收什么 |
|------|----------|--------------------------|--------------|------------|--------------|
| **0** | 现在～Gate 0 | 筑基 | L1/L2 骨架 | 「能开始接厂了」 | AC-BASE 子集绿 · mock Connector |
| **1** | Gate 0 后～首家 D1 签字 | **Business Execution Layer** | L1 Operational + L2 Execution 闭环 | 「一条链可靠、能 demo、能收费」 | D1-1～D1-5 · Shadow · Package export |
| **2** | D1 后～约 12 月 | **Operating Layer 复制** | Pack Registry + SaaS Pool | 「第二家快、订阅可复制」 | import ≤3 周 · 3～5 tenant |
| **3** | Y2 起 | **Experience Layer** | L3 · **岗位经验网** | 「人走了经验还在」 | Experience Schema · 岗位采集 · Pack |
| **4** | Y3 起 | **Decision Reference** | L4 · 模型参考 Graph+Exp | 「AI 会判、人可批」 | 方案排序 · Rule 引用 Experience |
| **5** | Y4～Y7 | **Factory Brain** | L4 + Agent L3 分级自治 | 「少人指挥、治理内自治」 | 场景白名单 · 全链路 Audit · 可回滚 |
| **愿景** | 2030+ | 自治工厂体系（资本市场） | 全球 Context 标准 | 战略叙事 | 不替代阶段验收 |

---

## 三、四层上下文架构（技术人员总图 · 全阶段共用）

所有阶段共用同一套 **内核不变、Pack 扩展** 的分层；阶段差异在于 **激活哪几层、卖哪几个 Pack**。

```text
┌──────────────────────────────────────────────────────────────┐
│ L4  Decision Context（阶段 4）                                │
│     排产/采购/库存 What-if · 方案对比 · 须主管批准后才写 L0      │
├──────────────────────────────────────────────────────────────┤
│ L3  Experience Context（阶段 3）                                │
│     事件→判断→原因→措施→结果→置信度→适用范围（结构化，非读脑）   │
├──────────────────────────────────────────────────────────────┤
│ L2  Execution Context（阶段 0～1 建满，全程核心）              │
│     DslPlan → Harness → Rule → Execution → Audit → Revert     │
│     → 对账 Job → ExecutionRecord / Evidence                   │
├──────────────────────────────────────────────────────────────┤
│ L1  Operational Context（阶段 0～1 建满，全程核心）            │
│     System Map（Connector/Pack/Edge 能力图）                    │
│     + Business Graph（工作坊 freeze 的业务链路）                │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼ 唯一写路径
                    Legacy ERP/MES（Data-L0 账本 · 权威不变）
```

**ChatGPT 融合命名对照**

| ChatGPT 说法 | 本架构层 | 说明 |
|--------------|----------|------|
| System Graph | **L1 System Map** | 不做「AI 全自动扫全 ERP」；Connector 映射 + 人审 freeze |
| Business Graph | **L1 Business Graph** | 核心资产；工作坊冻结 |
| Business Execution Layer | **L1 + L2** | 阶段 1 主战场 |
| Experience Graph | **L3** | 阶段 3；结构化经验网络 |
| Factory Brain | **阶段 5** | **治理内分级自治**；不是无 Harness 的 wild agent |

---

## 三点五、双资产飞轮（GPT 核心 · 不可只写 Graph）

> **Graph 解决「企业 **怎么操作**」；Experience 解决「企业 **怎么判断**」。两者叠加才是 ChatGPT 说的 Experience Graph + Factory Brain 终局。**

### 3.5.1 两类资产

| 资产 | 沉淀什么 | 来源 | 谁用 |
|------|----------|------|------|
| **Business Graph（L1）** | 冻结的业务 **流程链路**（报工、采购、质检闭环） | 工作坊 + Connector 摸底 + freeze | Execution / Agent 走流程 |
| **Experience Network（L3）** | 冻结的 **判断知识**（为什么、怎么办、适用条件） | **各岗位**在应用端/Harness 闭环中结构化留下 | 模型 **决策参考** · Rule 条件 · 未来 L3 自治 |

### 3.5.2 按岗位沉淀（GPT 明确讲的 · 必须写进路线）

经验 **不是** 一个笼统「知识库」，而是 **按制造角色分域沉淀**：

| 岗位/角色 | 典型经验示例 | 采集触点（应用端） |
|-----------|--------------|-------------------|
| **工人/班长** | 某工序常见误报、噪声环境怎么报工 | 报工 Harness 驳回原因 · 语音/图异常标注 |
| **质检** | 看图判缺陷根因（模具 vs 材料 vs 工艺） | 质检 App/H5 · 偏差处理闭环 |
| **工艺/工程师** | 湿度/温度与变形、刀具寿命 | 工艺参数确认 · NCR 关闭表单 |
| **采购** | 某供应商周五不发货、某物料交期虚标 | 跟单异常 · 到货偏差记录 |
| **设备/维修** | 听音/振动的故障预判 | 维保工单 · 停机原因结构化 |
| **计划/PMC** | 插单优先级、换线代价 | 排产调整 **理由** 必填（非只改数） |

**每条 Experience 标准结构（GPT + 可验收）：**

```text
事件（Event）→ 情境（Context）→ 判断（Judgment）→ 原因（Cause）
  → 措施（Action）→ 结果（Outcome）→ 置信度（Confidence）
  → 适用范围（Scope：产品/工序/供应商/季节…）→ 来源岗位（Role）
  → 关联 exec_id / graph_id（可追溯）
```

**「人走了经验还在」**：指 **L3 条目持久化 + 检索 + 进入后续 Agent/Rule/模型上下文** —— 不是把人聊天贴进向量库就完事。

### 3.5.3 模型如何用经验（GPT：决策参考）

```text
用户/系统事件
    │
    ▼
检索 L1 Graph（能做什么、走哪条流程）
    +
检索 L3 Experience（类似情境下历史判断与措施）
    │
    ▼
LLM/Planner 生成 DslPlan 或 方案列表（带引用：引用了哪条 Experience）
    │
    ▼
Rule Engine（硬约束）+ Harness（人确认 或 Agent L3 白名单自治）
    │
    ▼
Execution → Legacy + Audit（每次决策可追溯到引用的经验条目）
```

**越用越成熟**：Experience 条目随 **Outcome 反馈** 更新置信度；错误判断可 **降级/废止**（append-only Audit，不 silently 改历史）。

### 3.5.4 演进到「无人指挥的工厂体系」（GPT 终局 · 阶段 5）

ChatGPT 的 **Factory Brain / AI Native Factory** 在本路线中 **不删除**，而是 **放在阶段 5**，且定义为：

> **在 Graph 已 freeze、Experience 已积累、Shadow/Revert/对账已证明可靠的场景下，按场景逐步开放 Agent L3（低风险自动执行）与 L4 多步编排自治——不是一步跳到「全厂无人」。**

| 自治等级 | 含义 | 典型场景 | 治理 |
|----------|------|----------|------|
| **L0–L2** | 人主导 | 阶段 1 报工 | Harness 必确认 |
| **L3 场景自治** | 无人指挥 **单场景** 闭环 | 低风险通知、重复报工、标准检验通过 | Rule 白名单 + 全 Audit |
| **L4 编排自治** | 多步 **编排** 自治 | 标准插单、标准催料 | Simulation 前置 + drift 告警 |
| **Factory Brain** | 跨域 **建议+执行**（仍受 Policy） | 日夜班排产/采购联动 | 阶段 5 · Enterprise · 可降级回 L2 |

**与 GPT 一致的一句话**：终局是 **「经验越厚、自治越广、人越少指挥 routine」**；与工程红线一致的一句话：**任何写 Legacy 仍走 execution_service，任何自治场景必须可 Audit、可 Revert、可对账。**

### 3.5.5 当前系统有没有明确规划？（诚实对照 · 消除疑问）

| 能力 | 战略/文档 | 契约/代码 | 阶段 |
|------|-----------|-----------|------|
| Business Graph freeze | ✅ `08` · `contracts` Graph schema | W2+ 实现中 | **1** |
| 受控写路径 Harness/Revert | ✅ REDLINES · ADR-002 | W2+ 实现中 | **1** |
| Agent L0/L1/L2 | ✅ ADR-002 · `cap-*` Pack | Phase 1 | **1** |
| **Experience 条目 Schema** | ✅ **本文 + GPT 融合** | ❌ **尚无 `ExperienceEntry.schema` in contracts** | **3 先设计** |
| **按岗位采集 UX** | ✅ 本文 | ❌ 尚无质检/工艺专用 H5 Pack | **3** |
| **Experience → 模型检索** | ✅ 本文 | ❌ 尚无 RAG/Registry 模块 | **3～4** |
| Agent **L3 低风险自动** | ✅ ADR-002「Phase 2+」 | ❌ 未实现 | **4～5** |
| **Factory Brain 跨域自治** | ✅ GPT · `00` 2030+ 愿景 | ❌ 无模块 | **5** |

**结论**：GPT 讲的 **Experience + 岗位 + 决策参考 + 自治工厂**，在 **战略上必须保留**；在 **工程上阶段 1 只做 Graph+Execution**，Experience/Brain **有路线、尚未落契约** —— 之前融合文档 **写短了、阶段 4 表述偏保守**，容易读成「不做 Brain」，这是 **文档问题，不是战略否定**。

---

## 四、阶段 0 — 工程底座期（**当前阶段**）

### 4.1 本阶段在演进中的位置

- **状态**：**进行中**（W1 基座：契约、Alembic S-01～S-04、mock Connector、边界静态门禁）。  
- **目标**：完成 **Gate 0** —— 信任内核 **可编译、可测试、可迁移**，仍 **不接真实 ERP 生产写**。

### 4.2 解决的 core 问题

| 问题 | 不做的后果 |
|------|------------|
| 没有统一契约与写路径红线 | Agent 直写 ERP，后期无法审计/回滚 |
| 没有 Execution/Audit 骨架 | 「AI 报工」不可信，无法对账 |
| 没有 tenant/Connector 注册预埋 | 第二家复制无从谈起 |

### 4.3 商业价值（老板）

- **本阶段不直接产生 ARR**；价值是 **降低阶段 1 接厂风险与周期**。  
- 可对老板表述：**「我们在建司法级 AI 写库能力，而不是 demo。」**

### 4.4 应用场景

- 无对外生产场景；内部 **CI/AC 绿** = 可启动陀螺匠接入。

### 4.5 项目实现思路（技术人员）

| 工作包 | 内容 | 完成标志 |
|--------|------|----------|
| W1 骨架 | `shared_contracts` · Alembic S-* · mock `connector_sdk` · `/health` | `./scripts/gate step` 相关 AC 绿 |
| W2～W3 | audit + execution + graph freeze + rule_engine 骨架 | pytest AC-BASE 过半 |
| W4～W5 | agent 薄 FSM · DslPlan · OpenAPI 对齐 | import_boundaries 全绿 |
| W6～W8 | 对账 stub · revert 骨架 · **Gate 0 全绿** | AC-BASE-001 全绿 |

**本阶段禁止**：接真实 ERP 生产写 · 钉钉生产发布 · 为多端 App 分散主力。

**真源**：`_factoryos_pipeline/2026-06-25/plan/plan-0116-w1-base.md` · `docs/准备/2026-06-16/14-一年冲刺路线图与并行研发.md` §五。

---

## 五、阶段 1 — 业务执行层（Business Execution Layer）

### 5.1 演进定义

> **让 AI 学会「按企业已冻结的流程」操作 Legacy；人通过确认门负责；每笔写可审计、可对账、可撤回。**

对应 **ChatGPT Stage 1** + 本架构 **L1 + L2 闭环**。

### 5.2 时间边界

- **开始**：Gate 0 全绿之后。  
- **结束**：**D1 书面验收签字**（Shadow ≥14 天 + D1-1～D1-5 全过 + export Package v1）。  
- **首要验证环境**：**陀螺匠 ERP（内部沙箱）** → 再 **灯塔客户/对外 demo**（同一套 D1 标准，不降低验收）。

### 5.3 解决的核心问题

| 制造业通病 | FactoryOS 解法 |
|------------|----------------|
| 软件在「教人学 ERP/MES」 | 自然语言/轻入口 + Graph 替人走流程 |
| 不敢让 AI 写库 | Harness + Rule + 唯一写路径 + Shadow |
| 写错了收不回来 | Revert + before/after 快照 |
| 现场数和账本对不上 | 对账 Job + drift 告警 |
| 每家集成从零开始 | Graph/Rule/Connector **Package 首次 export** |

### 5.4 商业价值（老板）

| 项 | 说明 |
|----|------|
| **可卖 SKU** | Q0 付费 Shadow 试用 · L0 平台订阅 · **L1 D1 通病包**（报工+查询+钉钉/API 入口） |
| **定价逻辑** | 实施费（首次）+ 年费（订阅+审计+对账） |
| **销售故事** | 「不换 ERP，工人说一句话/拍一张就能报工，财务能查、能退、能对账」 |
| **阶段结束标志** | 1 家 **D1 签字** + 可演示 SaaS + **Implementation Package v1** |

### 5.5 应用场景（场景 ID · 需求明确）

| ID | 角色 | 场景 | 典型动词 | 入口 |
|----|------|------|----------|------|
| S-01 | 工人 | 报工 | WORK_REPORT | API / 简易 H5 / 钉钉（按演示裁剪） |
| S-02 | 主管 | 确认/驳回 | APPROVE / REJECT | 待办 / Harness |
| S-03 | 文员/计划 | 查工单/报工历史 | QUERY_WO 等 | 自然语言 / API |
| S-04 | IT/财务 | 审计、对账、撤回 | Audit / Reconcile / REVERT | 管理台 / 导出 |

**本阶段不做**：自动财务过账 · 无确认自主排产写回 · 全厂数仓 · PC/App 齐套（非阻塞项）。

### 5.6 项目实现思路（技术人员）

**接厂顺序（强制）**

```text
Step 1  只读摸底（Connector read · 字段映射 · 样例单据）
Step 2  Graph 工作坊 → freeze（5～8 节点 · 人签字 · checksum）
Step 3  Rule + DSL 绑定 · Harness 确认门
Step 4  Shadow ≥14 天（写操作零生产或 dry_run）
Step 5  小范围 UAT · Revert 演示
Step 6  对账零 drift 或告警闭环
Step 7  D1 验收签字 · export Package v1
```

**陀螺匠路径（Path A 等价）**

| 模块 | 实现要点 |
|------|----------|
| Connector | `conn-erp-*-read/write` 对接陀螺匠 API；私网则 **Edge Agent 出站** |
| Graph | 1 条链：查询工单 → 报工 → 主管确认 → 写回陀螺匠 |
| Execution | 仅 `execution_service` 写 Legacy；ExecutionRecord + Audit |
| 对账 | OS 记录 vs 陀螺匠 read-back |
| 部署 | Core **SaaS 多 tenant**；陀螺匠侧 Connector/Edge |

**D1 五项验收（全部满足才进入阶段 2）**

| ID | 验收要点 |
|----|----------|
| D1-1 | 跨系统只读查询可用 |
| D1-2 | 写仅经 DSL + Rule |
| D1-3 | 每次写有 ExecutionRecord |
| D1-4 | WORK_REPORT_REVERT 可演示 |
| D1-5 | 每日对账零 drift 或自动告警 |

**真源**：`08` §3.2 D1 · `04-工厂实施手册` · `REDLINES` R-01～R-11。

---

## 六、阶段 2 — 复制与 SaaS 规模化（Operating Layer 复制）

### 6.1 演进定义

> **同一条 D1 机制，第二家起以 import Package 为主、工作坊只做差量；SaaS 一套栈服务多 tenant。**

对应 **ChatGPT「Graph 复利 / 第二家像 import」** + 商业 **Land-Expand**。

### 6.2 时间边界

- **开始**：首家 D1 签字 + Package v1 已 export。  
- **目标（强资金节奏）**：12 月内 **3～5 家 tenant**；第二家 D1 **2～3 周**（Silver import）。

### 6.3 解决的核心问题

| 问题 | 解法 |
|------|------|
| 每家项目制、无法指数增长 | Implementation Package import/export |
| 运维随客户线性爆炸 | SaaS Pool + RLS + 统一发版 |
| 私网 ERP 接不进云 | Edge Agent 标准件 |
| 销售说不清「和黑湖/Celonis 差别」 | **Overlay 中立 + Trust Kernel**（不替账本） |

### 6.4 商业价值（老板）

| 项 | 说明 |
|----|------|
| **收入结构** | 复制实施费 ↓ · **订阅占比 ↑** · NRR 目标 **>120%** |
| **单元经济** | **厂 = 增长单元**（非 seat）；第二家边际成本下降 |
| **竞争话术** | 「第一家考古，第二家 import」 |
| **里程碑** | 3～5 tenant · 订阅占比 ≥50% · Studio MVP 可演示 |

### 6.5 应用场景

- **与阶段 1 相同 S-01～S-04**，换 tenant ERP 厂商/字段 **Override**，**不换内核**。  
- 新增：**Integration Studio** discover/map/prove（实施与 IT 配 Connector，非工人主路径）。

### 6.6 项目实现思路（技术人员）

| 工作包 | 内容 | 验收 |
|--------|------|------|
| Pack Registry | export/import JSON · tenant Override | 第二家 import 2～3 周结案 |
| SaaS Pool | 单 VPC · RDS · `tenant_id` + RLS | 多 tenant 隔离测试通过 |
| Edge Agent | 私网 ERP 出站 WSS | 至少 1 家私网厂 PoC |
| MCP Gateway | 内部 GA；tools/list · tools/call → DslPlan | 禁直写 Legacy |
| web-admin / Studio | Pack · Connector 状态 · Edge 在线 | OpenAPI v1.1.1 域 |

**禁止**：内核 `if tenant_id == xxx` · 未经 ADR 改 Layer 0 写路径。

---

## 七、阶段 3 — 经验上下文层（Experience Layer · **按岗位沉淀**）

### 7.1 演进定义

> **在 Execution 可靠后，从质检、工艺、采购、设备、计划等各岗位的应用端交互中，结构化沉淀 Experience；形成「人走了经验还在」的企业判断网络。**

对应 **ChatGPT Stage 2「Experience Graph / 理解企业」** —— **本阶段是 GPT 路线里 Graph 之外的第二条主轨，不是可有可无的附录。**

### 7.2 时间边界

- **开始**：阶段 2 稳定 · 至少 **3 家 D1** · NRR 健康。  
- **典型**：Y2 起。  
- **工程前置（阶段 2 末可启动）**：`ExperienceEntry` JSON Schema 入 `contracts/` · 岗位采集 UX 原型。

### 7.3 解决的核心问题

| 问题 | 解法 |
|------|------|
| ERP 只有「发生过什么」，没有「为什么」 | L3 条目挂 Event/Judgment/Cause/Action |
| 老师傅/质检员退休经验流失 | **按 Role 分域** 持久化 + 检索 |
| 模型只会操作不会判断 | Experience 进入 Planner 上下文（阶段 4） |
| 定制项目拖垮毛利 | ≥70% D2 入库为 Pack（`skill-experience-*`） |

### 7.4 商业价值（老板）

| 项 | 说明 |
|----|------|
| **SKU** | 岗位经验 Pack：质检/工艺/采购/设备… |
| **故事** | **「人走了经验还在」** —— 可单独对客户讲 |
| **ARPU** | L1 之上 +30%～80%；经验越厚续费越稳 |
| **壁垒** | 竞品 Overlay 多只有流程；**流程+判断双资产** |

### 7.5 应用场景（岗位 × 场景）

| 岗位 Pack | 场景 | 采集方式 |
|-----------|------|----------|
| `exp-quality-inspector` | 缺陷判因、8D 前置 | 质检 H5 关闭工单必填判断链 |
| `exp-process-engineer` | 参数/变形/刀具 | 工艺确认 Harness |
| `exp-purchaser` | 供应商/交期陷阱 | 到货异常结构化 |
| `exp-maintenance` | 停机/听音预判 | 维保工单 |
| `exp-planner` | 插单代价、换线 | 计划调整「理由码」 |

### 7.6 项目实现思路（技术人员）

| 项 | 要求 |
|----|------|
| **Schema** | 新增 `ExperienceEntry.schema.json` · Role enum · link `exec_id` |
| **存储** | tenant 隔离 · append 为主 · 废止=新条目标记 supersede |
| **采集** | 各岗位 Pack 的 Harness **扩展字段**（非自由聊天入库） |
| **Agent** | L1 建议时 **cite** 引用了哪条 Experience |
| **验收** | AC-EXP-001：录入→检索→被 Agent 引用→Audit 可追溯 |

---

## 八、阶段 4 — 决策参考层（Graph + Experience → 模型决策）

### 8.1 演进定义

> **Planner/LLM 同时读取 frozen Graph 与 L3 Experience，输出方案、排序、风险说明；默认人工批准写回；高置信场景试点 Agent L1→L3。**

对应 GPT：**模型不再只「替人按键」，而是「替人参考经验做判断」** —— 仍是 **Reference，不是 wild autowrite**。

### 8.2 时间边界

- **开始**：Y3+ · 至少 **1 万条级** 有效 Experience（单 tenant 或行业 Pack）  
- **依赖**：阶段 3 Schema 稳定 · Rule 可引用 Experience 条件

### 8.3 解决的核心问题

| 问题 | 解法 |
|------|------|
| 排产/采购靠人脑综合 | 多方案 + 每条方案 **引用 Experience ID** |
| 模型胡编 | Graph 约束动作空间 · Experience 约束判断 · Rule 硬 deny |
| 责任不清 | Decision trace 写入 Audit + Evidence |

### 8.4 商业价值（老板）

| 项 | 说明 |
|----|------|
| **SKU** | 决策辅助模块 · 排产/采购/质量 Copilot |
| **差异化** | **「带企业经验的 AI 判断」**，不是通用大模型 |
| **试点** | 单场景 L3 自治可 **单独收费** |

### 8.5 项目实现思路（技术人员）

| 项 | 要求 |
|----|------|
| Planner | Graph 合法动词集 + Experience 检索 top-k |
| 输出 | DslPlan 候选列表 + `cited_experience_ids[]` |
| Rule | 可配置「当 Experience 置信度≥θ 且场景∈白名单 → 允许 L3」 |
| 模拟 | dry_run / Shadow 必过再开 L3（ADR-002） |

---

## 九、阶段 5 — Factory Brain（治理内分级自治工厂 · **GPT 终局**）

### 9.1 演进定义

> **Experience 与 Graph 足够厚、对账与 Revert 长期零重大事故后，在 **Policy 圈定的域** 内实现「无人指挥」的 routine 自治；人退到异常与战略层。**

**这就是 GPT 说的「直到演化到无人指挥也能自动决策的工厂体系」在本项目中的正式位置** —— **不是不做，是阶段 5，且必须治理内生长。**

### 9.2 与 GPT 原文对齐

| GPT 表述 | 本阶段落地 |
|----------|------------|
| Factory Brain 推理排产/采购/物流 | 跨 Graph 编排 + L4 Planner |
| AI 员工（每岗位 Agent） | **Role Pack Agent** + L3 自治白名单 |
| 经验越成熟越自动 | Experience 置信度 → 逐步放宽 Harness |
| 企业认知系统 | **Graph + Experience 双注册表** |

### 9.3 自治边界（必须写进合同 · 消除「会不会乱写」）

**允许自治（示例，逐场景开）：**

- 标准报工、标准检验通过、标准催料提醒、标准库存查询触发补货 **建议**

**禁止自治（永远 Harness 或人）：**

- 财务过账、付款、成本结转、无确认库存调整、未授权 DSL（REDLINES 首期禁止类）

**任何自治写 Legacy：**

```text
仍仅 execution_service · 仍 Audit · 仍可对账 · 仍 Compensator
```

### 9.4 商业价值（老板 · 百亿叙事支点）

| 项 | 说明 |
|----|------|
| **品类** | **Governed Autonomous Factory** —— 比「AI ERP」准确 |
| **定价** | Enterprise · 按场景自治模块 · 按厂/按 Cell 计量 |
| **资本市场** | Graph+Experience 网络效应 · 经验越厚迁移成本越高 |

### 9.5 项目实现思路（技术人员）

| 项 | 要求 |
|----|------|
| Policy Engine | 场景 × Role × Agent Level × Experience 置信度 矩阵 |
| Orchestrator | 多 Agent 编排（LangGraph）· 状态机 · 超时/熔断 |
| 降级 | drift / 对账失败 → **自动降回 L2 人工确认** |
| 验收 | 7×24 Shadow 对比人工决策 · 书面自治开通签字 |

---

## 十、愿景层（2030+）

> **Legacy 逐步成为只读分析源；FactoryOS 成为工厂操作与上下文入口；可选 Layer 3 数仓/看板单独立项。**

- **仅用于**：融资/战略 PPT **最后一页**。  
- **不写入**：阶段 0～4 WBS · 合同默认范围 · 研发计划节点。

ChatGPT「ERP 时代结束 / Foundation Model」**仅放愿景页**，**不作为产品口号**。

---

## 十一、商业与部署（全阶段共用规则）

### 11.1 收入四层（与阶段对应）

| 层 | 名称 | 主要对应阶段 |
|----|------|--------------|
| L0 | 平台订阅（SaaS · 审计 · 对账 · tenant） | 1～ |
| L1 | D1 通病包 | 1 |
| L2 | 扩展 Pack（**含岗位 Experience**） | 3～5 |
| L3 | Override / 实施人天（≤30% 收入） | 1～2 |

### 11.2 部署默认

| 形态 | 何时 |
|------|------|
| **SaaS 多 tenant（Pool）** | 默认 · 阶段 1 起 |
| **Edge Agent** | 客户 ERP 私网 · 阶段 1～2 |
| **专属实例 / 私有化** | Enterprise · 阶段 4 或大单 |

### 11.3 数据边界（全阶段不变）

```text
Data-L0  账本 → 永远在客户 ERP/MES（FactoryOS 不默认托管全量业务库）
Data-L1  运行 → Graph · Audit · Execution · **Experience（阶段 3 起）** · 对账（必做）
Data-L2  缓存 → 最小字段 · TTL（按需）
Data-L3  数仓/分析 → 选配 · 单独合同
```

---

## 十二、不变红线（全阶段 · 技术/商务共同遵守）

| ID | 红线 |
|----|------|
| R-01 | Agent **禁止**直写 Legacy |
| R-03 | Graph 未 freeze **禁止** L2 写 |
| R-07 | Shadow/dry_run **先于**生产写 |
| R-09 | **禁止** AI 自动 freeze Graph |
| 架构 | integration **禁止** import os_core 私有 API |
| 商业 | **禁止** 默认承诺全厂数据上云/替代 ERP |

完整表：`.cursor/factoryos/REDLINES.md`

---

## 十三、大模型与技术演进（全阶段策略）

| 趋势 | FactoryOS 做法 |
|------|----------------|
| MCP 成标准 | `mcp_gateway` · Connector 动词稳定注册 |
| SLM 降本 | 意图/填槽/分类用中小模型 · LiteLLM 路由 |
| 治理瓶颈 | **Trust Kernel 产品化** = 护城河 |
| Context Layer 独立 | **L1 Graph + System Map** = 运营上下文 |
| Agent 41% 投产 | Shadow + Harness + AC 负向测试 |

**ChatGPT「Graph 随模型升级仍可用」→ 工程上 Graph/Rule freeze + Pack 版本化，LLM 仅换 endpoint。**

---

## 十四、里程碑速查（消除「我们现在到哪」的疑问）

| 里程碑 | 阶段 | 老板理解 | 技术 Gate |
|--------|------|----------|-----------|
| Gate 0 | 0 | 底座就绪 | AC-BASE-001 全绿 |
| 陀螺匠内部 D1 等价 | 1 | 机制在真 ERP 上成立 | D1-1～5 + Shadow 报告 |
| 对外 D1 签字 | 1 | 可收费、可案例 | 书面验收 + Package v1 |
| 第二家 import | 2 | 复制飞轮启动 | ≤3 周 + import 测试 |
| 3～5 tenant | 2 | 初具规模 | 多 tenant 生产稳定 |
| 首个岗位 Experience Pack（如质检） | 3 | 人走了经验还在 | AC-EXP-001 |
| 决策引用 Experience 上线 | 4 | AI 会判 | cited_experience in Audit |
| 首场景 L3 自治开通 | 5 | 少人指挥 | 自治 Policy 签字 |
| Factory Brain Enterprise | 5 | 百亿叙事 | 7×24 对账 + 降级 proven |

---

## 十五、给老板 vs 给技术（各读哪几节）

| 读者 | 必读 | 可选 |
|------|------|------|
| **老板** | 一 · 二 · **§3.5 双资产** · 五～九 · 十一 · 十四 | 十愿景 |
| **技术负责人** | 三 · **3.5** · 四～九 · 十二 · 十三 | 十一部署 |
| **研发成员** | 四～五（当前）· 十一红线 · `contracts/` | 阶段 6～8 预习 |

---

## 十六、文档关系（避免「听谁的」）

| 文档 | 作用 |
|------|------|
| **本文** | 演进思路融合版 · 老板+技术对齐 |
| `contracts/` + ADR | **编码与验收真源** |
| `08-平台战略与两次交付模型` | D1/D2 交付细节 |
| `14-一年冲刺路线图` | 周级任务（Gate 0 / 灯塔） |
| ChatGPT 对话 | **战略叙事来源** · 已过滤不可落地项 |

**冲突时**：REDLINES > contracts > 本文 > ChatGPT 原文。

---

## 十七、融合结论（为何这份文档合理）

1. **GPT 双轨完整保留**：**Graph（流程）+ Experience（岗位判断）+ 模型决策参考 + Factory Brain 终局**。  
2. **不是不做自治工厂**：放在 **阶段 5**，且 **治理内分级开放**，与 REDLINES 不矛盾。  
3. **当前工程诚实**：阶段 0～1 做 Graph/Execution；**Experience Schema 阶段 2 末设计、阶段 3 实现** —— 见 §3.5.5。  
4. **之前文档问题**：阶段 4 写「不是 Factory Brain」易误解为 **否定终局**；已改为 **阶段 4=决策参考、阶段 5=Brain**。

**定稿口径（可原句用于汇报）**

> 我们不止沉淀 Graph，还要 **按质检、工艺、采购等岗位沉淀 Experience，让模型在 Graph+Experience 上做决策参考**；经验越厚，在治理框架内 **逐步减少指挥、演进到 Factory Brain**。阶段 1 先把写路径做可靠，**不等于放弃 GPT 说的终局。**
