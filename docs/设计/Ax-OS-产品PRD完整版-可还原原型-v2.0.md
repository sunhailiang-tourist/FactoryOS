# Ax OS · 产品 PRD 完整版（可还原原型 · 可落地功能）

| 项 | 内容 |
|----|------|
| **产品名称** | Ax OS（FactoryOS 管理端品牌）· 产线端 h5-worker |
| **文档类型** | 资深 PM 级完整 PRD（原型规格 + 功能规格 + 验收追溯） |
| **版本** | **v2.1**（兜底核对修订） |
| **日期** | 2026-07-14 |
| **状态** | Accepted（全库 212 文件通读 + 像素核对 + 硬对账修订） |
| **配对战略** | [Ax-OS-平台定位与战略白皮书-v1.0.md](./Ax-OS-平台定位与战略白皮书-v1.0.md)（内容版本 **v1.1**） |
| **真源优先级** | ADR-000～008 > 18-一致性矩阵 > Integration-Studio / Playbook / STU·UX·MVP·BASE > **本文** > 早期 PNG/草稿 |
| **线框参考** | `docs/设计/factoryos-v2/*.html`（27 页） |
| **高保真登录** | `docs/设计/ax-os-ui/ax-os-login-v4-smart-hub.png` |
| **Token** | `docs/设计/figma/design-tokens.json` |

---

## 〇、给其他 AI / 设计师 / 前端的使用协议

### 0.1 本文能做什么

| 角色 | 用法 |
|------|------|
| **墨刀 / Axure / Figma AI** | 按 §4 建页 → §5～§6 摆元素 → §8 连热区；对照 factoryos-v2 同名 HTML |
| **前端** | §7 状态机 + §10 API 接线 + §11 验收 ID + §3.5 DSL 动词 实现功能 |
| **产品评审** | §1～§3 定义范围；§12 分期；§13 矛盾登记避免用错素材 |

### 0.2 绝对禁止（原型与实现）

1. Agent / 计划卡阶段展示「已写 ERP 成功」  
2. Connect 阶段出现生产写按钮  
3. 跳过 Prove 双签直接 Freeze / Export  
4. 侧栏使用工程模块名（`graph_service` 等）  
5. 界面明文密钥（必须 `secrets_ref`）  
6. 采用已废止 IA（工作台/集成工作室…）或废止六步（Simulate/Publish…）  
7. 登录使用「让制造不再黑箱」文案（设计稿禁用）

### 0.3 墨刀 / Figma 项目设置

| 项 | 值 |
|----|-----|
| 项目名 | Ax OS 智能中枢系统 · 产品原型 v2.0 |
| Web 画布 | 1440 × 900 |
| H5 画布 | 375 × 812（或 390 × 844） |
| 风格 | 深色；线框可先灰底；高保真跟 Token |
| 图标 | Phosphor `ph:*`（与 factoryos-v2 一致） |
| 侧栏宽 | 240px · 顶栏高 56px |

### 0.4 全局母版

**Web 侧栏五域（唯一 IA）**

| 序 | 文案 | 默认落地页 |
|----|------|------------|
| 1 | 制造全景 | W-02 kpi_dashboard / S-01 strategy |
| 2 | 产业连接 | S-02 integration / W-03 tenants → Studio |
| 3 | 资产与复制 | S-03 business / W-10 import |
| 4 | 运营与合规 | S-04 workflow / W-11 shadow |
| 5 | 平台治理 | W-03 tenants |

**顶栏品牌**：`Ax OS · 智能中枢系统`  
**灯塔徽章（哈森默认）**：`ERP 金蝶 ✅` · `Edge 在线` · `Path A · Pool`

**H5 顶栏三态（互斥 · 每页只显一种）**

| 状态 | 文案 | 色 |
|------|------|-----|
| `shadow_mode=true` | `⚠️ 影子运行 · simulated only · 生产写禁用` | 琥珀 `#FFB300` |
| `write_approved=false` | `🔒 生产写未批准 · Connector 写禁用` | 灰/锁 |
| `write_approved=true` | `✅ 生产写已批准 · 已写 Legacy` | 绿 `#00E676` |

---

## 一、产品概述

### 1.1 定位

**Ax OS = 制造业智能中枢 Overlay**：在客户 ERP/MES 之上，提供 **敢写、可追、可回滚** 的 AI 执行能力。

| 是 | 不是 |
|----|------|
| Governed AI Overlay | ERP 替代品 |
| 冻结链路 + 规则 + 审计 + 撤回 | 无治理聊天机器人 |
| 第一家 Export、第二家 Import | 装完离场 |
| 单登录 + RBAC 裁剪菜单 | 两套 Admin 门户 |

详见战略白皮书 §2。

### 1.2 产品形态

```text
web-admin（Ax OS） ─┐
                    ├── os_core ──► Legacy ERP/MES（或 Path C 内置账本）
h5-worker（产线 H5）─┘
```

### 1.3 产品目标与 KPI

| 目标 | 度量 |
|------|------|
| D1 结案 | 五机制 + 报工 + Package |
| 实施零仓库 | STU-01 |
| 工人愿意用 | P50 ≤30s；≤3 tap |
| 敢开写 | Shadow≥14d + 双签 + 零未解释 drift |
| 第二家复制 | Import ≤3 周（Silver） |

### 1.4 D1 五机制（原型与文案必须可指出）

只读查询 · 受控写 · 全审计 · 可撤回 · 每日对账

---

## 二、用户与场景

### 2.1 角色矩阵

| 角色 | 代码 | 入口 | 核心任务 |
|------|------|------|----------|
| 工人 | `role:worker` | h5-worker | 报工、查本单 |
| 主管 | `role:supervisor` | H5 待办 | 确认/驳回/24h 撤回 |
| 业务负责人 | `business_owner` | Studio Prove/Freeze | 双签、冻结、UAT |
| 实施顾问 | `integrator` | Studio 六步 | 接入、映射、导出/导入 |
| 客户 IT | `customer_it` | Connect | 凭证、Edge、私网 |
| 租户管理员 | `admin` | 运营域 | Shadow、开写批准 |
| 运维 | `ops` | 运营域 | Drift、熔断、审计 |
| 老板 | `boss` | 看板（Phase 2） | 只读问数 |
| 平台研发 | `platform` | CLI/guide（内部） | 非客户路径 |

### 2.2 用例主线

| ID | 场景 | 墨刀主线 | Gate |
|----|------|----------|------|
| UC-01 | 首家接入 | A：W-01→W-09 | STU |
| UC-02 | 日常报工 | B：H-00→H-07 | UX+MVP |
| UC-03 | 第二家 Import | C：W-10 | STU-07 |
| UC-04 | Gate/合规/对账 | D：S-05→W-12/13 | BASE 相关 |

---

## 三、功能与信息架构

### 3.1 五域功能树

```text
Ax OS web-admin
├── 制造全景（看）
│   ├── KPI 仪表盘
│   ├── 战略/平台先行说明（附页）
│   └── 工单/异常（D1+，非 Stage1 必做）
├── 产业连接（接）★
│   ├── 集成概览 Path A/B/C
│   ├── 租户入口
│   └── Studio：Connect→Discover→Map→Prove→Freeze→Export
├── 资产与复制（复制）
│   ├── Package 说明
│   └── Import 向导（6 步）
├── 运营与合规（管）
│   ├── Shadow / 开写
│   ├── Drift 对账
│   ├── 审计时间线
│   ├── 执行证据链
│   └── Gate 地图
└── 平台治理（SaaS）
    ├── 租户
    └── License / Pack（可后置）

h5-worker
├── 角色入口（工人/主管）
├── 多模态报工 → 确认 → 待主管 → 批准 → 完成
├── Shadow 状态附页
└── 报工历史（可选）
```

### 3.2 Studio 六步（产业连接主路径）

| 步 | ID | 产出 | 禁止 |
|----|-----|------|------|
| 1 | Connect | 连通报告 · secrets_ref · Edge 状态 | 任何生产写 |
| 2 | Discover | CMV 动词表 | — |
| 3 | Map | 字段映射 · idempotency_key | AI 建议不经人确认直生效 |
| 4 | Prove | Shadow≥14d · Contract Test · 对账 · **双签开写** | 未满 14d / 未双签批准 |
| 5 | Freeze | Graph `frozen` + checksum | Prove 未完成就冻结开写链路 |
| 6 | Export | Implementation Package JSON | 含 secrets |

### 3.3 Path × 部署

| Path | 写目标 | 默认 Pack |
|------|--------|-----------|
| A | ERP | `conn-erp-kingdee-write` + read + dingtalk |
| B | MES | `conn-mes-*` + erp read |
| C | builtin | `conn-mes-builtin` |

部署：Pool / Bridge / Silo（哈森演示默认 Path A + Pool）。

### 3.4 os_core → 用户感知（10 模块）

| 模块 | 用户感知 |
|------|----------|
| shared_contracts | 错误码 / Schema 一致（用户见 CODE·中文） |
| platform_registry | Studio 全部配置真源 |
| graph_service | 未冻结不能生产写 |
| rule_engine | 无权 / 允许提示 |
| execution_service | success / simulated / failed / reverted |
| audit_service | 时间线 |
| connector_sdk | 在线 / 熔断 |
| mcp_gateway | 外部工具仍走同一写路径 |
| agent_orchestrator | 计划卡（未执行） |
| license_service | 未购模块 403 |

> `integration/` 为 GIP 外置目录（catalog/packs），**不是**第 11 个 os_core 业务写模块。

### 3.5 D1 MVP DSL 动词（报工闭环 · 必须出现在 Map/确认卡）

| 动词 | 用途 | 用户可见 |
|------|------|----------|
| `QUERY_WO` | 查工单 | H-01 当前工单 |
| `WORK_REPORT` | 报工写 | H-03～H-07 |
| `WORK_REPORT_REVERT` | ≤24h 撤回 | 主管操作 / 运营域 |
| `QUERY_REPORT_HISTORY` | 报工历史 | O-01 |

### 3.6 Studio RBAC（原型必须体现）

| 角色 | Studio | 说明 |
|------|--------|------|
| `integrator` | Connect～Export | 实施主路径 |
| `admin` | + shadow / 开写相关 | W-11 |
| `business_owner` | Prove 双签 · Freeze | 人审 |
| `operator` | **403** | 无 Studio |

---

## 四、页面清单（共 **32** 墨刀页 = 核心 22 + 附页 8 + 可选 2）

> 每一行 = 墨刀/Figma 独立一页。参考 HTML：`docs/设计/factoryos-v2/<文件>`（**27 个文件**；Studio 六步合于 `studio.html` 一页多态）。  
> 历史「34 / 21」为上游笔误；本版以实际编号清点为准。

### 4.1 核心交付页（**22** · 验收必含）

| 编号 | 墨刀页名 | HTML | 画布 | 角色 |
|------|----------|------|------|------|
| W-01 | 登录 | login.html | Web | 全员 |
| W-02 | KPI 仪表盘 | kpi_dashboard.html | Web | 全员只读+ |
| W-03 | 租户 / Studio 入口 | tenants.html | Web | integrator/admin |
| W-04 | Studio · Connect | studio.html#step1 | Web | integrator |
| W-05 | Studio · Discover | studio.html#step2 | Web | integrator |
| W-06 | Studio · Map | studio.html#step3 | Web | integrator |
| W-07 | Studio · Prove | studio.html#step4 | Web | admin+owner |
| W-08 | Studio · Freeze | studio.html#step5 | Web | business_owner |
| W-09 | Studio · Export | studio.html#step6 | Web | integrator |
| W-10 | Import 向导 | import.html | Web | integrator |
| W-11 | Shadow / 开写 | shadow.html | Web | admin |
| W-12 | Drift 对账 | drift.html | Web | ops |
| W-13 | 审计时间线 | audit.html | Web | ops/admin |
| W-14 | 执行证据链 | evidence.html | Web | ops |
| H-00 | 产线入口 | h5_worker_entry.html | H5 | 工人/主管 |
| H-01 | 工人首页 | h5_worker_home.html | H5 | worker |
| H-02 | 报工输入 | h5_worker_input.html | H5 | worker |
| H-03 | 确认卡 | h5_worker_confirm.html | H5 | worker |
| H-04 | 提交成功（待审批） | h5_worker_success.html | H5 | worker |
| H-05 | 主管待办 | h5_worker_approve.html | H5 | supervisor |
| H-06 | 主管确认 | h5_worker_supervisor_confirm.html | H5 | supervisor |
| H-07 | 报工完成 | h5_worker_done.html | H5 | supervisor |

### 4.2 架构附页（8 · 讲解建议建）

| 编号 | 页名 | HTML |
|------|------|------|
| S-01 | 制造全景 / 战略 | strategy.html |
| S-02 | 产业连接概览 | integration.html |
| S-03 | 资产与复制 | business.html |
| S-04 | 运营与合规 / 七步 | workflow.html |
| S-05 | Gate 地图 | gate.html |
| S-06 | 核心模块 | core.html |
| S-07 | 数据架构 | data.html |
| S-08 | H5 Shadow 监控 | h5_worker_shadow.html |

### 4.3 可选页（2）

| 编号 | 页名 | HTML |
|------|------|------|
| O-01 | 报工历史 | h5_worker_history.html |
| O-02 | 移动预览壳 | mobile.html |

### 4.4 bak1 → v2 差异（落地以 v2）

| v2 新增 | 说明 |
|---------|------|
| kpi_dashboard.html | 正式首页 KPI |
| tenants.html | 租户/治理入口 |
| h5_worker_input.html | 报工输入独立页 |
| h5_worker_supervisor_confirm.html | 主管确认独立页 |
| h5_worker_done.html | 完成后台写 Legacy |

---

## 五、Web 管理台逐页规格

### W-01 登录（高保真对齐 V4）

**构图**：左表单 + 右 Hero（中枢球连接 ERP/MES/WMS/PLM/OA）

| 元素 | 规则 |
|------|------|
| Logo | Ax 几何标（青蓝渐变） |
| 主标题 | **智能中枢系统**（非「制造业数字中枢」） |
| 副标 | AI 时代 · 全域连接 · 全程可追 |
| 英文 | The Axis of Modern Manufacturing |
| 企业账号 / 密码 / 租户 ID | 必填 |
| 登录 | → W-02 |
| 底注 | 私有化部署 · 多租户 SaaS |
| 价值标签（右屏） | 打破孤岛 · 执行可管 · 决策可追 · AI 降复杂度 |
| **禁用** | 「让制造不再黑箱」顶栏文案 |

**视觉 Token**：bg `#0A0E1A` · primary `#00D4FF` · text `#F0F4FF`

### W-02 KPI 仪表盘

| 区域 | 内容 |
|------|------|
| 侧栏 | 五域；制造全景高亮 |
| 顶栏 | 租户选择 · 徽章 ERP/Edge/Path |
| KPI 四卡 | 今日报工 · 待确认 · 对账漂移 · Shadow 天数（如 14/14） |
| 快捷 | 进入 Studio → W-03；门禁地图 → S-05；体验报工 → H-00 |
| 图表 | 报工趋势 / 对账状态（可占位） |
| 底链 | 全量审计 → W-13 |

> **注意**：`ax-os-home-dashboard.png` 的「工作台/集成工作室」IA **作废**；KPI 语义可参考，导航必须五域。

### W-03 租户列表

- 哈森鞋业卡片高亮（Path A · Shadow 状态 · Pack）  
- 主 CTA：进入 Studio → W-04  
- `role:operator` 访问 Studio → 403 占位错误卡

### W-04 Connect

| 元素 | 说明 |
|------|------|
| 六步进度 | 步 1 高亮 |
| 只读横幅 | Connect 阶段禁止生产写 · secrets_ref |
| Pack | `conn-erp-kingdee-write` |
| Endpoint | 金蝶 URL |
| secrets_ref | `vault://tenant-hansen/erp` |
| Edge | 在线/离线灯 |
| 测试连通 | 成功 → Discover |
| API | `POST /v1/integration/connect/test` |

### W-05 Discover

- CMV 表：动词 · Legacy 操作 · 置信度  
- 样例行：`work_report` · `query_work_order` · `reconcile`  
- API：`POST /v1/integration/discover` · `.../blueprint/validate`

### W-06 Map

- DSL 字段 ↔ ERP 字段对照表  
- AI 置信度高/中/低；须人点确认  
- 标明 `idempotency_key`  
- API：`PUT /v1/integration/mappings/{packId}`

### W-07 Prove ★（最重要人审页）

| 区块 | 内容 |
|------|------|
| 琥珀顶栏 | shadow_mode=true · simulated 不写 Legacy |
| Shadow 进度 | n/14 天；未满禁用批准 |
| Contract Test | 全绿才允许双签 |
| 对账 | ok / drift；有未解释 drift 禁止双签 |
| 双签 | 租户管理员 + 业务负责人 |
| 批准生产写 | 双签前 disabled |
| API | `POST /v1/integration/prove/run` · `PUT /v1/tenants/{id}/settings` |

> Figma prove 参考图六步若为 Connect/Map/Simulate/Prove/Publish/Monitor → **忽略步进文案**，只借 Shadow/双签布局。

### W-08 Freeze

- Graph 节点：Perceive → Confirm → RuleEval → Execute  
- 状态机可视化：`draft → in_review → frozen → deprecated`  
- 仅 `frozen` 可 L2 写  
- 签字人 business_owner · Audit `GRAPH_FREEZE`  
- API：`POST /v1/graphs/.../freeze`

### W-09 Export

- Package 版本 / sha256 / 含 Graph·Rule·Pack（无 secrets）  
- 下载按钮 · STU-R4/R5 说明（Git 仅为镜像）  
- 「体验报工」→ H-00  
- API：`POST /v1/packages/export`

### W-10 Import（6 步可点）

1. Connect（**更新新客户凭证**，禁复用源租户 secrets）  
2. Package（选哈森包版本）  
3. Override  
4. Delta（workshop 差量）  
5. Prove（**不可跳过**）  
6. Deploy → 回到 W-07 语义  

API：`POST /v1/packages/import`

### W-11 Shadow / 开写

- `shadow_mode` 默认 true  
- `write_approved` 与 Prove 联动只读展示 + 深链 W-07  

### W-12 Drift

- 列表：时间 · 工单 · OS vs ERP 数量 · 待处理/已解释  
- 每日 Job；有 drift → 可提示冻结新写  

### W-13 审计

- 事件：`GRAPH_FREEZE` · `integration.write_approved` · `execution.*`  
- 筛选租户/时间/类型 · 导出  

### W-14 证据链

- Plan → Confirm → Rule → Execute → Connector → Audit  
- Hash / Snapshot 占位  

### S-01～S-07 附页要点

| 页 | 必含 |
|----|------|
| S-01 | 平台先行：1 平台 → 2 终端 → 3 项目；禁阶段 2 与 Studio 并行 |
| S-02 | Path A/B/C |
| S-03 | 第一家考古 vs 第二家 Import -85% |
| S-04 | 七步实施；Prove 在 Freeze 前 |
| S-05 | 三门顺序 **G-FREEZE → G-SHADOW → G-WRITE-APPROVE**（2026-07-15 裁定 · 见 `.cursor/factoryos/PM-GATES.md`） |
| S-06 | os_core 模块卡片 |
| S-07 | Data-L0～L3 |

---

## 六、H5 终端逐页规格

### H-00 入口

- 三态图例教学条  
- 一线工人 → H-01；班组长 → H-05；维修工灰显 Phase2+  
- 返回管理台 → W-02  

### H-01 工人首页

- 顶栏 shadow 态  
- 用户/班组 · 当前工单卡  
- 四入口：语音/扫码/拍照/手动 → H-02  
- Shadow 详情 → S-08  

### H-02 输入

- 工单号 · 数量步进 / 语音波形 / 扫码框  
- 低置信 → 强制澄清或大键盘（不可直接执行）  
- 下一步 → H-03  

### H-03 确认卡（计划卡 · 未执行）

必显：动作摘要 · 工单 · **大字数量** · 24h 可撤回说明 · 感知来源（语音转写/缩略图）  
确认 → H-04（**仍未写 Legacy**）

### H-04 提交成功

- **仅**「待主管审批」  
- **禁止**「ERP 已成功」  
- 切主管视角 → H-05  

### H-05 主管待办

- 顶栏 `write_approved=false`（若尚未开写）或业务态  
- 列表点入 → H-06  

### H-06 主管确认

- 详情：工人 · 数量 · 时间  
- 批准 → H-07；驳回 → 无写 + Audit  

### H-07 完成

- 顶栏 `write_approved=true · 已写 Legacy`  
- 对账一致展示  
- 返回 W-02  

---

## 七、业务规则与状态机

### 7.1 全局业务规则

| ID | 规则 | 原型体现 |
|----|------|----------|
| BR-01 | L2 写须 Graph frozen | Freeze 状态 |
| BR-02 | Rule 默认拒绝 | 无权限卡 |
| BR-03 | Agent 只出计划 | H-03 前无写成功 |
| BR-04 | 生产写须 write_approved | H5 三态 |
| BR-05 | 新租户默认 shadow | W-07 琥珀条 |
| BR-06 | L2 须 idempotency_key | Map 页 |
| BR-07 | 配置只经 Studio | 无改 YAML 入口 |

### 7.2 Graph 状态

```text
draft → in_review → frozen → deprecated
```

仅 `frozen` 允许 L2 写；frozen 不可原地改（clone 新版本）。

### 7.3 执行状态（用户可见）

| status | 含义 | UI |
|--------|------|-----|
| simulated | Shadow/dry_run | 琥珀 |
| success | 已写 Legacy | 绿 |
| failed | 失败 | 红 + CODE |
| reverted | 已撤回 | 灰/蓝 |

### 7.4 STU 铁律（产业连接页脚常驻）

- STU-R1 published 仅经 Studio API  
- STU-R2 实施零仓库  
- STU-R3 人审 Gate 有界面动作 + Audit  
- STU-R4 Git 仅为镜像  
- STU-R5 第二家以 Import 向导为主  

### 7.5 错误展示

格式：`CODE · 中文说明`

| Code | 场景 |
|------|------|
| AUTH_STUDIO_FORBIDDEN | 无权限进 Studio |
| RULE_DENIED | 规则拒绝 |
| GRAPH_NOT_FROZEN | 未冻结就写 |
| INT_SHADOW_REQUIRED | shadow 下禁止真写 |
| MODULE_NOT_LICENSED | 未购 Pack |
| EDGE_OFFLINE | Edge 断连 |
| MAPPING_ERROR | 映射错误 |

---

## 八、热区连线总表

### 8.1 主线 A · 首家接入

```text
W-01 → W-02 → W-03 → W-04 → W-05 → W-06 → W-07 → W-08 → W-09
```

### 8.2 主线 B · 报工

```text
H-00 → H-01 → H-02 → H-03 → H-04 → H-05 → H-06 → H-07 → W-02
```

### 8.3 主线 C · Import

```text
W-10 步1→…→步5 Prove → 步6 → W-07
```

### 8.4 主线 D · Gate

```text
W-02 → S-05 → W-07 → W-08
```

### 8.5 跨端

| 从 | 到 |
|----|-----|
| W-09 体验报工 | H-00 |
| H-00 / H-07 返回 | W-02 |
| W-02 审计 | W-13 |

---

## 九、设计系统（Token）

摘自 `figma/design-tokens.json`（实现禁止裸 hex 散落）：

| Token | 值 |
|-------|-----|
| `--ax-bg-default` | `#0A0E1A` |
| `--ax-bg-paper` | `rgba(15,22,40,0.72)` |
| `--ax-primary` | `#00D4FF` |
| `--ax-primary-deep` | `#1565C0` |
| `--ax-text-primary` | `#F0F4FF` |
| `--ax-border-glow` | `rgba(0,212,255,0.25)` |
| status.shadow | `#FFB300` |
| status.frozen / online | `#00E676` |
| status.drift / offline | `#FF5252` |
| radius.md | 12px |
| spacing.unit | 8px |
| font | Inter / PingFang SC |

**组件必做变体**：Path 徽章 A/B/C · Gate 进度 1–6 · Shadow 条 · Edge 灯 · ConfirmCard worker/supervisor · 错误卡

---

## 十、API 接线速查（功能落地）

| 页面 | 端点 |
|------|------|
| W-04 | `POST /v1/integration/connect/test` |
| W-05 | `POST /v1/integration/discover` · `.../blueprint/validate` |
| W-06 | `PUT /v1/integration/mappings/{packId}` |
| W-07 | `POST /v1/integration/prove/run` · `PUT /v1/tenants/{id}/settings` |
| W-08 | `POST /v1/graphs/{id}/versions/{v}/freeze` |
| W-09 | `POST /v1/packages/export` |
| W-10 | `POST /v1/packages/import` |
| H-02～H-03 | `POST /v1/perception/*` → `/v1/agent/plan` |
| H-03～H-06 | `POST /v1/harness/confirm` → `/v1/execute` |
| W-12 | `POST /v1/reconciliation/run` |
| W-13 | `GET /v1/audit/events` |
| W-14 | `GET /v1/executions/{id}/evidence` |

OpenAPI 镜像：`docs/文档/接口/工厂操作系统-v1.1.yaml`（published 真源 = Contract Registry）。

---

## 十一、验收追溯矩阵

| 页面/能力 | 验收 ID |
|-----------|---------|
| W-04～W-09 | STU-01～STU-06 |
| W-10 | STU-07 |
| W-07 双签/Shadow | STU-03、STU-04 |
| W-08 | STU-05 |
| Path 模板 | STU-10 |
| H-02～H-07 | UX M-01～M-06、H-01～H-05 |
| 报工落账 Path A/B | MVP A-*/B-* |
| Graph/Rule/Audit/Revert | BASE G-*/R-*/E-* |
| B-Lite | BL-01～BL-07 |

**D1 结案 = BASE-001 + UX-001 + MVP-001 + STU-001 四 Gate 同绿。**

---

## 十二、研发分期（功能落地顺序）

```text
1b-0  壳 + Token + IA（W-01/W-02）
1b-1  Connect + Discover
1b-2  Map + Prove（人审最重）
1b-3  Freeze + Export + Import
Stage2  h5-worker H-00～H-07
Stage3  哈森 Path A 真实写 + 钉钉 + Shadow/UAT
```

对齐战略：阶段 1b → 2 → 3；禁止 Stage2 与未完成 Studio 抢跑。

---

## 十三、素材矛盾登记（AI 必读）

| 素材 | 问题 | 用法 |
|------|------|------|
| 墨刀完整 PRD v1.1 | 写「34/21」页 | **以本 PRD v2.1 的 32=22+8+2 为准** |
| ax-os-home-dashboard.png | IA 非五域 | **禁止**抄侧栏 |
| login-v3 | 禁用 slogan | **禁止**；用 V4 |
| figma prove-ref | 六步名错误 | 只借 Prove 区布局 |
| figma dashboard-ref | 子导航偏 MES 全家桶 | Stage1 只保留 KPI 四卡+连接徽章 |
| factoryos-v2-bak1 | 缺 KPI/租户/部分 H5 | 历史；以 v2 为准 |
| 09「双轨并行」 | 已废止为执行主口径 | 执行跟 14 PLATFORM-FIRST |

---

## 十四、10 分钟演示脚本

| 分 | 内容 | 路径 |
|----|------|------|
| 0–1 | 登录+定位 | W-01→W-02 |
| 1–5 | Studio+Gate | W-03→W-09 + S-05 |
| 5–8 | 报工闭环 | H-00→H-07 |
| 8–9 | 对账审计 | W-12→W-13 |
| 9–10 | Import | W-10 简述 |

---

## 十五、原型自检清单

- [ ] **22** 核心页齐全；主线 A/B 无断点  
- [ ] 侧栏五域行业文案（与 factoryos-v2 全站一致）  
- [ ] Studio 六步名正确：Connect→Discover→Map→Prove→Freeze→Export；Prove 在 Freeze 前  
- [ ] Prove：14 天 / Contract Test / 对账 / 双签 / 批准禁用态  
- [ ] H5 三态条正确；H-04 不写 ERP 成功  
- [ ] secrets_ref 无明文；operator 进 Studio 见 403  
- [ ] 哈森 = Path A + Pool；Starter-A Pack 组合可见  
- [ ] 登录对齐 V4 文案与构图（智能中枢系统）  
- [ ] 错误态每关键页至少 1 Variant  
- [ ] MVP 四动词 QUERY_WO / WORK_REPORT / WORK_REPORT_REVERT / QUERY_REPORT_HISTORY 可指认  

---

## 十六、附录

### A. 相关文档

| 类型 | 路径 |
|------|------|
| 战略白皮书 v1.1 | `docs/设计/Ax-OS-平台定位与战略白皮书-v1.0.md` |
| 墨刀 PRD v1.1 | `docs/设计/Ax-OS-墨刀完整PRD-v1.1.md` |
| 设计稿 | `docs/设计/Ax-OS-产品设计稿-v1.0.md` |
| 线框 HTML | `docs/设计/factoryos-v2/`（27 文件，页 ID 全覆盖） |
| Studio 规格 | `docs/文档/规格说明/Integration-Studio规格.md` |
| Playbook | `docs/文档/规格说明/人工决策Playbook.md` |
| 终端体验 | `docs/文档/规格说明/Harness终端体验.md` |
| 核心模块 | `docs/文档/架构/核心模块架构图说明.md`（10 os_core） |

### B. 兜底核对结论（v2.1）

| 检查项 | 结果 |
|--------|------|
| factoryos-v2 27 HTML ↔ PRD 页表 | ✅ 双向零遗漏 |
| 五域 IA 全站出现 | ✅ 各域 ≥15 处命中 |
| Studio 六步 vs Integration-Studio 规格 | ✅ 一致 |
| 登录 V4 像素文案 | ✅ 智能中枢系统 · 三字段 · 私有化/SaaS |
| 废止素材门禁（V3 IA / 错误六步） | ✅ §13 已钉死 |
| 状态机章节交叉引用 | ✅ 已修正（§7） |
| 页数算术 | ✅ 已改为 32=22+8+2（废止错误 34/21） |
| 10 模块 / DSL 四动词 / RBAC | ✅ 已补 §3.4～3.6 |
| 设计 AI 可否还原主线原型 | ✅ **可以**（主线 A/B/C/D + Token + 热区 + 禁用态） |
| 前端可否按 PRD 落地功能 | ✅ **可以**（API 表 + 验收 ID + 状态机）；细字段以 OpenAPI/Schema 为补充真源 |

### C. 修订记录

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-07-09 | 原型说明书 / 设计稿 / 墨刀 PRD 分册 |
| v1.1 | 2026-07-14 | 墨刀完整 PRD 对齐 factoryos-v2 |
| v2.0 | 2026-07-14 | 全库通读合成首版 |
| **v2.1** | **2026-07-14** | **兜底核对修订**：页数校正、交叉引用、10 模块、DSL/RBAC、自检与核对结论 |
| v2.1.1 | 2026-07-15 | S-05 人审三门裁定为 **G-FREEZE → G-SHADOW → G-WRITE-APPROVE**；挂载 `【PM模式启动】` / `PM-GATES.md` |

---

**使用方式**：将本文作为 Prompt/规格真源；视觉对照 `factoryos-v2` 与 V4 登录图；实现对照 §10 API 与 §11 验收。  
**战略口径**：配对白皮书 v1.1。  
**产品 Agent**：`【PM模式启动】` → `.cursor/factoryos/PM-GATES.md`。  
**判定**：两份文档合用，**足以**让产品设计 AI 还原契合项目的原型，并支撑按原型落地功能。
