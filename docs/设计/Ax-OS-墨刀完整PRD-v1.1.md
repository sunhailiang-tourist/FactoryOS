# Ax OS · 墨刀完整 PRD（产品需求 + 原型搭建规格）

| 项目 | 内容 |
|------|------|
| **产品名称** | Ax OS（FactoryOS 管理端品牌） |
| **文档类型** | 墨刀专用 PRD（可直接复制给墨刀 AI / 设计师按表搭页） |
| **版本** | **v1.1** |
| **状态** | 真源合成稿（ADR + 规格 + 验收 + factoryos-v2 对齐） |
| **真源优先级** | ADR-000～008 > 18-一致性矩阵 > Integration-Studio > Playbook > 本 PRD |
| **参考线框** | `docs/设计/factoryos-v2/*.html`（27 页，已 ~100% 对齐） |

---

## 〇、给墨刀的使用说明（先读）

### 0.1 本文档能做什么

- **墨刀设计师**：按 **§4 页面清单** 建页，按 **§5～§7 逐页规格** 摆元素，按 **§8 热区连线表** 画跳转。
- **墨刀 AI**：将本文全文或单页 § 作为 Prompt，生成线框页；生成后对照 `factoryos-v2` 同名 HTML 校对。
- **产品/研发**：本文 = PRD + 原型说明合一；验收对照 **§10 追溯矩阵**。

### 0.2 墨刀项目设置

| 项 | 值 |
|----|-----|
| 项目名称 | Ax OS 智能中枢系统 · 产品原型 v1.1 |
| Web 画布 | 1440 × 900 |
| H5 画布 | 375 × 812（手机框） |
| 风格 | 深色线框（灰底 + 边框 + 文字），**非**视觉稿 |
| 图标族 | Phosphor `ph:*`（与参考 HTML 一致） |
| 动效 | Web：智能动画·向右推入；H5：向上滑入 |

### 0.3 全局母版（所有 Web 页复用）

**侧栏导航（五域 · 行业语言，禁止写工程模块名）**

| 顺序 | 文案 | 跳转页 |
|------|------|--------|
| 1 | 制造全景 | strategy / kpi_dashboard |
| 2 | 产业连接 | integration |
| 3 | 资产与复制 | business |
| 4 | 运营与合规 | workflow |
| 5 | 平台治理 | tenants |

**顶栏品牌**：Ax OS · 智能中枢系统

**哈森灯塔默认徽章（W-02 及 Studio 相关页）**

- `ERP 金蝶 ✅` · `Edge 在线` · `Path A · Pool`

### 0.4 H5 全局顶栏（三态互斥 · 每页只显示一种）

| 状态 | 顶栏文案 | 适用页面 |
|------|----------|----------|
| shadow_mode=true | `⚠️ 影子运行 · simulated only · 生产写禁用` | H-01～H-04 |
| write_approved=false | `🔒 生产写未批准 · Connector 写禁用` | H-05、H-06 |
| write_approved=true | `✅ 生产写已批准 · 已写 Legacy` | H-07 |

**H-01 入口页额外**：三态图例说明条（教学用，三格并排灰/琥珀/绿）。

### 0.5 概念铁律（原型中必须可见）

| 铁律 | 原型表现 |
|------|----------|
| STU-R1～R7 | 配置只经 Studio；Connect 只读；凭证用 secrets_ref |
| 无 ERP ≠ 无 Shadow | B-Lite 页须写此免责 |
| Gate 顺序 | **Prove(Shadow) → G-WRITE-APPROVE → G-FREEZE → Export**（卡片与流程均按此序） |
| Path ⊥ 部署 | Path A/B/C 与 Pool/Bridge/Silo **可组合**；哈森 = **Path A + Pool** |
| Agent 禁写 | 只出计划卡，执行须经 Harness 双确认 |

---

## 一、产品概述

### 1.1 定位

**Ax OS = 制造业智能中枢 Overlay**：在客户 ERP/MES 之上，提供 **敢写、可追、可回滚** 的 AI 执行能力。

| 是 | 不是 |
|----|------|
| ERP/MES 之上的执行 Overlay | ERP 替代品 |
| 冻结链路 + 规则 + 审计 + 撤回 | 无治理聊天机器人 |
| 第一家 Export、第二家 Import | 装完离场 |

### 1.2 产品形态

```text
web-admin（Ax OS 管理台） ─┐
                           ├── os_core 内核 ──► Legacy ERP/MES
h5-worker（产线 H5 终端） ─┘
```

### 1.3 产品目标

| 目标 | 度量 |
|------|------|
| 第一家 D1 结案 | 五机制 + 报工 + Package Export |
| 实施零仓库 | Studio 六步完成 onboard |
| 工人愿意用 | 报工 P50 ≤ 30s |
| 企业敢开写 | Shadow ≥14d + 双签 + 零未解释 drift |
| 第二家复制 | Import ≤ 3 周（Silver Pack） |

---

## 二、用户与场景

### 2.1 角色

| 角色 | 入口 | 核心场景 |
|------|------|----------|
| 实施顾问 | web-admin / Studio | Connect～Export / Import |
| 客户 IT | Studio Connect | 凭证、Edge、私网 |
| 业务负责人 | Prove / Freeze | 双签、Graph 冻结 |
| 租户管理员 | 运营域 | Shadow、开写批准 |
| 工人 | h5-worker | 语音/扫码/拍照报工 |
| 主管 | h5-worker | 待办确认、驳回 |
| 运维 | 运营域 | Drift、熔断、审计 |

### 2.2 用例（四条主线）

| 编号 | 场景 | 墨刀演示主线 |
|------|------|--------------|
| UC-01 | 首家接入 | 主线 A |
| UC-02 | 日常报工 | 主线 B |
| UC-03 | 第二家 Import | 主线 C |
| UC-04 | Gate / 合规 | 主线 D |

---

## 三、功能架构

### 3.1 五域信息架构

```text
Ax OS web-admin
├── 制造全景（看）     → KPI、战略全景、架构说明
├── 产业连接（接）★    → Studio 六步 + 集成概览
├── 资产与复制（复制） → Package / Import 向导
├── 运营与合规（管）   → Shadow、Drift、审计、证据、Gate 地图
└── 平台治理（SaaS）   → 租户、License

h5-worker（产线）
├── 角色入口 → 工人 / 主管
├── 报工多模态 → 确认 → 主管审批 → 完成
└── Shadow 状态监控（可选附页）
```

### 3.2 Studio 六步（产业连接主路径）

| 步 | ID | 页面 | 产出 |
|----|-----|------|------|
| 1 | Connect | W-04 | 连通报告；secrets_ref |
| 2 | Discover | W-05 | CMV 动词表 |
| 3 | Map | W-06 | 字段映射 |
| 4 | Prove | W-07 | Shadow + 双签 → write_approved |
| 5 | Freeze | W-08 | Graph frozen |
| 6 | Export | W-09 | Implementation Package |

### 3.3 写入路径（Path）

| Path | 条件 | 写目标 | 灯塔 |
|------|------|--------|------|
| A | 有 ERP | Connector 写 ERP | **哈森** |
| B | 有 MES | MES 写 + ERP 读 | — |
| C | 无 ERP | Builtin 账本 | B-Lite |

### 3.4 部署三态（与 Path 正交）

| 态 | 含义 |
|----|------|
| Pool | SaaS 多租户 · tenant_id + RLS |
| Bridge | schema-per-tenant |
| Silo | 独立部署 cell |

---

## 四、墨刀页面清单（共 34 页）

> 每一行 = 墨刀中独立一页。参考 HTML 在 `factoryos-v2/` 下同名文件。

### 4.1 核心交付页（21 页 · 验收必含）

| 编号 | 墨刀页名 | 参考 HTML | 画布 |
|------|----------|-----------|------|
| W-01 | 登录 | login.html | Web |
| W-02 | KPI 仪表盘 | kpi_dashboard.html | Web |
| W-03 | 租户列表 / Studio 入口 | tenants.html | Web |
| W-04 | Studio · Connect | studio.html#step1 | Web |
| W-05 | Studio · Discover | studio.html#step2 | Web |
| W-06 | Studio · Map | studio.html#step3 | Web |
| W-07 | Studio · Prove | studio.html#step4 | Web |
| W-08 | Studio · Freeze | studio.html#step5 | Web |
| W-09 | Studio · Export | studio.html#step6 | Web |
| W-10 | Import 向导 | import.html | Web |
| W-11 | Shadow / 开写管控 | shadow.html | Web |
| W-12 | Drift 对账看板 | drift.html | Web |
| W-13 | 审计时间线 | audit.html | Web |
| W-14 | 执行证据链 | evidence.html | Web |
| H-00 | 产线终端入口 | h5_worker_entry.html | H5 |
| H-01 | 工人首页 | h5_worker_home.html | H5 |
| H-02 | 报工输入 | h5_worker_input.html | H5 |
| H-03 | 确认卡 | h5_worker_confirm.html | H5 |
| H-04 | 提交成功 | h5_worker_success.html | H5 |
| H-05 | 主管待办 | h5_worker_approve.html | H5 |
| H-06 | 主管确认 | h5_worker_supervisor_confirm.html | H5 |
| H-07 | 报工完成 | h5_worker_done.html | H5 |

### 4.2 架构附页（8 页 · 讲解用，建议建）

| 编号 | 墨刀页名 | 参考 HTML | 说明 |
|------|----------|-----------|------|
| S-01 | 制造全景 / 战略 | strategy.html | 平台先行三阶段 |
| S-02 | 产业连接概览 | integration.html | Path A/B/C 示意 |
| S-03 | 资产与复制概览 | business.html | Package / Scale-up |
| S-04 | 运营与合规概览 | workflow.html | 七步实施法 |
| S-05 | Gate 治理地图 | gate.html | 三门卡片 |
| S-06 | 核心模块架构 | core.html | os_core 10 模块 |
| S-07 | 数据架构 | data.html | Data-L0～L3 |
| S-08 | Shadow 监控（H5） | h5_worker_shadow.html | 影子期详情 |

### 4.3 可选页

| 编号 | 墨刀页名 | 参考 HTML |
|------|----------|-----------|
| O-01 | 报工历史 | h5_worker_history.html |
| O-02 | 移动预览壳 | mobile.html |

---

## 五、Web 管理台逐页规格

### W-01 登录

| 元素 | 类型 | 规则 / 文案 |
|------|------|-------------|
| Logo | 图形 | Ax OS |
| 企业账号 | 输入框 | 必填 |
| 密码 | 输入框 | 必填 |
| 租户 ID | 输入框 | 多租户必填 |
| 登录 | 主按钮 | → W-02 |
| 钉钉 / 企微 | 图标入口 | 品牌图标保留 |

### W-02 KPI 仪表盘（首页）

| 区域 | 元素 |
|------|------|
| 侧栏 | 五域母版；制造全景高亮 |
| 顶栏 | W-02 标识；ERP/Edge/Path 徽章 |
| KPI 四卡 | 今日报工 · 待确认 · 对账漂移 · Shadow 天数（14/14） |
| 快捷入口 | **进入 Studio** → W-03；查看门禁地图 → S-05；体验报工 → H-00 |
| 图表区 | 报工趋势、对账状态（占位即可） |
| 底链 | 查看全量审计日志 → W-13 |

### W-03 租户列表

| 元素 | 说明 |
|------|------|
| Studio 选租户区 | 哈森鞋业卡片高亮 → 进入 Studio Connect |
| 租户表格 | 租户名、Path、Shadow 状态、Pack |
| 主按钮 | 进入 Studio 配置 → W-04（或 studio 六步容器页） |

### W-04 Connect（Studio 步 1）

| 元素 | 说明 |
|------|------|
| 六步进度条 | 步 1 高亮 |
| 只读横幅 | `Connect 阶段只读摸底 · 禁止生产写 · secrets_ref` |
| Connector Pack | `conn-erp-kingdee-write`（哈森） |
| API Endpoint | 金蝶 URL |
| secrets_ref | `vault://tenant-hansen/erp`（非明文密钥） |
| Edge Agent | 在线状态 |
| 测试连通 | 按钮 → 成功提示 → 下一步 Discover |

### W-05 Discover（Studio 步 2）

| 元素 | 说明 |
|------|------|
| CMV 动词表 | 列：动词、Legacy 操作、置信度 |
| 样例行 | work_report · query_work_order · reconcile |
| 下一步 | → Map |

### W-06 Map（Studio 步 3）

| 元素 | 说明 |
|------|------|
| 映射表 | DSL 字段 ↔ ERP 字段 |
| AI 置信度 | 高/中/低标签 |
| idempotency_key | 映射说明 |
| 下一步 | → Prove |

### W-07 Prove（Studio 步 4）★ 重点

| 元素 | 说明 |
|------|------|
| 琥珀顶栏 | `shadow_mode=true · 影子模式 · simulated 不写 Legacy` |
| Shadow 进度 | 14/14 天 |
| 对账通过率 | 如 99.8% |
| 双签区 | 实施方签字 ✅ · 客户方对账双签（待签/已签） |
| 批准开写 | 按钮：**未满 14 天禁用 · 双签未完成禁用** |
| 下一步 | 双签完成后 → Freeze |

### W-08 Freeze（Studio 步 5）

| 元素 | 说明 |
|------|------|
| Graph 节点流 | START → Perceive → Confirm → RuleEval → Execute → END |
| 图名 | Hasen_Production_Flow_V1.0 |
| 冻结说明 | 须在 Prove 双签（G-WRITE-APPROVE）后冻结 |
| 签字人 | business_owner · G-FREEZE |
| 状态 | draft → frozen |
| 下一步 | → Export |

### W-09 Export（Studio 步 6）

| 元素 | 说明 |
|------|------|
| Package 信息 | 版本、sha256、含 Graph/Rule/Pack |
| 下载 Package | 按钮 |
| STU-R4/R5 说明卡 | Git 仅为镜像；第二家 import 为主 |
| 体验报工 | 按钮 → **H-00**（产线入口） |

### W-10 Import 向导（6 步可点）

| 步 | 名称 | 核心内容 |
|----|------|----------|
| 1 | Connect | **须更新新客户凭证**，不可复用源租户 |
| 2 | Package | 选哈森鞋业报工包 v1.2.0 |
| 3 | Override | 字段差异映射 |
| 4 | Delta | Workshop 差量 2 项 |
| 5 | Prove | 双签 **不可跳过** |
| 6 | Deploy | → Studio Prove |

### W-11 Shadow / 开写管控

| 元素 | 说明 |
|------|------|
| shadow_mode 开关 | 默认 true |
| write_approved 状态 | 与 Prove 联动 |
| 链接 | → Studio Prove (W-07) |

### W-12 Drift 对账看板

| 元素 | 说明 |
|------|------|
| 漂移列表 | 时间、工单、OS vs ERP 数量 |
| 处理状态 | 待处理 / 已解释 |
| 对账 Job | 每日自动 |

### W-13 审计时间线

| 元素 | 说明 |
|------|------|
| 事件流 | GRAPH_FREEZE · integration.write_approved · execution.* |
| 筛选 | 租户、时间、事件类型 |
| 导出 | 按钮 |

### W-14 执行证据链

| 元素 | 说明 |
|------|------|
| 6 步证据 | Plan → Confirm → Rule → Execute → Connector → Audit |
| Hash / Snapshot | 展示占位 |
| 单笔追溯 | 从报工链路跳入 |

### S-01～S-07 架构附页（摘要）

| 页 | 必含要点 |
|----|----------|
| S-01 strategy | 平台先行：1 平台 → 2 终端 → 3 项目；**禁止**阶段 2 与 Studio 并行 |
| S-02 integration | Path A/B/C 对比；Connector 层示意 |
| S-03 business | 第一家考古 vs 第二家 Import -85% 周期 |
| S-04 workflow | 七步实施法；Prove 在 Graph Freeze **之前**（Studio 序） |
| S-05 gate | 三门卡片顺序：**G-SHADOW → G-WRITE-APPROVE → G-FREEZE** |
| S-06 core | os_core 10 模块卡片 |
| S-07 data | Data-L0～L3 分层 |

---

## 六、H5 终端逐页规格

### H-00 产线终端入口

| 元素 | 跳转 |
|------|------|
| 三态图例 | 教学条 |
| 一线工人 | → H-01 |
| 班组长/主管 | → H-05 |
| 维修工 | 灰显 Phase 2+ |
| 返回管理台 | → W-02 |

### H-01 工人首页

| 元素 | 说明 |
|------|------|
| 顶栏 | shadow 三态条 |
| 用户信息 | 姓名、班组 |
| 四快捷入口 | 语音/扫码/拍照/手动 → H-02 |
| 当前工单卡 | 工单号、工序、计划数 |
| Shadow 入口 | → S-08 |

### H-02 报工输入

| 元素 | 说明 |
|------|------|
| 输入方式 | 语音波形 / 扫码框 / 数量步进器 |
| 工单号 | WO-2026-xxxx |
| 下一步 | → H-03 |

### H-03 确认卡

| 元素 | 说明 |
|------|------|
| 计划卡摘要 | 工单、数量、工序 |
| 可撤回说明 | 24h 内主管可撤回 |
| 确认提交 | → H-04 |

### H-04 提交成功

| 元素 | 说明 |
|------|------|
| 状态 | **仅**「待主管审批」；不写 ERP 成功 |
| 切换主管视角 | → H-05 |

### H-05 主管待办

| 元素 | 说明 |
|------|------|
| 顶栏 | write_approved=false |
| 待办列表 | 3 条；点一条 → H-06 |

### H-06 主管确认

| 元素 | 说明 |
|------|------|
| 报工详情 | 工人、数量、时间 |
| 批准 / 驳回 | 批准 → H-07 |

### H-07 报工完成

| 元素 | 说明 |
|------|------|
| 顶栏 | write_approved=true · 已写 Legacy |
| 对账一致 | 展示 |
| 返回管理台 | → W-02 |

---

## 七、Studio 六步容器页（可选合并方案）

若墨刀希望 **1 页内切换** 而非 6 独立页：

- 建 **W-STUDIO** 单页，顶部六步条可点击
- 每步内容区互斥显示（与 `studio.html` 一致）
- 热区：步条 1～6 + 每步「下一步」

---

## 八、热区连线总表（墨刀核心）

### 8.1 主线 A · 首家接入（UC-01）

```text
W-01 ─登录→ W-02 ─进入Studio→ W-03 ─选哈森→ W-04 → W-05 → W-06 → W-07 → W-08 → W-09
```

### 8.2 主线 B · 日常报工（UC-02）

```text
H-00 ─工人→ H-01 ─报工→ H-02 → H-03 ─确认→ H-04 ─切主管→ H-05 ─点待办→ H-06 ─批准→ H-07 ─返回→ W-02
```

### 8.3 主线 C · 第二家 Import（UC-03）

```text
S-03 或 W-10 ─步1→ 步2 → 步3 → 步4 → 步5(Prove) → 步6(Deploy) → W-07
```

### 8.4 主线 D · Gate 合规（UC-04）

```text
W-02 ─门禁地图→ S-05 ─Studio Prove→ W-07 ─Freeze→ W-08
```

### 8.5 跨端连线

| 从 | 元素 | 到 |
|----|------|-----|
| W-09 | 体验报工 | H-00 |
| H-07 | 返回管理台 | W-02 |
| H-00 | 返回链接 | W-02 |
| W-02 | 进入 Studio | W-03 |
| W-02 | 审计日志 | W-13 |
| S-04 | Import 向导 | W-10 |
| S-05 | 进入 Studio | W-03 |

### 8.6 侧栏全局跳转

| 侧栏项 | 默认目标 |
|--------|----------|
| 制造全景 | W-02 或 S-01 |
| 产业连接 | S-02 或 W-03 |
| 资产与复制 | S-03 或 W-10 |
| 运营与合规 | S-04 或 W-11 |
| 平台治理 | W-03 |

---

## 九、业务规则（原型须体现）

### 9.1 全局规则

| 编号 | 规则 | 原型体现 |
|------|------|----------|
| BR-01 | L2 写须 Graph frozen | Freeze 页状态 frozen |
| BR-02 | Rule 默认拒绝 | 无权限提示占位 |
| BR-03 | Agent 只出计划 | H-03 前无写成功 |
| BR-04 | 生产写须 write_approved | H5 三态条 |
| BR-05 | 新租户默认 shadow | W-07 琥珀条 |
| BR-06 | L2 写须 idempotency_key | Map 页字段 |
| BR-07 | 配置只经 Studio | 无「改 YAML」入口 |

### 9.2 人审 Gate

| Gate | 页面 | 签署人 | 顺序 |
|------|------|--------|------|
| G-SHADOW | W-07 | integrator | 1 |
| G-WRITE-APPROVE | W-07 | admin + business_owner | 2 |
| G-FREEZE | W-08 | business_owner | 3 |

### 9.3 STU 铁律（产业连接页脚须出现）

- **STU-R1**：published 配置仅经 Studio API
- **STU-R2**：实施顾问零仓库
- **STU-R3**：人审 Gate 须有界面动作 + Audit
- **STU-R4**：Git 仅为 export/fixture/CI 镜像
- **STU-R5**：第二家 import 向导为主路径

---

## 十、验收追溯矩阵（PRD ↔ 原型 ↔ 用例）

| 页面 | 覆盖用例 | 验收 ID |
|------|----------|---------|
| W-04～W-09 | UC-01 | STU-01～STU-06 |
| W-10 | UC-03 | STU-07 |
| W-07 | Shadow+双签 | STU-03、STU-04 |
| W-08 | Graph 冻结 | STU-05 |
| W-09 | Export | STU-06 |
| H-02～H-07 | UC-02 | UX M-01～M-06、H-01～H-05、T-01～T-03 |
| W-12 | UC-04 | T-06 |
| W-13～W-14 | 审计 | BASE Audit 相关 |

**D1 结案** = STU-001 + UX-001 + MVP-001 + BASE-001 四 Gate 同绿。

---

## 十一、墨刀搭建步骤（建议 1～2 天）

### Day 1 · 骨架

1. 新建项目，设 Web/H5 画布
2. 建侧栏母版 + H5 顶栏母版
3. 按 §4.1 建 21 核心页（可先截图 `factoryos-v2` 垫底）
4. 画 §8.1、§8.2 两条主线热区

### Day 2 · 完备

5. 补 §4.2 架构附页 8 页
6. Studio 六步进度条与 W-07 禁用态
7. Import 六步可点（或参考 import.html 交互）
8. 走一遍 §十二 演示脚本，断点修补

### 自检清单

- [ ] 21 核心页齐全
- [ ] 主线 A、B 无断点
- [ ] Gate 卡片顺序正确
- [ ] H5 三态条正确
- [ ] Prove 批准按钮有禁用态
- [ ] H-04 不写「ERP 已成功」
- [ ] 侧栏为五域行业文案
- [ ] 哈森 = Path A + Pool

---

## 十二、10 分钟演示脚本

| 分钟 | 内容 | 路径 |
|------|------|------|
| 0～1 | 登录 + 定位 | W-01 → W-02 |
| 1～5 | Studio 六步 + Gate | W-03 → W-09；穿插 S-05 |
| 5～8 | 报工闭环 | H-00 → H-07 |
| 8～9 | 对账审计 | W-12 → W-13 |
| 9～10 | 第二家 Import | W-10 简述 |

---

## 十三、与「复制给墨刀」的关系

| 方式 | 推荐度 | 说明 |
|------|--------|------|
| **本文 PRD + 设计师按表搭** | ★★★★★ | 最稳；热区可控 |
| 墨刀 AI 读本文生成 | ★★★★ | 快；需对照 factoryos-v2 校对 |
| 墨刀 MCP 导入 HTML | ★★★ | 适合单页；27 页要批量 |
| 仅复制本文不给 HTML | ★★★ | 可行但慢 |

**推荐组合**：本文 PRD 作需求真源 + `factoryos-v2/*.html` 作视觉参考 + 墨刀内热区按 §8 连线。

---

## 十四、修订记录

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-07-09 | Ax-OS-产品原型说明书 初版 |
| v1.1 | 2026-07-14 | 墨刀完整 PRD：34 页清单、逐页规格、热区表、三态条、Gate/STU 对齐 factoryos-v2 |

---

**使用方式**：全文复制到墨刀 AI 对话，或按 §4 逐页创建。**参考线框**：`docs/设计/factoryos-v2/` 同名 HTML。
