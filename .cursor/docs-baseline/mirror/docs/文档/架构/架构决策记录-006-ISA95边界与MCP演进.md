# 架构决策记录 006：ISA-95 边界与 MCP 演进对齐

| 字段 | 值 |
|------|-----|
| 状态 | **Accepted** |
| 日期 | 2026-06-16 |
| 范围 | FactoryOS 在制造 IT 栈中的层级定位；MCP 2026-07 演进；Evolution Layer 命名 |
| 依赖 | ADR-001, ADR-004, ADR-005 |
| 关联 | [16-OS核心基座](../准备/2026-06-16/16-OS核心基座架构设计方案.md) · [MCP-Gateway规格](../规格说明/MCP-Gateway规格.md) |

---

## 1. 背景

FactoryOS 定位为 **ERP/MES Overlay 执行平台**，须在客户已有 ISA-95（IEC 62264）分层中明确 **不替代 L3 MES / L4 ERP**，同时与 **MCP 2026-07-28 RC**（无会话、Extensions、Feature 生命周期）对齐，避免 Y2 对外 MCP 时返工。

**08/07 中的「Layer 4 Evolution」** 为战略路线图用语，**不属于** ADR-001 定义的 **Platform-L0～L3** 运行时层。

---

## 2. ISA-95 定位

### 2.1 FactoryOS 在栈中的位置

```text
Level 4  ERP / 计划 / 主数据 / 财务权威     ← 客户系统（Path A 写落点）
Level 3  MES / 现场执行 / 追溯               ← 客户系统（Path B 写落点）
Level 3.5 FactoryOS Platform-L0～L3         ← Overlay：编排、治理写、审计、撤回
Level 2  设备 / SCADA（不经由 FactoryOS 直控）
```

| 决策 ID | 决策 |
|---------|------|
| I6-01 | FactoryOS **不**承担 MES 排程、设备 PLC 控制、全量 eBR 替代 |
| I6-02 | **Data-L0** = 客户 Legacy 权威账本；FactoryOS **不**成为默认主数据真源 |
| I6-03 | 跨层写须经 **CMV + Graph freeze + Rule + Execution**；禁止绕过 MES/ERP 治理直接改历史 |
| I6-04 | Blueprint 字段映射 **SHOULD** 对齐 ISA-95 对象语义（WorkOrder、OperationConfirmation、MaterialLot） |
| I6-05 | Path A：ERP 为报工 **写权威**；Path B：MES 写 + ERP 读；Path C：builtin 表模拟 L3 子集 |

### 2.2 与 B2MML 的关系

- **不**要求全量 B2MML/XML 交换  
- Implementation Package export **MAY** 含 `isa95_object_map` 元数据（Y2）  
- Contract Test 样例 **SHOULD** 使用稳定业务键：`work_order_id`、`completed_qty`、`legacy_ref`

---

## 3. Evolution Layer vs Platform-L*

| 用语 | 含义 | 文档位置 |
|------|------|----------|
| **Platform-L0～L3** | 运行时平台层（内核 / GIP / Skill / Harness） | ADR-001, 16 |
| **Data-L0～L3** | 数据分层 | 06, ADR-000 |
| **Pack-L1～L3** | 商业模块包层 | 05, ADR-003 |
| **Evolution Layer（战略 Layer 4）** | 流程挖掘、自动 Graph 建议、跨厂分析 | 07, 08 **路线图** |

**决策 I6-06**：Evolution **不得**写入 Platform-L 编号；实现前须 **新 ADR** + 明确不破坏 frozen Graph。

---

## 4. MCP 2026-07 对齐

| MCP 变更（RC） | FactoryOS 策略 |
|----------------|----------------|
| **无会话 / 无 `initialize`**（SEP-2567） | `mcp_gateway` **不**依赖 `Mcp-Session-Id`；tenant 在 URL `/mcp/v1/{tenant_id}` |
| **Extensions**（SEP-2133） | Enterprise Auth、Tasks 以 `ext-*` 注册；Y2 对外前评估 |
| **Feature 生命周期 ≥12 月** | 对外 MCP 版本钉扎在 OpenAPI `info.version` + ADR 修订 |
| **`_meta` OTel**（SEP-414） | 已实现于 MCP-Gateway §4.1；M-03 P1 钩子 |
| **Enterprise-Managed Authorization** | Y2：OAuth 2.1 + PKCE + IdP；Y1 内部 API Key |

**决策 I6-07**：Y1 MCP stub **MUST** 保留 `params._meta` 解析钩子；Y2 升级时 **不得**破坏 `tools/call → DslPlan` 契约。

---

## 5. Integration Studio 宿主（闭合 C-01）

| Phase | 决策 |
|-------|------|
| **P1 MVP** | Studio 路由宿主 **`src/apps/web-admin`**，路径前缀 `/studio/*`；与 Graph 管理同 deployable |
| **Y2 可选** | 若前端 bundle 过大，可拆 **`apps/integration-studio/`** 独立构建，**API 不变** |

**决策 I6-08**：OpenAPI v1.1.1 路由为真源；`apps/integration-studio/` 目录名保留为 **Y2 拆分目标**，P1 可不建独立 app 工程。

---

## 6. S1 接入 KPI 定义（闭合 C-03）

| 指标 | 定义 | 目标 |
|------|------|------|
| **S1 机制** | 已有 **Silver Pack** 的 `import Package` + tenant Override | **≤1 周**（工程机制） |
| **S1 日历** | 实施人天 + Shadow/UAT + 客户签字 | **2～3 周**（Silver import，见 04/14） |
| **全量 D1** | 无 Silver、绿field 实施 | **4～8 周** |

**废止**：17 §四「4～8 **小时**」表述——易与日历周混淆，以本 ADR 为准。

---

## 7. Gate 0 P0 计数

**AC-BASE-001 v0.2 P0 = 52 条**（§十四枚举：原 48 + ADR-007 **S-01～S-04**）。全文 **废止「55 条 P0」** 陈旧表述。

Phase 1 完成附加：**H-01～H-03**（P1）+ **M-03**（P1 钩子）。

---

## 8. 后果

### 正面

- 制造客户 IT 可理解 FactoryOS 与 ERP/MES 边界  
- MCP 对外路线与 2026 标准一致，降低 Y2 返工  
- Studio 宿主、S1 KPI、P0 计数单一真源  

### 负面

- 须批量勘误 prep/README 中「55 P0」「4～8 小时」  
- ISA-95 对象映射增加 Blueprint 评审项  

---

## 9. 参考

- [ISA-95 / IEC 62264](https://www.siemens.com/en-us/technology/isa-95-framework-layers/)  
- [MCP 2026-07-28 RC](https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/)  
- [SEP-414](https://modelcontextprotocol.io/seps/414-request-meta)  
- [ADR-004](./架构决策记录-004-集成平台化GIP.md) · [ADR-005](./架构决策记录-005-双写入路径与灯塔定版.md) · [F1 膨胀期守则](./膨胀期架构守则.md) · [Evolution 宪章](./Evolution-Layer-宪章.md)
