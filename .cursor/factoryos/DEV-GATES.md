# Dev · Gate 1–4 与实现纪律

> plan 为**唯一执行清单**；未落盘禁止 `可以开始` 写码。

## 关键词（L1）

| 词 | 解锁 |
|----|------|
| `可以继续` | Step0 通过；或 Step N 验收后下一 Step |
| `确认规划` | plan 合法落盘后 |
| `可以开始` | **仅当前 Step** 编码 |
| `测试不通过` | 回当前 Step 修复 |

---

## 文档完整合并模式（推荐：无 A 类缺口时）

一次输出 **一次性规划确认**，含：

1. 需求审核结论（Gate 1）
2. 增量流程图 Mermaid（Gate 2，可删节若纯内核 API）
3. Step 列表（Gate 3 模板）

等你 `确认规划` → 落盘 plan → Gate 4 问 `可以开始`。

## 快速路径（Bug/联调 · 全条件满足）

1. 类型：Bug修复 / 联调排障
2. 可定位：方法+路径 或 现象+日志
3. 范围小：不涉及跨域状态机大改

策略：Step 0-A 完整 · 0-B 简化 · 可跳过 Gate2 流程图 · Gate1+3 合并单 Step plan · 仍须落盘 · 仍须 Gate4 `可以开始`。

---

## Gate 3 · Step 列表（每 Step 必填）

```text
Step N — <名>（流程节点：xxx）
  AC ID：G-01, E-03, …
  接口：METHOD /v1/...（新增/修改）
  模块路径：os_core/... 或 apps/api/...
  Harness 验收盘：`./scripts/gate step --step N -k '<AC-ID>'`（停机；编码中按改动面见 HARNESS-SCRIPTS.md）
  风险：幂等/越权/shadow/…
  验收标准：（可测一句话）
```

---

## Gate 4 · 开始本 Step 前

1. plan 已落盘
2. 输出 `确认项（<=3）`：无则写「无（口径已闭环）」
3. 问：「是否 `可以开始` Step N？」

---

## 每 Step 前置：git diff 复核

进入 Step N 前：`git diff` 核对 Step 1…N-1 与 plan 一致；未完成 → **停机**，禁止 Step N。

---

## 资深实现质量自检（10 项 · 停机逐项 Pass/Fail）

1. **分层**：api 薄；业务 os_core；写 Legacy 仅 execution_service
2. **响应契约**：对齐 OpenAPI / Pydantic；错误码一致
3. **鉴权/租户**：N-03；无跨 tenant 泄漏
4. **红线**：R-01–R-11 本 Step 不涉及项也须确认未破
5. **DTO/Schema**：与 `contracts/schemas` 一致
6. **输入校验**：Pydantic；枚举/范围与 AC 一致
7. **Shadow**：dry_run/shadow_mode → simulated，Legacy 不变（T-01）
8. **幂等/补偿**：idempotency_key；L2 有 Compensator（R-05）
9. **静态检查**：lint/type 无新增错误
10. **注释**：字段四要素 + 函数上下游（编码绝对门禁）

未全 Pass → 禁止停机等用户测试。

---

## Harness 分层（L0→L3 · 停机前仍四门全绿）

| 层级 | 何时 | 脚本 |
|------|------|------|
| L0 契约 | Step 0-B · `确认规划` · 动 `contracts/` | `./scripts/harness --tier contracts` |
| L1 边界 | 动 `src/os_core` · `src/integration` | `./scripts/harness --tier boundaries` |
| L2 冗余 | 动 `src/os_core` · `src/apps` 业务 `.py` | `./scripts/harness --tier step` |
| L3 行为 | 每 Step 停机 | `./scripts/gate step --step N -k '<AC-ID>'`（含 verify + static） |

详表：[HARNESS-SCRIPTS.md](./HARNESS-SCRIPTS.md) · 脚本目录：[scripts/README.md](../../scripts/README.md)

---

## Step 停机输出（必用 `templates/step-stop-template.md`）

Step ID · 改动文件 · 10 项自检 · `./scripts/gate step --step N` 摘要 · **Verify 落盘** · 等你 `可以继续`

Verify 细则：[VERIFY-GATES.md](./VERIFY-GATES.md)

---

## 架构落位（新目录/模块前）

≤10 行：业务域 · 依赖方向证据 · 为何不漂移。新 `os_core/*` 或 `apps/*` 目录 → 先 README → 等你确认再继续。

---

## 注释与 pre-dev 骨架

plan 结构见 `templates/plan-template.md`。字段注释四要素：语义 / 用法 / 业务说明 / 上下游。
