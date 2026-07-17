# Ax OS / FactoryOS · 平台定位与战略白皮书

| 项 | 内容 |
|----|------|
| **版本** | **v1.1**（兜底核对修订） |
| **日期** | 2026-07-14 |
| **状态** | Accepted（全库 `docs/` **212** 文件递归通读 + 像素核对 + 兜底修订） |
| **读者** | 老板 · 产品 · 实施 · 研发 · 其他 AI（战略输入） |
| **配对文档** | [Ax-OS-产品PRD完整版-可还原原型-v2.0.md](./Ax-OS-产品PRD完整版-可还原原型-v2.0.md) |
| **真源优先级** | ADR-000～008 > `18-基座文档一致性矩阵` > PLATFORM-FIRST 策略 > 本白皮书 > 早期演进草稿 |

---

## 0. 阅读说明与证据范围

### 0.1 本文回答什么

用**资深产品/战略**口径，一次说清：

1. 这个平台**是什么 / 不是什么**  
2. **核心目标**（短期 / 中期 / 长期）  
3. **商业价值**与变现结构  
4. **业务策略**（两次交付、部署即资产化、飞轮）  
5. **执行方案**（平台先行三阶段）  
6. **设计思路**（双极 · Overlay · UI-First · GIP）

### 0.2 通读范围（绝对门禁 · 已执行）

| 分区 | 规模 | 用途 |
|------|------|------|
| `docs/准备/` | 战略 · 一年/三年 · GIP · 演进 | 商业与执行主口径 |
| `docs/文档/` | ADR · 规格 · Schema · 验收 · 连接器 · OpenAPI | 产品边界与工程宪法 |
| `docs/设计/` | PRD · 设计稿 · factoryos-v2/bak1 · 墨刀 · Figma · UI 图 | 原型与视觉真源 |
| 资源 | 11 PNG · 5 SVG · HTML 52 · JSON 33 · YAML/CSV/XLSX | 像素级核对 + 结构对账 |

> 日常研发契约真源仍在 `.cursor/factoryos/` 与 `contracts/`；`docs/` 为历史+产品认知仓。本白皮书是对 `docs/` 的**战略收敛**，不替代 Contract Registry。

### 0.3 命名约定（必须统一）

| 名称 | 含义 |
|------|------|∏
| **FactoryOS** | 平台产品总称 / 企业业务操作系统 |
| **Ax OS** | 管理端（web-admin）品牌名 · 「智能中枢系统」 |
| **h5-worker** | 产线终端（钉钉/企微 H5） |
| **os_core** | 内核门禁极（Graph/Rule/Execution/Audit…） |

---

## 1. 一句话定义

> **FactoryOS 是制造业 AI 执行操作系统（Governed Overlay）；管理端品牌为 Ax OS（智能中枢系统）。不替换 ERP/MES 账本，用冻结业务图谱 + 规则引擎 + 唯一写路径 + 全审计 + 可撤回 + 每日对账，让工厂「敢写、可追、可回滚」；配置只走 Integration Studio；部署过程把老系统执行链路提炼成可复制的数字资产（Pack / Package）。**

---

## 2. 我们是什么 / 不是什么

### 2.1 是什么（✅）

| 维度 | 定义 | 证据 |
|------|------|------|
| 产品形态 | ERP/MES **之上**的执行 Overlay + 终端入口 | ADR-000 · 08 · 设计稿 §1 |
| 能力内核 | frozen Graph + Rule + DSL + Audit + Revert + 对账 | ADR-001/002 · D1 五项 |
| 交互形态 | **双极**：终端说/扫/拍 + 内核门禁 | ADR-001 · UX-001 |
| 实施形态 | **UI-First**：Studio 六步接入，零改仓库 | ADR-008 · STU-001 |
| 商业形态 | Graph / Capability / Connector **Pack** 模块化售卖 | ADR-003 · 模块包商业目录 |
| 复制形态 | 第一家考古 Export，第二家 Import | 08 §1.4 部署即资产化 |
| 验证路径 | 哈森灯塔 **Path A（ERP 写+读 + 钉钉）** | ADR-005 · 14 |

### 2.2 不是什么（❌）

| 禁止定位 | 为什么 |
|----------|--------|
| ERP / MES 替代品 | 账本权威在 Legacy（Data-L0） |
| 无治理聊天机器人 / Agent 直写库 | R-01：Agent 只出计划，禁止直连 Connector 写 |
| 客户全量业务数仓 | 默认不做 Data-L3；必做的是执行跟踪与对账（Data-L1） |
| 装完离场的一次性 SI | 必须 export Package；飞轮靠 Pack 复利 |
| 无确认自动财务/付款/库存调整 | 首期禁止；操作原则「先读→建议→确认→自动化」 |
| 改 Git YAML 上线的实施路径 | STU-R1～R5；published 真源 = Registry DB |
| Phase 1 独立 App | 入口以钉钉/企微 H5 + PC Web（1+2+1） |

### 2.3 对外价值主张（行业语言）

| 成果 | 用户感知 | 禁用文案 |
|------|----------|----------|
| 打破孤岛 | ERP/MES/WMS/PLM/OA 经中枢连通 | 「让制造不再黑箱」（设计稿明确禁用） |
| 执行可管 | 每笔写入有规则、确认、审计 | 售前内部名「Studio 六步」勿对外当 slogan |
| 决策可追 | 对账零漂移或告警；可撤回 | — |
| AI 降复杂度 | 说/扫/拍代替菜单树，**不是**代替账本 | — |

**品牌语（定稿）**：`Ax OS · 智能中枢系统` · `AI 时代 · 全域连接 · 全程可追` · *The Axis of Modern Manufacturing*

---

## 3. 核心目标

### 3.1 北极星（产品结果）

| 目标 | 度量 |
|------|------|
| 第一家工厂 D1 可结案 | 五机制 + 报工 Skill + Package 导出 + 书面签字 |
| 实施零仓库 | Studio 完成 onboard（STU-01） |
| 工人愿意用 | 报工 P50 ≤ 30s；≤3 次关键点击 |
| 企业敢开写 | Shadow ≥14 天 + 双签 + 零未解释 drift |
| 第二家可复制 | Import ≤ 3 周（Silver）或全量 4–8 周 |

### 3.2 D1 只承诺五件事（通病包边界 · 铁律 R1）

1. 跨系统 **只读查询**（L0）  
2. **受控写**（DSL + Rule + 人工确认）  
3. **全链路审计**  
4. **可演示撤回**（Revert / Compensator）  
5. **每日对账**（零未解释 drift 或自动告警）

首条垂直场景：**生产报工**（`graph-work-report` + `skill-work-report-v1`）。

### 3.3 时间轴目标

| 视窗 | 目标 | 真源 |
|------|------|------|
| **短期（当前）** | 阶段 1b：Studio UI 真 API 联调绿；禁止抢跑 h5 / 哈森生产写 | 14 §〇 · PLATFORM-FIRST |
| **中期（一年）** | 平台→终端→哈森四 Gate；3～5 家 tenant；飞轮启动 | 14 · 09 |
| **长期（三年）** | Pack 目录化 · 多租户规模 · MCP 生态 · ARR 订阅为主 | 09 · ADR-007 |

---

## 4. 商业价值

### 4.1 痛点 → 价值映射

| 制造业通病 | 平台机制 | 客户价值 |
|------------|----------|----------|
| Execution Gap（计划与执行脱节） | Overlay + frozen Graph | 现场动作与账本对齐 |
| 系统孤岛 | Connector + CMV 标准动词 | 少搬数据、少培训 |
| 不敢让 AI 写库 | Rule 默认拒绝 + Harness 双确认 | 敢开写 |
| 错了收不回 | Audit + Revert | 可控风险 |
| 数对不上 | Shadow + 每日对账 | 信任建立 |
| 每厂从零集成 | Package Export/Import | 复制加速、成本下降 |

### 4.2 收入四层（L0–L3）

| 层 | 卖什么 | 典型 SKU |
|----|--------|----------|
| **L0** | 平台订阅（审计/对账/租户） | Platform Starter / Pro / Enterprise |
| **L1** | D1 通病包 + 首期 Connector | Starter-A / Starter / B-Lite |
| **L2** | D2 沉淀 Pack | 计件草案、质量追溯、WMS 只读… |
| **L3** | Override / 配置化定制 | 厂/线级差异（禁止进内核） |

**哈森主力档**：`Starter-A` = D1 + `conn-erp-*-write/read` + `conn-dingtalk`。

### 4.3 九十日付费试用（Q0）

- 试用 **收费**（防 pilot purgatory）  
- 范围 = D1 五项，不含计件/排产等 D2  
- 转化 Gate：Shadow 报告 + D1 签字 + Package export + 订阅合同  
- 哈森内部可模拟费用，**流程与签字不变**（铁律 R5）

### 4.4 壁垒（不是模型更聪明）

1. 冻结图谱 + 默认拒绝规则 + 唯一写路径（信任）  
2. Shadow / 对账 / Revert 工程化（敢写）  
3. 部署即资产化 → Pack 复利（越部署越快）  
4. UI-First Studio（实施可规模化，不靠改代码）

---

## 5. 业务策略

### 5.1 两次交付模型（D1 / D2）

```text
平台地基（通病机制）
  → 第一次交付 D1（通病包，≤90 天书面结案）
  → 第二次交付 D2（厂特异痛点，≥70% 入库 Pack）
  → export Package → 下一家 D1 更快
```

| 铁律 | 内容 |
|------|------|
| R1 | 通病包 v1 **只有五项** |
| R2 | 第一次 **≤90 天书面结案** |
| R3 | **第二次**才开放特异 Graph/Skill |
| R4 | 每家结束必须 **export Package** |
| R5 | 内部灯塔 **按外部客户验收** |

### 5.2 部署即资产化

> 每部署一家厂，在现场提炼老系统**执行链路**（谁报工、写哪、谁确认、怎么对账、怎么撤）→ Graph / Pack / Package；第一家像考古，第二家起像 import。

**红线**：≠ 扒库做数仓；≠ AI 自动认定链路（必须 freeze）；≠ 改内核。

### 5.3 写入路径（Path）与部署态正交

| Path | 客户 | 写落点 | 灯塔 |
|------|------|--------|------|
| **A** | 有 ERP 无 MES | ERP | **哈森** |
| **B** | 有 MES | MES（ERP 只读） | 其他厂 |
| **C** | 无 ERP | 内置 PG 账本 | B-Lite（默认不售） |

部署三态：**Pool / Bridge / Silo**（与 Path 可组合；哈森 = Path A + Pool）。

### 5.4 客户分型

| 类 | 特征 | 策略 |
|----|------|------|
| A | 有 ERP/MES | **优先** Overlay |
| B | 烂系统+Excel | 痛点强、数据难，谨慎 |
| C | 无系统 | 短期不做全栈；B-Lite 仅老板拍板应急 |

### 5.5 场景优先级

```text
工人报工 → 生产主管分析 → 老板决策（先只读/建议/确认）
```

---

## 6. 执行方案（锁死）

### 6.1 平台先行三阶段（废止「三线并行」）

```text
P0 内核 Gate 0 ✅
  → 阶段 1 平台打磨（STU-001）
       ├─ 1a STU-API ✅
       └─ 1b STU-UI（Studio 真 API）← 当前主战场
  → 阶段 2 终端设计（h5-worker · UX-001）须 1b 绿
  → 阶段 3 项目验证（哈森 · BASE+UX+MVP+STU 四 Gate）
```

| 阶段 | 硬 Gate | 明确不做 |
|------|---------|----------|
| 1 平台 | STU-001（1a+1b） | h5 生产、哈森现场、D1 |
| 2 终端 | UX-001 | 哈森 UAT、生产开写 |
| 3 项目 | 四 Gate 同绿 | 改 os_core major |

### 6.2 工程优先级（不可颠倒）

```text
可靠性 > 安全性 > 可追溯 > 可回滚 > AI 能力
```

投入顺序：**Graph → Rule → Audit → Rollback → Agent → 多模态**（与常见团队相反）。

### 6.3 一年节奏（主口径）

```text
① 方向确认 → ② 内核 W1–W8 Gate 0 → ③ 云采购并行
→ ④ 1a API → ④b 1b Studio UI → ⑤ h5-worker
→ ⑥ 哈森 Shadow/UAT/D1/export → ⑦ 第 2 家 import / B-Lite
```

---

## 7. 设计思路（产品架构哲学）

### 7.1 双极架构

```text
终端智能极（h5-worker）          内核门禁极（os_core）
说/扫/拍 · ≤3 tap · 0 智培训      Graph frozen · Rule deny-by-default
              ╲                  ╱
                 Harness 确认门
                 （工人 + 主管）
```

### 7.2 唯一写路径（产品必须可见）

```text
感知 → Agent 出 DslPlan（未执行）
    → Harness 确认
    → Rule 评估（默认拒绝）
    → Execution（唯一写 Legacy）
    → Connector
    → Audit / 对账 / Revert
```

### 7.3 配置平面（UI-First · GIP）

- **GIP（Governed Integration Platform）**= Platform-L1：Connector Pack + Studio + Registry，**不改** L0 写路径红线（ADR-004）  
- published 配置只经 **Studio API → PostgreSQL Registry**（ADR-008）  
- Git YAML = export / CI 镜像，**不是**实施主路径  
- 关键租户开关（产品语言必须可见）：

| 开关 | 默认 | 含义 |
|------|------|------|
| `shadow_mode` | `true` | L2 写仅 `simulated`，Legacy 不变 |
| `write_approved` | `false` | 未双签批准前禁止生产写 |
| `secrets_ref` | 必填 | 凭证只存引用，界面禁止明文密钥 |

- Studio 六步顺序（铁律）：

```text
Connect → Discover → Map → Prove(Shadow+双签) → Freeze → Export
```

> Studio **六步名称**锁死如上。人审三门**语义顺序**（2026-07-15 用户裁定）：**G-FREEZE → G-SHADOW(≥14d) → G-WRITE-APPROVE**。若向导 Tab 序与三门语义不一致，登记对齐债，不得改六步名。真源：`.cursor/factoryos/PM-GATES.md`。

### 7.4 人审 Gate（不可自动化跳过）

| Gate | 含义 | 签署 | 产品字段 |
|------|------|------|----------|
| G-FREEZE | Graph 冻结（L2 写前置） | business_owner | `graph.status=frozen` |
| G-SHADOW | 影子运行 ≥14 天 | integrator | `shadow_mode=true` |
| G-WRITE-APPROVE | 批准生产写 | admin + business_owner | `write_approved=true` |

### 7.5 信息架构（管理台五域 · 行业语言）

```text
制造全景（看） → 产业连接（接 · Studio）→ 资产与复制（复制）
→ 运营与合规（管）→ 平台治理（SaaS）
```

**禁止**侧栏出现工程模块名（如 `graph_service`）。

### 7.6 视觉定稿要点（像素核对结论摘要）

| 资产 | 结论 |
|------|------|
| `ax-os-login-v4-smart-hub.png` | **登录定稿**：左表单 + 右中枢连接 ERP/MES/WMS/PLM/OA；主标「智能中枢系统」 |
| `ax-os-login-v3-*.png` | **废止视觉**：含「让制造不再黑箱」「制造业数字中枢」 |
| `ax-os-home-dashboard.png` | **早期 IA 草案**：侧栏为工作台/集成工作室等，**不得**作五域真源 |
| `figma/ax-os-dashboard-figma-ref.png` | KPI 四卡对齐产品；子导航偏 MES 深化，属 D1+ 扩展，非 Stage1 必做 |
| `figma/ax-os-studio-prove-figma-ref.png` | Shadow/双签语义正确；**六步文案错误**（含 Simulate/Publish），以 Studio 规格为准 |
| `design-tokens.json` | 深空底 `#0A0E1A` · 主色 `#00D4FF` · Shadow 琥珀 `#FFB300` |

完整原型规格见配对 PRD。

---

## 8. 文档矛盾登记（核对结论）

| 级 | 矛盾 | 裁定真源 |
|----|------|----------|
| **A** | 侧栏 IA 多版本并存 | **五域**（墨刀 PRD v1.1 + factoryos-v2） |
| **A** | Studio 六步名不一致 | **Connect/Discover/Map/Prove/Freeze/Export** |
| **A** | Gate 0 后并行 vs 平台先行 | **平台先行三阶段**（14 v1.2） |
| **A** | 哈森 MES 写 vs ERP 写 | **Path A ERP 写**（ADR-005） |
| **B** | 原型页数 34/21 vs 实际编号 | **32 墨刀页 = 22+8+2**；HTML 27 文件（Studio 合页）；见 PRD v2.1 |
| **B** | 09 一年「双轨」措辞 | 日历以 **14** 为准；09 的 Y1/Y2/Y3 作能力标签 |
| **C** | bak1 vs v2 HTML | **v2 为线框真源**；bak1 仅历史 |
| **C** | 登录 V3 vs V4 | **V4** |

---

## 9. 成功要点（老板一页）

1. **不换 ERP**：接在账本之上做受控执行。  
2. **第一次只卖通病五项 + 报工**，90 天内书面结案。  
3. **第二次才做厂特异**，且大部分变成 Pack。  
4. **配置走 Studio**，不靠工程师改 YAML。  
5. **先平台后终端后项目**，哈森验证放在能力够用之后。  
6. **每部署一家就变快**：Export → Import 飞轮。

---

## 10. 兜底核对结论（v1.1）

| 维度 | 判定 | 说明 |
|------|------|------|
| 是什么 / 不是什么 | ✅ Pass | 与 ADR-000/001/002、08、设计稿一致 |
| 核心目标 / D1 五项 | ✅ Pass | 与 08 R1、验收四 Gate 一致 |
| 商业价值 / Pack / Q0 | ✅ Pass | 与 09、模块包目录、九十日试用一致 |
| 业务策略 D1/D2 / Path | ✅ Pass | Path A 哈森灯塔（ADR-005）正确 |
| 执行方案平台先行 | ✅ Pass | 对齐 14 v1.2.1；废止三线并行 |
| 设计思路双极/写路径/UI-First | ✅ Pass | 已补 GIP + `shadow_mode`/`write_approved` |
| 与 PRD 可接力设计原型 | ✅ Pass | 配对 PRD v2.1；线框真源 factoryos-v2 五域 IA 全库一致 |

**本白皮书职责边界**：只锁战略与定位；**页面级原型还原**必须另读配对 PRD。

---

## 11. 附录 · 关键文档索引

| 主题 | 路径 |
|------|------|
| 沟通结论 / 术语 | `docs/准备/2026-06-16/00-今日沟通结论清单.md` |
| 两次交付 | `docs/准备/2026-06-16/08-平台战略与两次交付模型.md` |
| 一年执行 | `docs/准备/2026-06-16/14-一年冲刺路线图与并行研发.md` |
| 三年商业 | `docs/准备/2026-06-16/09-三年商业与技术路线图.md` |
| GIP | `docs/准备/2026-06-16/17-集成平台化战略(GIP).md` |
| 一致性矩阵 | `docs/准备/2026-06-16/18-基座文档一致性矩阵.md` |
| ADR 链 | `docs/文档/架构/架构决策记录-000～008*.md` |
| 完整架构 | `docs/文档/架构/FactoryOS完整架构设计.md` |
| Pack 目录 | `docs/文档/商业/模块包商业目录.md` |
| 试用转化 | `docs/文档/商业/九十日付费试用与转化策略.md` |
| 验收四 Gate | `docs/文档/验收/验收用例-*.md` |
| 产品原型入口 | `docs/设计/README.md` |

---

## 修订记录

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-07-14 | 全库通读核对后首版战略白皮书 |
| **v1.1** | **2026-07-14** | 兜底核对：修正「成功要点」笔误；补 GIP/`shadow_mode`/`write_approved`；品牌命名澄清；追加核对结论表 |
| v1.1.1 | 2026-07-15 | §7.4 人审三门裁定为 **G-FREEZE → G-SHADOW → G-WRITE-APPROVE**；挂载 PM Agent |

---

**本文 = 战略与定位真源合成。** 原型与功能落地请读配对 PRD v2.1。  
**产品 Agent**：`【PM模式启动】` → `.cursor/factoryos/PM-GATES.md`。
