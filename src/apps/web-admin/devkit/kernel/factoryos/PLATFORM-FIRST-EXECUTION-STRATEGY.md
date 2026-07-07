# 执行策略（锁死）· 平台先行三阶段

> **版本** v1.0.0 · **状态**：**Locked**（2026-07-03 拍板）  
> **优先级**：与 [UI-FIRST-CONFIG-PRINCIPLE.md](./UI-FIRST-CONFIG-PRINCIPLE.md) 并列；**高于** `docs/准备/` 旧「P1 并行 H5+哈森」周表字面解读  
> **废止**：Gate 0 后立刻哈森生产接入 · Gate 0 后立刻钉钉 H5 · 三线并行（平台+终端+项目）

---

## 一、策略陈述（30 秒）

```text
Gate 0（os_core）✅
    → 阶段 1：平台打磨 ~80 分（Studio + API + Pack · STU-001）
    → 阶段 2：终端设计 ~80 分（H5/Harness · UX-001）
    → 阶段 3：项目验证（哈森 Path A · 四 Gate · 调策略）
```

**核心**：先把 **FactoryOS 当集成与治理平台** 做透；终端是第二层；真实项目是第三层压测。**不跳阶段。**

---

## 二、三阶段定义（硬 Gate）

### 阶段 1 · 平台打磨期（当前）

| 项 | 内容 |
|----|------|
| **目标** | 实施顾问 **零仓库** 完成 onboard；SaaS/私有化 **同一 Registry 模型** |
| **代码域** | `src/apps/web-admin` · `src/server/api/modules/integration|registry` · `src/integration/`（Pack 源码） |
| **禁止动** | `src/server/os_core/**`（`core-v1.0.0` 后仅 bugfix + ADR） |
| **禁止做** | `h5-worker` · 钉钉生产 · 哈森现场 · D1 结案 · 生产 L2 开写 |
| **80 分硬 Gate** | **[STU-001](../../docs/文档/验收/验收用例-STU-001-Studio配置主路径.md) P0 全绿** |
| **必须含** | Studio 六步 · Registry API · ≥1 ERP Pack 在 Studio 内 Shadow Prove · Package export/import 可演示 |

### 阶段 2 · 终端设计期

| 项 | 内容 |
|----|------|
| **前置** | 阶段 1 STU-001 已绿 |
| **目标** | 工人/主管走通 plan → confirm → execute；API 契约冻结 |
| **代码域** | `src/apps/h5-worker` · Harness 相关 `server/api` 路由 |
| **禁止做** | 改 os_core 写路径 · 为单厂 hardcode |
| **80 分硬 Gate** | **[UX-001](../../docs/文档/验收/验收用例-UX-001-终端体验与多模态.md) P0 全绿** |

### 阶段 3 · 项目验证期（哈森灯塔）

| 项 | 内容 |
|----|------|
| **前置** | 阶段 1 STU-001 + 阶段 2 UX-001 已绿 |
| **目标** | 证明平台+终端 **整体可用**；export Package；策略复盘 |
| **路径** | Path A：ERP 写+读 + 钉钉（不接 MES） |
| **硬 Gate** | **BASE + UX + MVP + STU 四 Gate 同过** → D1 可宣告 |
| **周期** | Shadow ≥14d · 客户 D1 窗 ≤90 天（**本阶段起算**，不含平台/终端研发期） |

---

## 三、与文档层级关系

```text
本策略（Locked）
    ↕ 同步
docs/准备/14-一年冲刺路线图.md §〇（三阶段）
    ↕
UI-FIRST · STU-001 · INTEGRATION-CHAIN · ADR-008
```

**冲突时**：本策略 > `14` 旧 §一④「立刻哈森+H5」> `14` §六 W3 钉钉（**延后至阶段 2**）。

---

## 四、研发纪律

| # | 纪律 |
|---|------|
| P1 | 新轮 Dev plan **必须声明**所处阶段（1/2/3） |
| P2 | 阶段 1 plan **不得**含 h5-worker、钉钉 OAuth、哈森 UAT |
| P3 | `tag core-v1.0.0` 为阶段 1 **开工前置**（若未打则 Step0 首项） |
| P4 | 阶段跨越须 **STU/UX 硬 Gate 绿** + 用户关键词 `可以继续` |
| P5 | 商业对外：阶段 1 称 **「平台 Beta / Studio 可演示」**；**不称** D1 结案 |

---

## 五、阶段 1 交付清单（复制到 plan）

- [ ] `web-admin` 脚手架 + `/studio/*` 路由
- [ ] `/v1/integration/*` 六步 API 补齐
- [ ] `/v1/registry/*` tenant/relation/change-request
- [ ] Path 模板 path-a/b/c
- [ ] 金蝶 Blueprint + Studio Connect/Map/Prove（Shadow）
- [ ] Graph/Rule freeze + 开写 Gate 上屏
- [ ] Package export/import
- [ ] STU-001 P0 pytest/手工验收全绿

---

## 六、参考

- [14-一年冲刺路线图](../../docs/准备/2026-06-16/14-一年冲刺路线图与并行研发.md)
- [Integration-Studio规格](../../docs/文档/规格说明/Integration-Studio规格.md) §0
- [PRE-DEV-CHAIN.md](./PRE-DEV-CHAIN.md)
