# Evolution Layer 宪章

> 版本：**v1.0.0** | 日期：2026-06-16  
> 状态：**Accepted**  
> 关联：ADR-006 I6-06 · [07-行业痛点 §五](../../准备/2026-06-16/07-行业痛点与顶级平台差距分析.md) · [治理规范](./治理规范.md)

---

## 1. 定义

**Evolution Layer（战略 Layer 4）** 指：利用 AI / 事件 / 挖掘 **辅助** 集成与 Skill 演进的能力层。

**不是** ADR-001 的 **Platform-L0～L3** 运行时层编号；**不得**在代码目录中使用 `platform_l4/` 或与 L0 混编。

```text
Platform-L0～L3   → 生产运行时（Graph/Rule/Execution/GIP/Skill/Harness）
Evolution Layer   → 路线图能力（Y2+ 只读 assist 为主）
```

---

## 2. 允许（Evolution 可做的事）

| ID | 能力 | 输出 | 人审 |
|----|------|------|------|
| EVO-01 | Connector-Agent 生成 **Bronze** Blueprint 草稿 | YAML 文件 | ✅ 必须 |
| EVO-02 | Studio mapping **建议**（confidence 分数） | mapping.yaml 草案 | ✅ 必须 |
| EVO-03 | Contract Test **用例生成** | test fixtures | ✅ 必须 |
| EVO-04 | Event 日志 → Graph **Draft** 建议 | draft Graph JSON | ✅ freeze 前 |
| EVO-05 | Skill **提示词 / 步骤文案** 优化 | Prompt 版本 | ✅ A/B 可选 |
| EVO-06 | drift 根因 **分析报告** | 只读报告 | 可选 |

---

## 3. 禁止（Evolution 不得做的事）

| ID | 禁止行为 | 原因 |
|----|----------|------|
| EVO-X01 | **自动 freeze** Graph / RuleSet | ADR-002 R-09 |
| EVO-X02 | **自动修改** frozen Graph checksum 内节点 | 审计链破坏 |
| EVO-X03 | **绕过** Rule Engine / Execution 直写 Legacy | ADR-002 R-01 |
| EVO-X04 | **自动 promote** Bronze → Silver Pack | GIP 成熟度门禁 |
| EVO-X05 | **自动执行** L2 写（无 Harness confirm） | R-11 |
| EVO-X06 | 在生产租户 **静默改** Override `effect`/Rule deny | ADR-003 |
| EVO-X07 | 全量 **Process Mining** 替代客户 MES/ERP 权威 | 非 Overlay 定位 |

违反 EVO-X* 的代码 **不得合并**；须新 ADR + 治理 G4 评审。

---

## 4. 与 MCP / Agent 的边界

| 路径 | Evolution 角色 |
|------|----------------|
| MCP `tools/call` | **不得** 返回可直接写 Legacy 的 payload；仍只产出 **DslPlan** |
| LangGraph Skill | 可换模型/提示；**不得**改 `allowed_dsl` 集合（Graph 属性） |
| Connector-Agent | 输出进 `integration/` Git PR；**不得** import `execution_service` |

---

## 5. 上线门禁（Evolution 功能）

新 Evolution 能力上线须：

1. 本文档 EVO-* ID 登记  
2. 只读或 draft 输出契约（Schema/OpenAPI）  
3. AC 负向用例：证明 EVO-X01～X05 不可触发  
4. 治理 G3（Evolution 专用）签字  

---

## 6. 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0.0 | 2026-06-16 | F1 初版；闭合 ADR-006 I6-06 |
