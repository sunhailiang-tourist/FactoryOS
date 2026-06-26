# 集成平台化战略（GIP）

> 版本：**v1.0.0** | 日期：2026-06-16  
> 状态：**Accepted**（与 ADR-004 同步）  
> 关联：[16-OS核心基座架构设计方案](./16-OS核心基座架构设计方案.md) · [ADR-004](../../文档/架构/架构决策记录-004-集成平台化GIP.md) · [08-平台战略与两次交付模型](./08-平台战略与两次交付模型.md) · [07-行业痛点与顶级平台差距分析](./07-行业痛点与顶级平台差距分析.md)

---

## 一、战略定位

### 1.1 GIP 是什么

**GIP（Governed Integration Platform）** = FactoryOS **Platform-L1** 的工程化战略：在 **不改动 L0 信任内核** 的前提下，把集成从「Python 适配器集合」升级为 **可快速接入、可信任写回、可复制、AI 可演进** 的集成 OS。

```text
GIP ≠ 通用 iPaaS（Boomi/MuleSoft）
GIP ≠ Process Mining（Celonis）
GIP = 受治理的制造执行集成平台（全球差异化品类）
```

### 1.2 与当前定版策略的关系

| 维度 | 当前定版（08/16/ADR-001） | GIP | 关系 |
|------|---------------------------|-----|------|
| L0 信任内核 | Graph/Rule/Execution/Audit/Revert | **不变** | 继承并放大 |
| 写路径唯一 | Agent→DSL→Rule→Execution→Connector | **不变** | 继承 |
| Pack/Package 飞轮 | export/import | **增强**（三速接入） | 补全工程路径 |
| Platform-L1 | connector_sdk + httpx | **升级为 GIP 四层** | **本战略主体** |
| MCP | Y3 对外开放 | **Y1 末内部 GA；Y2 对外** | 时间表修正 |
| Implementation Console | Y2～Y3 | **Integration Studio P1** | 提前 |
| connector-host | Y3 | **Edge Agent P1 PoC** | 提前 |

**结论**：GIP **不是换路**，是 **Platform-L1 从设计假设变为可交付产品**。

### 1.3 品类竞争定义（对外一句话）

> **Celonis 让 AI 读懂流程；Tulip 让工人连上系统；FactoryOS GIP 让 AI -assisted 集成 **敢写、可撤、可复制** 到任何 ERP/MES。**

**全方位领先的 realistic 定义**：

在 **「制造执行 Overlay + 受控写 + 可复制集成」** 品类综合第一——不追求 Connector 数量、Process Mining、通用 iPaaS 全覆盖。

---

## 二、竞品策略与位势（2025–2026）

| 竞品 | 核心赌注 | 集成强项 | 集成弱项（FactoryOS 机会） |
|------|----------|----------|---------------------------|
| **Celonis** | No AI without PI；Solution Suites；Agent Tools (MCP) GA | 1000+ Connector、Extractor Builder、OpenAPI AI 导入 | 制造 L2 写治理弱；Revert/对账非一等公民 |
| **Tulip** | Composable 现场 + AI Agent 调 Connector Function | 无代码 HTTP/SQL/MQTT、OPCH 私网 | Agent/App 直调写；缺 freeze/revert 闭环 |
| **Boomi / StackOne / Fivetran** | AI 从文档生成 Connector YAML | 小时～天级生成 Blueprint | 无 Graph freeze；无制造写治理 |
| **ERP 原生 AI** | 单系统 Copilot | 深度懂自家 ERP | 不解决 Execution Gap |

```text
                    接入速度 ──────────────────────────────►
                    慢                                    快
              ┌─────────────────────────────────────────────┐
  写治理  高  │  ★ FactoryOS 目标区（GIP 落地后）            │
              │     又快又可信                               │
              │  FactoryOS 当前（L0 强 / L1 弱）              │
              │                          Celonis / Boomi    │
              │                          Tulip（快但弱治理）  │
         低  │                                             │
              └─────────────────────────────────────────────┘
```

---

## 三、GIP 四层架构

```text
┌──────────────────────────────────────────────────────────────────────┐
│  L3  Integration Studio（实施/UI）                                     │
│      Connect · Map · Prove · Freeze · Export · Monitor               │
├──────────────────────────────────────────────────────────────────────┤
│  L2  Connector Intelligence（AI 层，可并行演进）                        │
│      Connector Agent · Mapping Copilot · Drift 诊断 · Test 生成        │
├──────────────────────────────────────────────────────────────────────┤
│  L1  Integration Runtime（Core 1.0 重点）                              │
│      Blueprint Engine · Runtime SDK · Edge Agent · Webhook Ingress     │
│      MCP Gateway（治理）· Pack Loader · Contract Test Runner           │
├──────────────────────────────────────────────────────────────────────┤
│  L0  Trust Kernel（冻结，不改）  ← 现有 graph/rule/execution/audit     │
└──────────────────────────────────────────────────────────────────────┘
```

| 层 | 职责 | 是否含 LLM |
|----|------|------------|
| **GIP-L1 Runtime** | Blueprint 解释、httpx 调用、韧性、Registry | 否 |
| **GIP-L2 Intelligence** | OpenAPI→Blueprint、mapping 建议、测试生成 | 是 |
| **GIP-L3 Studio** | 六步实施向导、健康/ drift 监控 | 否（Copilot 调 L2） |
| **Platform-L0** | 唯一写、Revert、对账 | 否 |

**红线**：GIP 任何组件 **不得** bypass `execution_service` 写 Legacy。

---

## 四、三速接入模型

| 模式 | 适用 | 目标周期 | 产出 |
|------|------|----------|------|
| **S1 认证 Pack** | 同型厂、同 ERP 厂商 | **≤1 周（机制）** / **2～3 周（日历 import）** | import Package + tenant Override |
| **S2 AI Blueprint** | 新 ERP 厂商、新 API | **2～5 天** | blueprint.yaml + 人工 Review + Contract Test |
| **S3 Custom Pack** | 私有协议、复杂签名 | **1～2 周** | Python Connector + blueprint.meta.yaml |

```text
S1/S2/S3 ──► Shadow（零写）──► Contract Test ──► 对账 ──► 批准开写 ──► Graph freeze ──► export Package
```

**AI 在环规则**（扩大优势、不失控）：

1. AI **不得** auto-freeze Graph  
2. AI **不得** bypass execution 写 Legacy  
3. AI 产出 **必须** 可 diff（YAML/JSON）  
4. 模型升级只换 GIP-L2 / Platform-L2；**L0 hash 不变**

---

## 五、核心交付物

### 5.1 Connector Blueprint Spec

- 规格：[Connector Blueprint 规格说明](../../文档/规格说明/Connector-Blueprint规格.md)  
- 原则：**80% 厂商接法 = 只写 Blueprint，不写 Python**

### 5.2 Canonical Manufacturing Verbs（CMV）

DSL 动词对外显式化；各 vendor Blueprint **只映射到 CMV**，不发明私有动词。

| 示例 CMV | 级别 | 说明 |
|----------|------|------|
| `QUERY_WORK_ORDER` | L0 | 读工单 |
| `WORK_REPORT` | L2 | 报工写 |
| `WORK_REPORT_REVERT` | L2 | 报工撤 |

### 5.3 MCP Gateway（治理型集成 ABI）

| 阶段 | 范围 |
|------|------|
| Y1 末 | 内部 GA：Skill/Agent 经 MCP 调 CMV；`tools/call` → DSL Plan，不直写 |
| Y2 | 对外：OAuth 2.1 + tenant scope + 工具级 ACL + audit |

**差异化**：Celonis MCP 偏 **PI 读**；FactoryOS MCP 偏 **受治理的制造写动词**。

### 5.4 Edge Agent（私网接入）

- 客户私网部署轻量 agent；**出站** mTLS/WSS 连 cloud  
- 凭证只在 edge 解密；cloud 存 `secrets_ref`  
- P1 PoC；灯塔 ERP 在私网则 **阻塞项**

### 5.5 Integration Studio 六步

| 步 | 名称 | 产出 |
|----|------|------|
| 1 | Connect | 连通报告 |
| 2 | Discover | 动词候选清单 |
| 3 | Map | mapping.yaml |
| 4 | Prove | Shadow + Contract Test + 开写批准 |
| 5 | Freeze | frozen Graph + RuleSet |
| 6 | Export | Implementation Package |

### 5.6 认证分级

| 级别 | 要求 | 对外承诺 |
|------|------|----------|
| **Bronze** | Blueprint + Contract Test + mock 通过 | 实验室可用 |
| **Silver** | + 1 家 Shadow 零 drift + Revert 实测 | 可复制 Pack |
| **Gold** | + ≥2 tenant + 对账 SLA | 「认证 Connector」 |

目录：`文档/连接器/catalog/{system}/{vendor}.yaml`

---

## 六、仓库与 CI 边界（2026-06-26 v6-full 勘误）

```text
FactoryOS/
├── src/
│   ├── server/
│   │   ├── os_core/                    # Core v1.0 冻结（tag core-v1.0.0）
│   │   │   ├── connector_sdk/
│   │   │   │   ├── runtime/             # Blueprint 引擎
│   │   │   │   └── protocol.py
│   │   │   └── mcp_gateway/             # Y1 末
│   │   ├── api/                         # deployable（import: server.api）
│   │   └── edge-agent/                  # 私网组件（P1 PoC）
│   ├── integration/                     # 集成团队主战场
│   │   ├── catalog/                     # Blueprint YAML（Runtime 加载）
│   │   ├── packs/
│   │   ├── tenants/{id}/overrides.yaml
│   │   └── tools/connector-agent/
│   └── apps/
│       ├── web-admin/                   # Studio `/studio/*`（P1）
│       └── h5-worker/
```

**CI 规则**：

- `os_core/*` 变更 → AC-BASE-001 全量  
- `integration/*` 变更 → Pack contract tests + API smoke  
- **禁止** `integration/` import `os_core/` 私有符号  

---

## 七、与全球顶级的优劣势（GIP 落地后）

### 7.1 优势（保持 + 放大）

| 优势 | 对竞品 | 放大方式 |
|------|--------|----------|
| 受控写 + Revert | Tulip/Agent 平台弱 | 每 op 绑定 revert + reconcile |
| Graph 冻结 | 无代码平台难审计 | Studio Freeze 步骤 |
| 部署即资产化 | Celonis Suite 偏 PI | S1 import ≤1 周 KPI |
| MCP 治理型写 | Celonis MCP 偏读 | CMV + Rule 门禁 |
| AI 演进不侵蚀 L0 | 多数 Agent 平台 | L1/L2 可换，L0 frozen |

### 7.2 劣势（诚实预期）

| 劣势 | 竞品 | GIP 策略 | Y1 预期 |
|------|------|----------|---------|
| Connector 数量 | Celonis 1000+ | 认证分级，不拼数量 | 10～20 Silver |
| 无代码 UX | Tulip 成熟 | Studio + Blueprint | Y1 末接近 |
| Process Mining | Celonis 核心 | 只做 Event→Draft assist | 不追 |
| 品牌案例 | 竞品有标杆 | 哈森闭环 | 商业层 |

### 7.3 必须第一的维度（非协商）

```text
接得进 → 试得够（Shadow）→ 写得稳 → 撤得了 → 复制得快 → AI 接得上且不失控
```

---

## 八、AI 并行演进路线

| 阶段 | 时间 | AI 能力 | L0 不变量 |
|------|------|---------|-----------|
| **A** | Core 1.0～P1 | OpenAPI→Blueprint 草稿；mapping 建议；contract test 生成 | 写路径、freeze |
| **B** | Y2 | Event→Graph Draft 建议（只读 assist）；drift 根因 + patch 建议 | 人 freeze |
| **C** | Y2 对外 MCP + Partner Pack；Y3 Evolution 只优化 Skill | Graph/Rule frozen |

---

## 九、落地路线图

### Phase 0 · Core 1.0 冻结（W1–W8）

| 周 | 交付 |
|----|------|
| W1–2 | Blueprint Spec v1 + Runtime 解释器 + mock |
| W3–4 | Runtime 韧性 + ExecutionRecord trace |
| W5–6 | Pack Loader + Package import/export |
| W7–8 | Shadow + 对账 P0 + AC 全绿 → `core-v1.0.0` |

### Phase 1 · GIP MVP（W9–W16，哈森并行）

| 周 | 交付 |
|----|------|
| W9–10 | Studio Connect + Discover |
| W11–12 | conn-erp-hasen blueprint + Contract Test |
| W13–14 | Edge Agent PoC + Studio Prove |
| W15–16 | Studio Freeze/Export + 首份 Silver 候选 Pack |

### Phase 2 · GIP 领先（W17–W24）

- Connector Agent CLI（7 步流水线）  
- MCP Gateway 内部 GA  
- Webhook Ingress  
- Mapping Copilot  
- 金蝶/用友 read Bronze Pack  

---

## 十、KPI（可量化领先）

| KPI | 竞品典型 | FactoryOS GIP 目标 |
|-----|----------|-------------------|
| 同型厂接入 | 4～12 周 | **S1：≤1 周** |
| 新 ERP 厂商 | 4～8 周 | **S2：≤2 周** |
| 生产写前验证 | 可选 UAT | **Shadow 标准步骤** |
| 写后一致性 | 人工对账 | **自动 reconcile + drift 告警** |
| 写错恢复 | 手工冲销 | **24h Revert** |
| 集成变更 | 改 App/脚本 | **只改 integration/** |
| Core 变更 | 频繁 | **Gate 0 后零变更（集成期）** |

---

## 十一、刻意不做

| 不做 | 原因 |
|------|------|
| 全量 Process Mining | Celonis 主场 |
| 无治理 iPaaS | 与 L0 冲突 |
| Agent 直写 ERP | 无差异化 |
| Day1 1000 Connector | 质量 > 数量 |
| Core 内 vendor 分支 | 全进 Blueprint/Pack |

---

## 十二、文档与 ADR 索引

| 文档 | 用途 |
|------|------|
| [ADR-004](../../文档/架构/架构决策记录-004-集成平台化GIP.md) | 架构决策（MCP 提前、Blueprint、Gate 0 扩展） |
| [16 §12](./16-OS核心基座架构设计方案.md#12-platform-l1-gip-架构) | 基座文档中的 L1 架构 |
| [Connector Blueprint 规格](../../文档/规格说明/Connector-Blueprint规格.md) | YAML 契约 |
| [AC-BASE-001 §GIP](../../文档/验收/验收用例-BASE-001-平台底座.md) | Gate 0 扩展验收 |

---

## 十三、版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| **v1.0.0** | 2026-06-16 | 初版；审计 Phase A/B 落地 |
