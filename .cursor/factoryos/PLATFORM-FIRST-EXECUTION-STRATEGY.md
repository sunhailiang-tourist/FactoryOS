# 执行策略（锁死）· 平台先行三阶段

> **版本** v1.1.0 · **状态**：**Locked**（2026-07-03 拍板 · **v1.1.0 细化 2026-07-07**）  
> **优先级**：与 [UI-FIRST-CONFIG-PRINCIPLE.md](./UI-FIRST-CONFIG-PRINCIPLE.md) 并列；**高于** `docs/准备/` 旧「P1 并行 H5+哈森」周表字面解读  
> **废止**：Gate 0 后立刻哈森生产接入 · Gate 0 后立刻钉钉 H5 · 三线并行（平台+终端+项目）

---

## 一、策略陈述（30 秒）

```text
Gate 0（os_core）✅
    → 阶段 1：平台打磨 ~80 分（Studio + API + Pack · STU-001）
         ├─ 1a STU-API：后端 + pytest 验收盘          ✅ 2026-07-07
         └─ 1b STU-UI：web-admin 六步真 API 联调     ← 当前
    → 阶段 2：终端设计 ~80 分（h5-worker · UX-001）   须 1a+1b 绿后
    → 阶段 3：项目验证（哈森 Path A · 四 Gate）         须 阶段2 绿后
```

**核心**：先把 **FactoryOS 当集成与治理平台** 做透（**含管理台 UI 联调**）；**h5-worker 终端是第二层**；真实项目是第三层压测。**不跳阶段、不跳 1b。**

---

## 二、三阶段定义（硬 Gate）

### 阶段 1 · 平台打磨期

| 项 | 内容 |
|----|------|
| **目标** | 实施顾问 **零仓库**、**仅 Studio + 浏览器** 完成 onboard；SaaS/私有化 **同一 Registry 模型** |
| **代码域** | `src/apps/web-admin` · `src/server/api/modules/integration\|registry\|package` · `src/integration/`（Pack 源码） |
| **禁止动** | `src/server/os_core/**`（`core-v1.0.0` 后仅 bugfix + ADR） |
| **禁止做** | **`h5-worker`** · 钉钉生产 · 哈森现场 · D1 结案 · 生产 L2 开写 |
| **80 分硬 Gate** | **[STU-001](../../docs/文档/验收/验收用例-STU-001-Studio配置主路径.md) P0 全绿**（**含 UI 主路径**，非仅 API pytest） |

#### 阶段 1a · STU-API（后端验收盘）— ✅ 2026-07-07

| 项 | 内容 |
|----|------|
| **范围** | `server/api` integration/registry/package · STU pytest **17/17** · `gate delivery`（API 切片） |
| **已交付** | 六步 API · path 模板 · Package export/import · audit 编排 · import 边界合规 |
| **刻意不含** | web-admin 业务页接真 API · 浏览器内走完 STU-01～07 |
| **状态** | **结案** · 不等于阶段 1 全结案 · **不等于可开阶段 2** |

#### 阶段 1b · STU-UI（Studio 浏览器联调）— **← 当前**

| 项 | 内容 |
|----|------|
| **范围** | `web-admin` `/studio/*` 六步页面接 **真 API**（非 MSW 主路径） |
| **前置** | WEB-PROFILE 基座已封存（`frontend-devkit 2.0.0-s5`）· STU-API 1a 已绿 |
| **验收盘** | `cd src/apps/web-admin && ./scripts/activate.sh` 绿 · STU-001 §一「仅 Studio + 浏览器」手工/E2E |
| **归属** | **仍属阶段 1 平台** · **不是** 阶段 2 终端 · **不是** WEB-PROFILE 基座轨 |
| **禁止** | 以「STU pytest 已绿」跳过 1b 直接开 `h5-worker` |

### 阶段 2 · 终端设计期

| 项 | 内容 |
|----|------|
| **前置** | **阶段 1a + 1b 均已绿**（STU-001 产品语义闭合） |
| **目标** | 工人/主管走通 plan → confirm → execute；API 契约冻结 |
| **代码域** | **`src/apps/h5-worker`** · Harness 相关 `server/api` 路由 |
| **禁止做** | 改 os_core 写路径 · 为单厂 hardcode |
| **80 分硬 Gate** | **[UX-001](../../docs/文档/验收/验收用例-UX-001-终端体验与多模态.md) P0 全绿** |

### 阶段 3 · 项目验证期（哈森灯塔）

| 项 | 内容 |
|----|------|
| **前置** | 阶段 1（1a+1b）+ 阶段 2 UX-001 已绿 |
| **目标** | 证明平台+终端 **整体可用**；export Package；策略复盘 |
| **路径** | Path A：ERP 写+读 + 钉钉（不接 MES） |
| **硬 Gate** | **BASE + UX + MVP + STU 四 Gate 同过** → D1 可宣告 |
| **周期** | Shadow ≥14d · 客户 D1 窗 ≤90 天（**本阶段起算**，不含平台/终端研发期） |

---

## 三、与文档层级关系

```text
本策略（Locked）
    ↕ 同步
docs/准备/14-一年冲刺路线图.md §〇（三阶段 + 1a/1b）
    ↕
UI-FIRST · STU-001 · WEB-PROFILE charter · INTEGRATION-CHAIN · ADR-008
```

**冲突时**：本策略 > `14` 旧 §一④「立刻哈森+H5」> `14` §六 W3 钉钉（**延后至阶段 2**）。

**次级文档**若仍写「Gate 0 后 Studio/H5 **并行**」→ 视为过期，以本策略 §一 为准。

---

## 四、研发纪律

| # | 纪律 |
|---|------|
| P1 | 新轮 Dev plan **必须声明**所处阶段（**1a / 1b / 2 / 3**） |
| P2 | 阶段 1 plan **不得**含 `h5-worker`、钉钉 OAuth、哈森 UAT |
| P3 | `tag core-v1.0.0` 为阶段 1 **开工前置**（若未打则 Step0 首项） |
| P4 | 阶段跨越须 **硬 Gate 绿** + 用户关键词 `可以继续` |
| P5 | 商业对外：阶段 1 称 **「平台 Beta / Studio 可演示」**；**不称** D1 结案 |
| **P6** | **1b STU-UI 属平台打磨**；**禁止** 以 STU-API pytest  alone 宣称「平台完成」或开 UX-001 |
| **P7** | WEB-PROFILE 验收盘 **不替代** 1b；1b 须独立 plan · Test · Verify |

---

## 五、阶段 1 交付清单（复制到 plan）

### 1a · STU-API（✅）

- [x] `/v1/integration/*` 六步 API
- [x] `/v1/registry/*` tenant/path-templates
- [x] Path 模板 path-a/b/c
- [x] Package export/import（`package_service`）
- [x] STU pytest 17/17 · integration 84/84

### 1b · STU-UI（待）

- [x] `web-admin` 脚手架 + `/studio/*` 路由（WEB-PROFILE）
- [ ] Studio 六步 **浏览器内** 接真 API（connect→discover→map→prove→freeze→export）
- [ ] 开写双签 / freeze **上屏**（STU-04/05 UI 语义）
- [ ] 第二家 import **界面为主**（STU-07 UI KPI）
- [ ] STU-001 §一「零仓库 · 仅 Studio + 浏览器」手工/E2E 闭合

---

## 六、参考

- [14-一年冲刺路线图](../../docs/准备/2026-06-16/14-一年冲刺路线图与并行研发.md)
- [Integration-Studio规格](../../docs/文档/规格说明/Integration-Studio规格.md) §0
- [WEB-PROFILE charter](../../_factoryos_pipeline/2026-07-06/plan/plan-web-admin-profile-autonomy.md) §4（联调 = 1b）
- [PRE-DEV-CHAIN.md](./PRE-DEV-CHAIN.md)
