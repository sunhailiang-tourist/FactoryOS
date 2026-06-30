# FactoryOS 宏观演进策略（GPT × 顶级产业策略 · 融合版）

> **版本**：v1.0.0 · **日期**：2026-06-25  
> **文档性质**：**宏观战略** — 回答「我们往哪演化、每演化一段卖什么、壁垒是什么」  
> **不是**：W1/Gate 0/D1 验收、周计划、模块清单（那些见 `FactoryOS-系统演进思路-融合版.md` 与 `contracts/`）  
> **读者**：老板 · 投资人 · 技术负责人（战略对齐用）

---

## 一、30 秒：宏观 vs 微观

| | **宏观（本文）** | **微观（另一份文档）** |
|---|------------------|------------------------|
| **问什么** | 五年/十年我们成为什么品类？ | 本季度写什么代码、怎么验收？ |
| **阶段单位** | 产业能力跃迁（操作→理解→决策→自治） | 工程里程碑（Gate 0、D1、Pack import） |
| **GPT 关系** | **与 GPT 六层/三阶段同高度** | 把宏观 **落地** 到陀螺匠/灯塔/SaaS |

**GPT 的演进 = 宏观策略；你要的是把 GPT 宏观线 + 产业顶级策略（Celonis Context、Trust、Pack 飞轮、SaaS 规模化、百亿路径）合成一条，而不是再讲一遍现有 plan。**

---

## 二、战略总判断（融合后的品类定义）

### 2.1 我们不是什么

- 不是 AI ERP · 不是聊天 Copilot · 不是替客户建数仓 · 不是无治理的 Agent 平台

### 2.2 我们是什么（GPT + 产业共识融合）

> **FactoryOS = 制造业「受治理的企业行动上下文平台」（Governed Enterprise Action Context Platform）**

| 来源 | 贡献 |
|------|------|
| **GPT** | 企业认知系统 · Graph 网络 · 操作→理解→经营 · Factory Brain 终局 |
| **Celonis 2026** | **Context Layer** — Enterprise AI 的操作上下文层 |
| **QAD/Gartner** | System of Record → **System of Action** |
| **DronaHQ/Tulip** | ERP/MES **之上** 的 Agentic Workflow，Legacy 不动 |
| **黑湖（反面参照）** | 中国制造可规模化，但我们是 **Overlay+治理**，不是自建账本+高自主豪赌 |
| **2026 LLM 趋势** | MCP 连接 · SLM 执行 · **治理才是产品**（80% 试 Agent，41% 真投产） |

### 2.3 双资产终局（GPT 核心 · 不可只讲 Graph）

```text
Operational Graph（流程资产）     — AI 学会「企业怎么运转、怎么操作」
Experience Graph（经验资产）     — AI 学会「企业怎么判断、为什么这样做」
         ↓ 融合 + 持续学习
Factory Brain（治理内自治工厂） — AI 在目标与 Policy 内「替企业行动」
```

**壁垒公式（GPT + 顶级策略一致）：**

> **Graph + Experience 沉淀 + 持续学习 + 受治理写路径**  
> **≠ 单一模型 · ≠ Prompt · ≠ 项目制集成**

---

## 三、宏观演进总图（一条线看懂）

```text
宏观Ⅰ  操作时代          GPT：学会操作企业（System + Business · Execution Layer）
       │                 产业：Context + Action 入口 · Trust Kernel
       ▼
宏观Ⅱ  理解时代          GPT：学会理解企业（Experience + Knowledge）
       │                 产业：人走经验在 · 岗位经验网 · Pack 复利
       ▼
宏观Ⅲ  决策时代          GPT：学会权衡企业（Decision Graph）
       │                 产业：Graph+Experience 驱动 Planner · 方案而非 autowrite
       ▼
宏观Ⅳ  自治时代          GPT：Factory Brain + Enterprise AI OS + 数字员工
       │                 产业：治理内分级自治 · 管理者只批目标/异常
       ▼
宏观Ⅴ  网络时代          GPT：Learning Graph + Industrial Context 标准
                         产业：跨厂模式迁移 · 平台网络效应 · 百亿/千亿叙事
```

**与 GPT 三句话对齐：**

| GPT 三阶段 | 本宏观阶段 |
|------------|------------|
| 让 AI 学会 **操作** 企业 | **宏观Ⅰ** |
| 让 AI 学会 **理解** 企业 | **宏观Ⅱ** |
| 让 AI 学会 **经营** 企业 | **宏观Ⅲ + Ⅳ** |
| （GPT 第七层 Learning） | **宏观Ⅴ** |

**与 GPT 六层 Graph 塔对齐：**

```text
宏观Ⅰ  ← System Graph + Business Graph + Execution
宏观Ⅱ  ← Experience Graph + Knowledge Graph
宏观Ⅲ  ← Decision Graph
宏观Ⅳ  ← Factory Brain（融合 System/Business/Knowledge/Experience/Decision）
宏观Ⅴ  ← Learning Graph + Foundation / World Model 叙事
```

---

## 四、宏观Ⅰ — 操作时代（Operation Era）

> **GPT：第一阶段 — 让 AI 学会操作企业（Business Execution Layer）**  
> **产业命题：软件在「教人」，我们要「让 AI 学软件、人不用学软件」。**

### 4.1 这一时代的核心问题

- ERP/MES/OA 孤岛 · 培训成本爆炸 · 人在系统间搬数据  
- Enterprise AI 有 **Context 盲区**（Celonis 2026）— 模型不懂企业真实怎么写、怎么批  
- Agent 普及但 **不可信** — 缺 Shadow、Revert、对账

### 4.2 这一时代沉淀的核心资产

| 资产 | GPT 名称 | 内涵 |
|------|----------|------|
| **系统能力图** | System Graph | Legacy 能读什么、能写什么（非「全自动扫全库」，而是 **可连接、可映射、可扩展**） |
| **业务流程图** | Business Graph | 冻结的企业链路（报工、查询、确认…）— **GPT：真正资产，不是 LLM** |
| **信任执行链** | Execution Layer | Intent → Graph → Rule → Harness → 写 Legacy → Audit/Revert/对账 |

### 4.3 商业形态与价值

| 维度 | 内容 |
|------|------|
| **品类** | AI Overlay 运行层 · 受治理的 System of Action |
| **卖什么** | 平台订阅 + D1 通病包（报工/查询/确认）+ 实施（首家） |
| **部署** | **SaaS 多 tenant 默认** + Edge 接私网 ERP |
| **客户价值** | 不换 ERP · 现场一句话/轻入口 · IT 能审计能退能對账 |
| **ARR 量级** | 单厂 8～30 万/年 · 首家考古 · **验证 PMF** |

### 4.4 竞争位势（为何能赢）

| 竞品 | 他们强 | 我们这一时代的差分 |
|------|--------|-------------------|
| Celonis | Context + 流程挖掘 | 我们 **自带受治理写回 + 制造现场入口** |
| DronaHQ | Agentic on ERP | 我们 **Graph freeze + Revert + 对账闭环** |
| 黑湖 | 中国工厂规模化 | 我们 **不替账本 · 中立 Overlay · 信任司法链** |
| 通用 Agent | 聪明 | 我们 **可验收、可签单、可追责** |

### 4.5 典型应用场景（宏观）

- 工人/主管：**自然语言 + 多模态** 完成 governed 报工与查询  
- IT/财务：**每笔写可追溯、可对账、可撤回**  
- 实施：**Graph 工作坊 freeze → 导出 Package**（为宏观Ⅱ 复制埋伏笔）

### 4.6 宏观阶段结束标志（战略意义，非工程 AC）

> **「在至少一个细分行业，FactoryOS 被认可为 Legacy 之上唯一可信的 AI 操作入口。」**

*微观落地：Gate 0 → 陀螺匠/灯塔 D1 → Package v1 — 见微观文档。*

---

## 五、宏观Ⅱ — 理解时代（Comprehension Era）

> **GPT：第二阶段 — 让 AI 学会理解企业（Experience Graph · 你战略里「缺失的关键一块」）**  
> **产业命题：ERP 只有「发生过什么」，没有「为什么」— 隐性经验是人走即失的最大成本。**

### 5.1 这一时代的核心问题

- 老师傅、质检、采购、工艺、设备、计划的判断 **不在系统里**  
- 仅 Business Graph → AI 只会 **按键**，不会 **判**  
- 黑湖等走「Agent 替人决策」，但 **经验从哪来、错了谁负责** 说不清

### 5.2 这一时代沉淀的核心资产

| 资产 | GPT 名称 | 内涵 |
|------|----------|------|
| **经验网络** | **Experience Graph** | 按 **岗位/角色** 结构化：事件→判断→原因→措施→结果→置信度→适用范围 |
| **规则图谱** | Knowledge Graph | 外部知识：标准、SOP、制度、设备手册 — **与 Experience 分立** |
| **岗位 Pack** | Role Experience Pack | 质检/工艺/采购/设备/计划… **可售卖、可 import 的经验模块** |

**GPT 金句在本阶段的地位：**

> **「人走了，经验还在。」**  
> Experience **不是知识库，是经验图谱。**

### 5.3 经验从哪来（GPT 明确 · 宏观设计）

- **应用端角色交互中沉淀** — 质检闭环、偏差处理、计划调整理由、Harness 扩展字段  
- **与 Execution 挂钩** — 每条经验可关联 `exec_id` / 业务情境  
- **持续更新** — 结果反馈修正置信度；错误经验可废止（Audit 留痕）

### 5.4 商业形态与价值

| 维度 | 内容 |
|------|------|
| **品类跃迁** | 从「AI 操作层」→ **「AI 操作 + 判断参考层」** |
| **卖什么** | L2 岗位经验 Pack · 行业经验包 · ARPU **+30%～80%** |
| **飞轮** | 宏观Ⅰ 的 Graph 复制 + **经验 Pack 叠加** → NRR **>120%** |
| **壁垒** | 竞品多只有流程；**流程 + 判断双资产** 迁移成本指数上升 |

### 5.5 竞争位势

- **vs 黑湖工业 Agent**：他们推 **决策 Agent**；我们推 **先沉淀 Experience 再放开自治** — 更可持续、更可审计  
- **vs 企业知识库/RAG**：我们是 **结构化经验图谱 + 岗位域 + 与 Graph 联动**，不是文档堆  

### 5.6 典型应用场景（宏观）

- 质检：看图判因 → 沉淀 → 下次类似缺陷 **自动引用**  
- 采购：供应商/交期陷阱 → 提醒 → 采购决策 **带经验 cite**  
- 工艺：湿度/变形关联 → 全产品线 **条件提醒**

### 5.7 宏观阶段结束标志

> **「客户明确为 Experience Pack 付费，且经验条目被 Agent/Rule 稳定引用。」**

---

## 六、宏观Ⅲ — 决策时代（Decision Era）

> **GPT：Decision Graph — AI 开始「思考、权衡」，不是只执行**  
> **产业命题：从 alerting 到 acting — 但制造承担不起无治理的 autowrite（2026 行业共识）。**

### 6.1 这一时代的核心问题

- 排产/采购/插单/多目标优化 — 人脑跨 ERP/MES/库存/交期 **算不过来**  
- 模型能生成方案，但 **无 Graph 约束会胡写、无 Experience 会胡判**  
- Celonis + Ikigai 方向：**决策智能 + 模拟** — 但缺 **受治理写回制造现场**

### 6.2 这一时代沉淀的核心资产

| 资产 | GPT 名称 | 内涵 |
|------|----------|------|
| **策略图谱** | Decision Graph | 多方案 · 收益/风险/交期/成本 **权衡结构** — 存「策略」不存「按钮」 |
| **决策上下文** | Graph + Experience + Knowledge **联合检索** | Planner 输出 **带引用** 的方案列表 |
| **决策痕迹** | Decision Trace | 选了哪方案、引用了哪条 Experience、谁批准 — **合规资产** |

### 6.3 模型如何用经验（GPT · 本阶段核心机制）

```text
情境输入
  → 检索 Business Graph（能做什么）
  → 检索 Experience + Knowledge（类似情境下历史判断）
  → LLM/Planner 生成多方案 + cited_experience_ids
  → Rule 硬约束 + Harness 人批（或 Policy 允许的高置信 L3）
  → Execution 写 Legacy
  → Outcome 反馈 → 更新 Experience 置信度
```

**越用越成熟**：本阶段开始 **经验厚度 → 决策质量 → 客户粘性** 的正循环。

### 6.4 商业形态与价值

| 维度 | 内容 |
|------|------|
| **品类** | **Decision Intelligence on Action Context** — Celonis 类决策 + Tulip 类执行 的 **合体** |
| **卖什么** | 排产/采购/质量 **决策辅助模块** · Enterprise Copilot · 按场景计量 |
| **客单价** | 集团/上市制造 **百万级年费** 可能 |
| **差异化** | **「带企业经验的 AI 判断」** — 不是通用大模型 |

### 6.5 竞争位势

- **vs Celonis**：他们有 Context + Orchestration + Ikigai 收购；我们有 **制造现场写路径 + Experience 岗位沉淀 + 中国供应链深度**  
- **vs 纯 BI/APS**：我们 **决策→执行→对账** 闭环，不是报表  

### 6.6 宏观阶段结束标志

> **「关键业务场景（如插单排产）由 AI 出多方案，人/Policy 选一，全链路可追溯。」**

---

## 七、宏观Ⅳ — 自治时代（Autonomy Era）

> **GPT：第三阶段 — 让 AI 学会经营企业 · Factory Brain · Enterprise AI OS · 全岗位 Digital Employee**  
> **产业命题：2030 AI Native Factory — 管理者只批目标与异常，routine 由 AI 自治。**

### 7.1 这一时代的核心问题

- 人工指挥 routine（报工、标准催料、标准检验、重复跟单）**成本仍高**  
- 宏观Ⅰ～Ⅲ 已证明：**写路径可信、经验够厚、决策可追溯** — 才配谈自治  
- 行业需要的是 **bounded autonomy（有界自治）**，不是 wild agent

### 7.2 这一时代的系统形态（GPT 2030 五层 · 融合）

| GPT 层 | FactoryOS 宏观含义 |
|--------|-------------------|
| **AI 员工** | 每岗位 Role Agent（采购/PMC/工艺/品质/设备…） |
| **Enterprise AI OS** | FactoryOS = 统一调度 · 人→AI→Legacy |
| **Factory Brain** | 跨域 Planner：目标→拆解→多 Agent 编排→执行 |
| **Digital Twin** | 模拟/What-if（选配 · 与 Decision 联动） |
| **World Model / Foundation** | 资本市场叙事 · 非近期工程承诺 |

**GPT 终局 ASCII（宏观目标态）：**

```text
CEO（目标/异常）
    ↓
Factory Brain
    ↓
岗位 Agent 群
    ↓
Enterprise AI OS（FactoryOS）
    ↓
ERP / MES / WMS / SCADA / IoT …
```

### 7.3 自治如何与「受治理」共存（顶级策略约束 · 非 GPT 原话但必须写清）

| 原则 | 含义 |
|------|------|
| **Policy 圈定** | 只有白名单场景可 L3 自治（标准报工、标准通过、标准通知…） |
| **永远 execution_service 写 Legacy** | 自治 ≠ 绕过内核 |
| **永远 Audit + 可对账 + 可 Revert** | 自治 ≠ 无证据 |
| **drift → 自动降级 L2** | 对账失败则收回人工确认 |
| **财务/过账/无确认库存** | **永不自治**（红线） |

**GPT「无人指挥的工厂」在本战略中的定义：**

> **不是无规则 autowrite，而是 Experience 足够厚 + Policy 足够清晰后，routine 域内不再需要人工逐步指挥。**

### 7.4 商业形态与价值

| 维度 | 内容 |
|------|------|
| **品类** | **Governed Autonomous Factory Platform** |
| **卖什么** | Enterprise · 按场景自治模块 · 按厂/Cell 计量 · 私有化溢价 |
| **ARR 跃迁** | 从「操作订阅」→ **「自治能力订阅」** |
| **资本市场** | **百亿叙事支点**：Graph+Experience 网络 + 治理内自治 **品类唯一性** |

### 7.5 宏观阶段结束标志

> **「客户在 Policy 书面开通下，至少 1 个 routine 场景 7×24 自治运行，且对账/Revert 长期无重大事故。」**

---

## 八、宏观Ⅴ — 网络时代（Network Era）

> **GPT：Learning Graph + Industrial Foundation Model · 工业知识跨企业复用**  
> **产业命题：从「单厂智能」到「行业上下文标准 + 平台网络效应」。**

### 8.1 这一时代的核心问题

- 单厂经验 **无法跨厂复利** → 实施仍贵  
- 哪类决策模式可迁移？哪些经验被证伪？ — 需要 **Learning Graph**  
- GPT 与产业共识：**模型 commoditize，平台与行业资产升值**

### 8.2 这一时代沉淀的核心资产

| 资产 | GPT 名称 | 内涵 |
|------|----------|------|
| **学习图谱** | Learning Graph | 方案成功率 · 审批修改模式 · 经验证伪 · **跨厂可迁移模式** |
| **Pack 网络** | Industry Pack Registry | 认证 Connector · 行业 Graph · 行业 Experience · **ISV/渠道分发** |
| **上下文标准** | Manufacturing Action Context Standard | FactoryOS 成为 **区域/行业默认 Context Layer**（类比 Celonis 在流程智能的地位） |

### 8.3 商业形态与价值（百亿 / 千亿叙事）

| 维度 | 内容 |
|------|------|
| **收入** | 平台抽成 · Pack 市场 · Enterprise · 国际化（东南亚/拉美制造带） |
| **ARR 量级** | **10 亿→100 亿** 需：**万级厂 × ARPU × NRR × Pack 网络** |
| **估值逻辑** | Context + Action + Experience **三重复利** · land-expand **厂=单元** · NRR 125%+ |

**GPT 选的三个百亿方向 — 我们的落点：**

1. **Enterprise AI OS** → 宏观Ⅰ～Ⅳ 已做  
2. **Industrial Agent Platform** → 宏观Ⅳ Role Agent + Pack  
3. **Foundation Model + 工业知识库** → **宏观Ⅴ 叙事/partnership**，非自建万亿参数

### 8.4 宏观阶段结束标志

> **「第二家同细分厂主要依赖 import 行业 Pack + 经验，而非从零集成。」**

---

## 九、宏观阶段 × 商业 × GPT Graph 对照总表

| 宏观阶段 | GPT 三阶段 | GPT Graph 层 | 核心资产 | 商业主轴 | 竞争一句话 |
|----------|------------|--------------|----------|----------|------------|
| **Ⅰ 操作** | 学会操作 | System + Business + Execution | 流程图 + 信任写 | Overlay 订阅 + D1 | 唯一可信 AI 写入口 |
| **Ⅱ 理解** | 学会理解 | Experience + Knowledge | **岗位经验网** | 经验 Pack · NRR | 人走经验在 |
| **Ⅲ 决策** | （权衡） | Decision | 方案 + cite | 决策模块 · Enterprise | 带企业经验的 AI 判 |
| **Ⅳ 自治** | 学会经营 | Factory Brain + AI OS | Policy 内自治 | 自治模块 · 大单 | Governed Autonomous Factory |
| **Ⅴ 网络** | 持续学习 | Learning + 标准 | Pack 网络 | 平台 · 国际化 | 行业 Context 标准 |

---

## 十、价值四层论（GPT × 产业 · 指导投资优先级）

| 层 | 内容 | FactoryOS 押注 |
|----|------|----------------|
| L1 模型 | 越来越便宜 | **不押** · LiteLLM 可换 |
| L2 流水线 | Agent+Graph+Execution+反馈 | **宏观Ⅰ 起押** |
| L3 行业资产 | Graph + **Experience** + Pack | **宏观Ⅱ 起押 · 主壁垒** |
| L4 IP/标准 | 平台标准 · 跨厂网络 | **宏观Ⅴ 叙事** |

---

## 十一、与微观规划的关系（避免混读）

```text
宏观Ⅰ  ←→  微观：Gate 0 · 陀螺匠/灯塔 D1 · SaaS · Trust Kernel 工程化
宏观Ⅱ  ←→  微观：ExperienceEntry Schema · 岗位 Pack · AC-EXP
宏观Ⅲ  ←→  微观：Planner cite · Decision trace · Rule+Experience
宏观Ⅳ  ←→  微观：Agent L3 Policy · 多 Agent 编排 · 自治开通流程
宏观Ⅴ  ←→  微观：Pack Registry 生态 · 国际化 Connector · Learning 作业
```

**读法：**

- **老板/投资人/战略会** → **只读本文**  
- **研发排期/验收** → 宏观阶段对齐后，看微观文档 + `contracts/`

---

## 十二、定稿口径（宏观 · 可直接汇报）

> **FactoryOS 的宏观路线，与 GPT 演进同构：先让 AI 在受治理前提下学会操作企业（Graph+Execution），再按岗位沉淀 Experience 让「人走了经验还在」，再让模型在 Graph+Experience 上做决策参考，最终在 Policy 内演进到 Factory Brain 与 Enterprise AI OS，形成可复制的 Pack 网络与行业 Context 标准。**  
> **我们不是重做 ERP，而是在 Legacy 之上，用 Trust Kernel + 双资产 Graph 网络，走一条比「纯 Agent」可信、比「纯 Celonis」能执行、比「黑湖式自治」可审计的制造业 AI 操作系统之路。**

---

## 十三、文档索引

| 文档 | 层级 |
|------|------|
| **本文** | **宏观演进策略（GPT × 顶级产业融合）** |
| `FactoryOS-系统演进思路-融合版.md` | 微观：阶段 0～5 · D1 · 陀螺匠 · 工程 Gate |
| `08-平台战略与两次交付模型.md` | D1/D2 交付 · 飞轮 |
| `contracts/` · `REDLINES.md` | 编码真源 |
