# FactoryOS 创建期对话归档 · 全量行为可追踪链路

> **文档类型**：AI 可读 · 项目创建史 · 决议与行为快照  
> **归档日期**：2026-06-24  
> **覆盖范围**：Cursor Agent 会话 `58e262bf-3054-4647-855a-8bdae148d923`（通读 1427 行 transcript · **243 条用户指令** · 无抽检）  
> **截至状态**：开发前脚手架与治理体系已就绪；**业务代码约 0%**（`src/os_core/__init__.py` 占位）；`gate pr` 本地可绿；分支 `dev_sunhailiang_260624` 已与 origin 同步  
> **用法**：新会话 `@` 本文件 + `.cursor/factoryos/INDEX.md` → 勿重复争论已 **[✅ 已确认]** 决议

---

## 0. 元信息 · 给未来 AI 的阅读协议

### 0.1 本项目创建期在做什么

在 **写 FactoryOS 业务代码之前**，用 AI Coding 完成：

- 产品方向与商业策略文档化（Overlay、两次交付、数字飞轮）
- OS 内核（`os_core`）架构与 ADR 体系
- 契约层（`contracts/`）与验收（AC）
- 研发治理：**SH-步步流** + **Spec×Harness** 融合 + Cursor Hooks + `scripts/gate`
- **UI-FIRST**：接入/扩展主路径为 Integration Studio，非 CLI/改仓库
- 开发环境单入口：`./scripts/activate_dev_env.sh` + 依赖封版 A′

### 0.2 符号约定

| 标记 | 含义 |
|------|------|
| **[✅ 已确认]** | 用户明确确认或指令「落地/执行/确认」 |
| **[🚫 已否决]** | 用户明确拒绝的方案 |
| **[📌 决议]** | 形成的长期规则（写入文档/规则/脚本） |
| **U{n}** | 用户第 n 条指令（对应 transcript 用户消息序号 1–243） |
| **产物** | 文件/目录/脚本/commit 等可追踪输出 |

### 0.3 产品北极星（贯穿全对话）

- **定位**：制造业 AI 执行平台 · Overlay on ERP/MES/OA 等 · 终端多模态 + 内核 Graph/Rule/Revert 门禁
- **商业路径**：基座 → 通病方案首次交付（约 10× 效率叙事）→ 定制第二次交付 → 数字资产/飞轮
- **首批客户**：哈森制造、哈森精密（哈森旗下）；先 **ERP + 钉钉 OA**，非先 MES
- **实施形态**：老系统不全废弃 → **Overlay**；中长期老系统可沉淀为 **数仓/读模型**
- **体验**：终端 0 智（语音/拍照/视频）+ 内核硬核门禁（Graph 冻结、可回滚）
- **扩展**：一切皆 **界面化配置**（UI-FIRST）；代码层只做约束与内核，非实施主路径

---

## 1. 全量用户指令索引（243 条 · 无遗漏）

> 完整原文见 transcript；此处为 **可检索摘要**，保证每条指令可追溯。

| U# | 主题摘要 |
|----|----------|
| U1–U4 | 读取 ChatGPT 分享链接 `6a30bf36…`，汇总产品方向与实施方案 |
| U5 | 分析业务类型/可行性/工程设计 → 两份文档入 `prepare/日期/` |
| U6 | **[📌]** 未确认前不要随便改文档 |
| U7 | 评审业务拆分、工程设计、商业潜力、可落地性 |
| U8 | Agent 业务链路锁定 + 可回滚 — 工程如何保证 |
| U9 | AI Coding 前锁定架构设计与推进计划 |
| U10 | 快速接入其他工厂 OA/ERP 的实施过程 |
| U11 | 业务链路模块化、免费/收费模块、各端入口（App/钉钉/企微/小程序/PC） |
| U12–U14 | 今日沟通结论清单；写入 3/4/5 与清单 |
| U15–U17 | 客户业务数据跟踪 vs 仅部署；记入文档 |
| U18 | 全量读文档 + 联网印证；评估策略是否可更强 |
| U19 | MCP / Skill / Harness Loop 如何融合分配 |
| U20 | 该策略属于什么水平 |
| U21–U23 | 业内痛点 + 顶级平台差距；沉淀文档需兜底联网 |
| U24 | 先服务哈森两家；技术基座成熟后再谈/deploy |
| U25 | **[📌]** 基座通用性：制造业通病机制 + 场景二次交付 + 数据飞轮 |
| U26–U27 | 验证该成功路径；**[✅]**「需要，落地」 |
| U28 | 全文档链路审核：商业/技术/落地性四维评价 |
| U29–U30 | 距离 coding 还差什么 |
| U31–U32 | 补 coding 前文档；冻结 Graph 策略；**[✅]** 只先做底座 |
| U33 | OS 底座涉及多少系统、架构什么样 |
| U34–U38 | WMS/OA；ERP+MES+OA 成本；预留 CRM/APS/PLM/QMS 等接入 |
| U39 | **绝对门禁**全量审 `docs`+`prepare`：商业/架构/Graph/回滚/安全 |
| U40–U44 | 3 年商业+技术版图；coding 前基础设施能否支撑演进 |
| U45 | 基座不含具体业务；3 年并行演进文档是否足够 |
| U46 | 是否可直接 coding 再谈业务 |
| U47–U48 | 什么是 ADR |
| U49–U50 | 生成 ADR；压缩 |
| U51–U53 | 系统架构图；文档/文件夹改中文名 |
| U54–U55 | Python 后端技术选型；**[✅]** 1–4 确认；cursor 规则用户自加 |
| U56 | 技术架构图（AI 板块清晰） |
| U57–U58 | ERP+钉钉场景：财务/物料痛点能否化解 |
| U59 | AI Coding 最快多久上线基础平台 |
| U60–U65 | **绝对门禁**全量评价（产品/商业/架构/成本/AI 匹配） |
| U61–U63 | 工人/管理/老板端 0 智；多模态；**[✅]** 落地终端智能+内核门禁 |
| U66–U67 | 项目结构一致性；先更新文档一致性 |
| U68–U69 | 梳理核心文档；列出可删；**[✅]** 确认删除列表「1」 |
| U70–U75 | 阿里云双 ECS（测/产）+ GitLab/YApi；精简 vs 完整 RDS；落盘云方案 |
| U76 | 先搭框架 vs 先了解业务 |
| U77 | **绝对门禁**兜底：是否满足 coding；用于内部宣讲 |
| U78 | 数字资产/飞轮策略是否清晰 |
| U79–U81 | 内部宣讲 PPT 大纲；先讲终局价值；**[✅]** 按沟通更新文档 |
| U82–U86 | 研发成本：Cursor $60、多模态 token、域名 SSL |
| U87–U90 | ERP 是否下沉数仓；Overlay vs 数仓商业；无 ERP 客户路径 |
| U91 | **[✅]** 执行 B-Lite 无 ERP 应急指引 |
| U92 | 再次 **绝对门禁** coding 就绪确认 |
| U93 | 研发周期压缩：1 年内初具规模；可并行加人 |
| U94–U97 | 策略：内核→ERP+OA(钉钉)→再加人扩展；**[📌]** 切入非 MES 而是 ERP+OA |
| U98–U101 | 优化 PPT；层次讲清 Overlay/数仓时机/通病先行 |
| U102–U103 | 大纲转 PPT；云服务用途细分；架构图是否更新 |
| U104–U106 | 部署即扒老系统形成 Graph/数字资产；写入大白话顶级战略 |
| U107–U108 | 老板已对齐；有系统+无系统双线并行；是否可进基座开发 |
| U109–U112 | 基座设计要严谨（模块/分层/项目数）；纯技术说明图；能力流程图 |
| U113–U115 | 基座是否后面不用动；做全做稳单独部署；国际架构对比 |
| U116–U120 | 对标国际竞品缺口；接入平台化 GIP；**[✅]** 确认战略 |
| U121–U135 | 多轮「顶级内核」文档审核与优化；多次 **确认** |
| U136–U141 | 是否已达 coding 前顶级内核；**[✅]** 执行 1.5（CMV/OpenAPI 等补齐） |
| U142–U145 | 百企/千企演进；**[✅]** Redis Streams；补百级演进 ADR |
| U146–U148 | 再审顶级内核；**[✅]** 生成最新基座能力图等全套图 |
| U149–U151 | 专家点评 + 竞品；**[✅]** 执行 Week 0 |
| U152–U154 | ERP 公网 API vs Edge Agent；集成后置；内核扩展性封装 |
| U155–U160 | 裁定技术栈；`os_core` 命名；仓库暂不拆；后期再分 |
| U161–U169 | 完整项目架构；配置枢纽 relation.config；**[✅]** 1–6 落地+编码绝对门禁 |
| U170–U175 | 读 rules 双 Agent；解释 Spec-Harness；融合工作流方案清单 |
| U176–U180 | docs 迁走风险；**[✅] B 策略**：精髓沉淀 `.cursor/` |
| U181–U185 | 能否融合；**[✅]** 工作流未确认禁止开工；**[✅] 我确认** 融合 |
| U186–U187 | 合并 `scripts/`；删 `src/scripts/` |
| U188–U190 | scripts 通读；README；harness 分层；**[✅]** 一步到位 |
| U191–U197 | `.cursor` 全读；工作流缺口；**[✅]** 顶级优化 |
| U198 | **[🚫]** README 必须在根目录非 docs |
| U199–U201 | T4.5 对标硅谷；**[✅]** 需要增强 |
| U202–U203 | coding 前复盘；激活工作流=最佳状态？ |
| U204–U207 | docs 快照；**[✅]** 更可靠全面策略 → `docs_baseline` |
| U208 | 核对接入/扩展交互流程是否写入文档 |
| U209–U217 | **UI-FIRST 转向**：一切皆界面配置；**[✅]** 加上/同步 |
| U218 | UI 优先策略是否已加 |
| U219 | coding 前最后链路审查（第二轮） |
| U220–U223 | `uv` 未找到；激活/ gate 报错排障 |
| U224 | 是否加 commitizen(cz) |
| U225–U228 | 提交代码正确流程；README 完整工作流表 |
| U229 | coding 前最后链路审查（第三轮） |
| U230–U234 | 依赖封版 + 自动 add 钩子？**[✅]** A′ 策略落地 |
| U235–U236 | 初始化并入「激活开发环境」单入口 |
| U237 | **[🚫]** 工作流不要双轨 A/B → 单表场景/阶段/类型 |
| U238 | **[📌]** SH-步步流通用，不含 W1 |
| U239–U240 | git push HTTP/2；SSH publickey → 切回 HTTPS |
| U241–U243 | 本归档需求；**[✅]** 全篇总结无遗漏 |

---

## 2. 分阶段行为链（按时间顺序 · 可追踪）

### 阶段 A · 外部知识导入与 prepare 建档（U1–U17）

**行为**

1. 多次尝试抓取 [ChatGPT 分享](https://chatgpt.com/share/6a30bf36-d378-83e8-8e82-971a7ffdeaf6)（页面常无正文 → 结合本地与导出补全）。
2. **U5 [✅]**：在 `docs/准备/2026-06-16/`（当日日期文件夹）形成：
   - `01-业务类型与可行性分析.md`
   - `02-工程设计总结.md`
   - `03-锁定实施策略.md` 等（后持续增补至 00–18 系列）
3. **U6 [📌]**：建立「用户未确认不改文档」纪律（贯穿后续）。
4. **U12–U14**：`00-今日沟通结论清单.md` 及条目 3/4/5 落盘。
5. **U15–U17**：数据边界（跟踪 vs 部署）、问题回写文档。

**决议摘要**

- 业务按类型拆分；工程上强调 **链路锁定 + 回滚**。
- 模块化商业：部分免费、部分模块付费；终端以 **钉钉/企微/小程序/PC** 组合按场景选型（非单一 App 定论）。

---

### 阶段 B · 策略论证与行业印证（U18–U27）

**行为**

- 全量读现有文档 + 联网查同业（MCP/Skill/Harness、工厂痛点、创业路径）。
- **U25 [📌] 核心战略**：制造业 **通用基座解决通病** → 首次部署见效 → **第二次定制交付** → 场景沉淀为方案资产（飞轮）。
- **U27 [✅]**：将论证结论写入准备区/文档。

**决议摘要**

- 不以营销为先；以哈森两家为实战验证。
- Harness/契约/Agent 分层：MCP 做连接，Skill 做场景，Harness 做门禁（后融入 `scripts/`）。

---

### 阶段 C · Coding 前文档补齐与系统边界（U28–U38）

**行为**

- 评估距离 coding 差距；补 **冻结 Graph / 执行与回滚** 策略文档。
- **U32 [✅]**：仅底座，不涉及具体业务实现。
- 系统接入范围迭代：
  - 先 ERP+MES 讨论 → **U37** 保留 OA/WMS 扩展 → **U38** 预留 CRM/CSM/APS/PLM/QMS。

**产物方向**

- `docs/文档/架构/` 下 Graph、Rule、Revert、治理规范
- `docs/文档/规格说明/执行与回滚.md` 等

---

### 阶段 D · 三年商业与技术并行演进（U39–U46）

**行为**

- **U39 绝对门禁**：递归读 `docs`+`prepare`，多维评估 + 联网对标。
- **U40–U44**：3 年商业版图与技术版图对齐；不足则补文档。
- **U45**：确认基座阶段 **不含具体系统业务**，但须支撑 3 年扩展。

**决议摘要**

- 商业：90 天试用 → 通用收费 → 定制模块（见 `九十日付费试用与转化策略.md` 等）。
- 技术：Evolution Layer、膨胀期守则、过渡架构四态。

---

### 阶段 E · ADR · 中文文档 · 架构图（U47–U56）

**行为**

- 解释并生成 **ADR** 体系（`docs/文档/架构/架构决策记录-*.md`）。
- **U52–U53**：文档标题与目录 **中文化**（`docs/文档/`、`docs/准备/`）。
- **U51、U56**：系统架构图、技术架构图（SVG/PNG，脚本生成）。

**技术裁定 [✅ U55]**

- 后端：**Python**（FastAPI 等异步栈 — 见技术架构说明文档）
- AI：LLM + 多模态链路单独成图
- Cursor 规则：**用户自行统一添加**，Agent 不擅自改 rules（当时）

---

### 阶段 F · 场景验证 · 全量评价 · 文档瘦身（U57–U69）

**行为**

- ERP 财务/物料 + 钉钉 OA 场景可行性分析。
- **U60/U64/U65 绝对门禁**：全文档再评（国内/东南亚、部署/对接成本、AI 上限）。
- **U61–U63 [✅]**：强化 **感知与多模态入口**、`Harness终端体验`、终端 0 智 + 内核门禁双强。
- **U68–U69 [✅]**：删冗余文档（用户确认列表「1」）。

---

### 阶段 G · 云基础设施与成本 · 内部宣讲（U70–U106）

**行为**

- 阿里云：**测试 ECS + 生产 ECS**，含 GitLab、YApi；**RDS 不砍**（U73：复杂度也是成本）。
- 落盘：`12-软硬件与API成本框架.md`、`15-阿里云部署方案.md`（名以实际文件为准，见 prepare）。
- **U79–U103**：内部宣讲 PPT 大纲 → **v3.1.pptx**（`generate_internal_deck.py`）。
- **U87–U91**：Overlay vs 数仓叙事；**B-Lite 无 ERP** 应急路径 **`13-产品B-Lite应急开发指引.md` [✅]**。
- **U93–U97 [📌]**：研发节奏改为 **1 年初具规模**；切入 **ERP + 钉钉 OA**，非 MES 优先。
- **U104–U106**：**部署即沉淀 Graph/数字资产** — 写入战略文档（大白话顶级战略）。

**老板对齐 [U107–U108]**

- 方向确认；基座完成后 **有系统接入 + 无系统接入** 双线并行。

---

### 阶段 H · OS 核心基座设计 · 竞品对标 · 演进 ADR（U109–U148）

**行为**

- **U109–U112**：`16-OS核心基座架构设计方案.md` — 模块、分层、项目边界、能力说明图（基座能力说明图 SVG/PNG）。
- **U113–U115**：基座低频变更、可独立发版；与国际架构对比。
- **U116–U120**：对标 Celonis/UiPath 等 → **GIP 集成平台化战略** `17-集成平台化战略(GIP).md` **[✅]**。
- 多轮文档一致性矩阵 `18-基座文档一致性矩阵.md`。
- **U139–U141 [✅] 执行 1.5**：契约/OpenAPI/CMV 等补齐。
- **U142–U145 [✅]**：百企/千企演进 ADR；**Redis Streams** 裁定；`Evolution-Layer-宪章.md`。
- **U148 [✅]**：重生成系统/数据/技术/基座能力全套图。

**内核模块（九模块 · 见名知意 `os_core`）**

`shared_contracts` · `graph` · `rule` · `revert` · `execution` · `governance` · `integration_bridge` · `observability` · `evolution`（以 `MODULE-MAP.md` / 架构设计为准）

---

### 阶段 I · Week 0 · 技术栈 · 仓库结构（U149–U169）

**行为**

- **U151 [✅] Week 0**：契约、目录骨架、测试占位、CI 雏形。
- **U153 [📌]**：**集成后置** — 内核封装扩展点；对接业务时低接入成本、读策略→资产丝滑。
- **U155–U160**：技术栈裁定文档化；仓库名 **`os_core`**；暂不分仓，后期可拆。
- **U161–U163**：`FactoryOS完整架构设计.md`、配置枢纽 `*_relation.config` 交叉配置方案。
- **U164**：**factoryos guide** CLI — 接入链路可视化（`flows.json`）；**非实施主路径**（后由 UI-FIRST 覆盖叙事）。
- **U168–U169 [✅]**：**架构闭合 1–6** + **编码绝对门禁** `.cursor/rules/编码绝对门禁.mdc`：
  - 每项目根 **README**
  - 中文注释要求
  - 未 **`确认编码门禁，开始 W1`** 禁止写 `src/os_core/**/*.py`（里程碑规则，非通用 SH-步步流）

**仓库布局（闭合后）**

```text
src/os_core/          内核九模块
src/apps/             api · web-admin · h5 · edge-agent
src/integration/      Pack · tenants · guide
src/tests/            契约/AC 测试
contracts/            OpenAPI · Schema · CMV · 验收
scripts/              gate · harness · docs_baseline · activate_dev_env.sh
.cursor/factoryos/    研发工作流真源
.cursor/docs-baseline/ docs 认知基线
_factoryos_pipeline/  运行时落盘
```

---

### 阶段 J · SH-步步流 × Spec-Harness 融合（U170–U197）

**背景**：用户 `rules/` 内原有 **Dev/Test 双 Agent 工作流**；要对标 **Spec-Harness** 全球范式并融合。

**关键对话**

- **U172–U174**：逐步确认 > 黑盒；融合后仍 **步步确认 + 落盘 + gate**。
- **U176–U180 [✅] B 策略**：`docs/` 可迁走 → **工作流真源沉淀 `.cursor/factoryos/`**（比只依赖 docs 更可靠）。
- **U184–U185 [✅]**：工作流未确认前 **禁止提开工**；用户 **「我确认」** 后实施融合。
- **U186–U187 [✅]**：`scripts/` 为唯一脚本真源；**删除 `src/scripts/`**。
- **U188–U190 [✅]**：`scripts/README.md`；`check_harness.py` 分层 tier（contracts/boundaries/step/full/auto）。
- **U191–U197 [✅]**：T4.5+ 顶配 — `gate_cli.py`（plan/test/step/pr/gate0/verify/analyze/docs-sync）、Cursor `protect-paths` hooks、pre-commit、CI。

**融合公式（终态）**

```text
步步确认（可以继续 / 确认规划 / 可以开始）
  + 落盘（plan / test / step-stop / verify / summary）
  + contracts/（OpenAPI · Schema · AC）
  + failing test → 实现 → gate step 绿
  = SH-步步流 T4.5+（L1 人机 + L2 Spec + L3 Harness）
```

**三 Agent [📌]**

| Agent | 口令 | 写 | 禁 |
|-------|------|-----|-----|
| Dev | `【Dev模式启动】` | `src/os_core` apps integration | 不宣称已测 |
| Test | `【Test模式启动】` | 仅 `src/tests/**` | 不改业务码 |
| Verify | `【Verify回合】Step N` 新对话 | `verify/` | 不写实现 |

---

### 阶段 K · README 归位 · docs 认知基线（U198–U207）

- **U198 [🚫]**：工作流说明必须在 **根 `README.md`**，不是 `docs/README.md`。
- **U204–U207 [✅]**：`docs_baseline` — manifest + mirror + policy + `WORKFLOW_MAP.json`；`gate docs-sync`；分级 Tier A/B/C。

---

### 阶段 L · UI-FIRST 产品宪法（转向 · U208–U218）

**用户纠正 [📌 重大转向]**

- **U209–U213**：接入/扩展不应长期停留在 CLI/交互命令/改代码；应 **一切皆界面**（Integration Studio）。
- 产品核心不变；变的是 **表现形态**：实施顾问与客户 IT 主路径 = **管理台 UI + AI 协同配置**。
- **U215–U217 [✅] 加上/同步** 至厚文档与 `.cursor/factoryos/`。

**产物**

- `.cursor/factoryos/UI-FIRST-CONFIG-PRINCIPLE.md`（产品宪法）
- `.cursor/factoryos/INTEGRATION-CHAIN.md`（接入链）
- 同步：`factoryos-guide规格.md`、Playbook、架构厚文档等

**与 factoryos guide CLI 关系**

- CLI 保留为 **平台研发调试** Gate 状态机；**硬性规定**非实施主路径（UI-FIRST §U4）。

---

### 阶段 M · 开发前最后三轮审查 + 环境激活（U219–U229）

- **U219/U229**：`PRE-DEV-CHAIN.md` 补链路；INDEX；ACTIVATION；WORKFLOW_MAP UI-FIRST 条目。
- **U220–U223**：安装 `uv`；`pyright` venvPath；`conftest.py` ROOT/OPENAPI；pre-push 走 `.venv`（`pytest_contract_workflow.sh`）。
- **U224**：Commitizen — 讨论后 **未强制**（可选轻量 hook）。
- **U225–U228**：明确 commit 在 Step 编码期；README 工作流表（后再改单表）。

---

### 阶段 N · 依赖封版 A′ + 激活单入口（U230–U236）

**问题**：激活工作流时多次缺依赖（pytest、pre-commit 等）。

**方案对比**

- A 自动 `uv add` on import — 用户问能否全自动
- **A′ [✅ U234]**（Agent 建议 + 用户确认）：低智管理
  - 提交 **`uv.lock`**；`uv sync --frozen --extra dev`
  - **`deptry`** 入 `gate pr`
  - pre-commit **`uv lock --check`**
  - **禁止** 裸 `pip install`
  - **不** 做 import 自动 add（避免静默漂移）

**产物**

- `scripts/activate_dev_env.sh` — **唯一激活入口**
- `scripts/check_deptry.py` · `check_uv_lock.sh` · `venv_exec.sh`
- `pre-commit`/`deptry` 入 `pyproject.toml` dev 依赖
- CI：`uv sync --frozen --extra dev`

**U235–U236 [✅]**：并入 README「激活开发环境」，删除独立「依赖封版」执行策略。

---

### 阶段 O · README 工作流单表 · 通用化（U237–U238）

- **U237 [🚫] 双轨 A/B**（对话轨/终端轨分列）→ **单表**：场景 | 阶段 | 类型(对话/终端) | 你说/你做 | 说明（#0–#15）。
- **U238 [📌]**：SH-步步流 **通用**，**删除主表中的 W1 总闸行**；`确认编码门禁，开始 W1` 仅作 **里程碑附加口令**（`编码绝对门禁.mdc` · ACTIVATION §四）。

---

### 阶段 P · Git 推送排障（U239–U240）

| 现象 | 原因 | 处理 |
|------|------|------|
| `Error in the HTTP2 framing layer` | HTTPS HTTP/2 链路不稳 | `GIT_HTTP_VERSION=HTTP/1.1 git push` |
| `Permission denied (publickey)` | remote 改为 SSH 但未配 key | **切回 HTTPS** `https://github.com/sunhailiang-tourist/FactoryOS.git` |

---

## 3. 关键决议总表（Decision Log）

| ID | 决议 | 确认 | 影响 |
|----|------|------|------|
| D01 | 未确认不改文档 | U6 | Agent 纪律 |
| D02 | 通用基座 + 通病首次 + 定制二次 + 飞轮 | U25–U27 | 08-平台战略与两次交付模型 |
| D03 | 先 ERP+钉钉 OA，非 MES 优先 | U94–U97 | 实施顺序、PPT |
| D04 | Overlay 先行；老系统中长期沉淀数仓 | U87–U90 | 商业叙事 |
| D05 | B-Lite 无 ERP 应急路径 | U91 | 13-产品B-Lite |
| D06 | 部署过程沉淀 Graph = 数字资产 | U104–U106 | 战略文档 |
| D07 | 基座低频变更、可独立发版 | U113–U115 | os_core 治理 |
| D08 | GIP 集成平台化 | U118–U120 | 17-GIP |
| D09 | Redis Streams（演进总线） | U823 | Evolution ADR |
| D10 | 集成后置；内核封装扩展性 | U153 | 架构原则 |
| D11 | 内核命名 `os_core`；见名知意 | U160 | 目录 |
| D12 | 配置枢纽 relation.config | U162–U163 | 跨项目配置 |
| D13 | 编码绝对门禁 + 中文注释 + 项目 README | U168–U169 | `.cursor/rules/编码绝对门禁.mdc` |
| D14 | B 策略：工作流真源 `.cursor/factoryos/` | U180 | 与 docs 分离 |
| D15 | SH×Spec-Harness 融合 T4.5+ | U185 | gate/hooks/CI |
| D16 | scripts 唯一真源；删 src/scripts | U187 | 目录 |
| D17 | 工作流说明在根 README | U198 | README.md |
| D18 | docs_baseline 快照 | U207 | `.cursor/docs-baseline/` |
| D19 | **UI-FIRST** 实施主路径 = Studio | U213–U217 | UI-FIRST-CONFIG-PRINCIPLE |
| D20 | 依赖 A′：lock+frozen+deptry | U234 | pyproject/uv.lock/scripts |
| D21 | 激活单入口 activate_dev_env.sh | U235–U236 | README/ACTIVATION |
| D22 | 工作流单表；非双轨 | U237 | README §完整工作流 |
| D23 | SH-步步流通用；W1 仅里程碑 | U238 | README/ACTIVATION |

---

## 4. 主要产物清单（按类别）

### 4.1 文档 · docs/准备/2026-06-16/（系列）

`00-今日沟通结论清单` · `01`–`18`（含 OS 基座设计、GIP、一致性矩阵、成本、B-Lite、路线图、PPT 等）

### 4.2 文档 · docs/文档/（厚文档 · 可外迁）

架构 ADR、架构图 SVG/PNG、规格说明、连接器 catalog、验收 AC、商业目录等

### 4.3 契约 · contracts/

OpenAPI、JSON Schema、CMV 注册表、schemas、acceptance

### 4.4 治理 · .cursor/

| 路径 | 作用 |
|------|------|
| `factoryos/` | SH-步步流、GATES、三 Agent 细则、ACTIVATION、PRE-DEV-CHAIN、UI-FIRST、INTEGRATION-CHAIN、模板 |
| `rules/` | 编码绝对门禁、工厂操作系统、SH-步步流 mdc、test workflow |
| `docs-baseline/` | manifest、mirror、policy、WORKFLOW_MAP |
| `hooks.json` + `hooks/` | protect-paths 等 |
| `ai_chat_history/` | **本归档** |

### 4.5 脚本 · scripts/

`gate` / `gate_cli.py` · `harness` / `check_harness.py` · 四门检查 · `docs_baseline` · `factoryos` guide CLI · **`activate_dev_env.sh`** · `check_deptry.py` · `check_uv_lock.sh` · `venv_exec.sh` · `pytest_contract_workflow.sh`

### 4.6 代码骨架 · src/

`os_core/`（占位）· `apps/` · `integration/`（含 guide/flows.json）· `tests/`（contract/ac）

### 4.7 CI / 工具链

`.github/workflows/ci.yml` · `.pre-commit-config.yaml` · `pyproject.toml` + **`uv.lock`** · `.python-version`

### 4.8 Git 提交链（创建期）

```
6e7f1d4 init
2f5843a 开发前AI研发工作流和研发规范初始化完成
9fa06e8 更新验证工作流问题
c59aa26 开发环境工作流激活-验证工作流问题修复
6b055a8 coding前脚手架设计存档
3e75c24 coding前脚手架设计存档
2543505 添加依赖包自动同步机制
```

---

## 5. 研发工作流终态（as-of 2026-06-24）

### 5.1 激活（每台机器一次）

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh && source $HOME/.local/bin/env   # 首次
./scripts/activate_dev_env.sh
# → frozen sync · docs_baseline refresh · gate pr · pre-commit install
# → Cursor 仓库根 · Hooks protect-paths · 重启
```

### 5.2 完整工作流（README 单表 #0–#15）

| # | 场景 | 类型 | 要点 |
|---|------|------|------|
| 0 | 准备 | 终端 | activate_dev_env.sh |
| 1–2 | 启动 | 对话 | Dev启动 → 可以继续 |
| 3–5 | 规划 | 对话+终端 | plan → 确认规划 → gate plan |
| 6–7 | 测试 | 对话+终端 | Test启动 → gate test |
| 8–10 | 编码 | 对话+终端 | 可以开始 → harness+commit |
| 11–13 | 验收 | 对话+终端 | step-stop → gate step → Verify |
| 14–15 | 交付 | 对话+终端 | summary → gate pr → push |

**↻** #8–#13 每 Step 循环。

**里程碑附加**（非通用）：W1 首轮前 `确认编码门禁，开始 W1`（见编码绝对门禁.mdc）。

### 5.3 workflow_state 关键词

`可以继续` · `确认规划` · `可以开始` · `测试不通过` · （W1）`确认编码门禁，开始 W1`

---

## 6. 尚未完成 / 刻意 pending

| 项 | 状态 | 说明 |
|----|------|------|
| W1 业务实现 | 未开始 | 需 SH-步步流首轮：Dev启动 → plan → Test → 可以开始 |
| Gate 0 全量 AC | pending | 52 P0；CI `gate0-ac-full` 仍注释 |
| Integration Studio UI | 未建 | UI-FIRST 主路径；可与 W1 并行（PRE-DEV-CHAIN 建议） |
| `src/os_core` 业务代码 | ~0% | 仅 `__init__.py` |
| Commitizen | 未强制 | U224 讨论；可选 |
| docs/ 外迁 | 未执行 | B 策略已防依赖 |

---

## 7. 用户偏好与 Agent 纪律（创建期沉淀）

1. **绝对门禁**：多次要求「全量阅读、不得抽检、不得随机」— 审文档/写归档须通读。
2. **确认前不改文档**（U6）；**工作流未确认不开工**（U184）。
3. **反感双轨撕裂感**（U237）；要单表、小白友好。
4. **低智管理**：依赖/门禁机械检查，开发者不盯包管理（A′）。
5. **README 跟仓库走**（U198）；真源分层清晰。
6. **产品 vs 研发分离**：UI-FIRST = 实施；SH-步步流 = 平台研发。

---

## 8. 给未来 AI 的快速恢复指令

新开对话建议：

```text
请阅读 @.cursor/ai_chat_history/2026-06-24-FactoryOSCreateChatHistory.md
和 @.cursor/factoryos/INDEX.md、@README.md。
当前阶段：开发前脚手架已完成，业务 coding 未开始。
不要重新争论 [Decision Log] 中已确认决议。
若要继续研发，从 SH-步步流 #1 Dev模式启动 开始。
```

---

## 9. 溯源

| 项 | 值 |
|----|-----|
| Transcript ID | `58e262bf-3054-4647-855a-8bdae148d923` |
| Transcript 路径 | `.cursor/projects/.../agent-transcripts/58e262bf-.../58e262bf-....jsonl` |
| 用户指令数 | 243 |
| Transcript 行数 | 1427 |
| 归档撰写 | 2026-06-24 · 通读 transcript 后人工结构凝练 |

---

*本文档为创建期快照。代码与 `.cursor/factoryos/` 演进后，以仓库真源为准；重大变更请增补新日期归档或更新 WORKFLOW_MAP。*
