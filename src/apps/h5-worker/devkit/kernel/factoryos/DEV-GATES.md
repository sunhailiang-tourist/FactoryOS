# Dev · Gate 1–4 与实现纪律

> plan 为**唯一执行清单**；未落盘禁止 `可以开始` 写码。

## 关键词（L1）

| 词 | 解锁 |
|----|------|
| `材料已齐` | **新功能**材料准入通过 → 允许 Step 0 |
| `可以继续` | Step0 通过；或 Step N 验收后下一 Step |
| `确认规划` | plan 合法落盘 + **`./scripts/gate plan` 绿（plan.ok · 绝对门禁）** |
| `可以开始` | **`./scripts/gate start --step N`（code.ok）** + 仅当前 Step 编码 |
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

## Gate 3 · Step 列表（每 Step 必填 · 与 plan-template §4/§6 一致）

plan 落盘必须让开发者**一眼**看清：共几步、每步做什么、落哪、是否合理、怎么用、入参/出参。  
对话中的 Gate 3 摘要可短，**落盘 plan 不得省略**下列列。

```text
§4 Step 总览表：Step | 名称 | 功能 | 问题 | 接口 | 新增函数 | 新增文件 | 改动文件 | Harness

每 Step（§6）必须含表：
  6.1 摘要（功能 / 解决问题 / AC / 验收 / 风险）
  6.2 接口（方法·路径·新增或改）
  6.3 函数（符号·路径·新增或改·职责·上下游）
  6.4 文件落位（路径·为何在此·是否合理·有无重复可复用）
  6.5 怎么用（HTTP / 代码入口）
  6.6 入参（JSON 骨架 + 字段表）
  6.7 返回（JSON 骨架 + 字段表）
  6.8 gate step 命令
```

**实现纪律**：`可以开始` Step N 后**仅**实现 plan §6 Step N；禁止提前做 N+1；停机对照 §6 自检。  
**UI对账**：命中则本 Step 对应 plan §8.2 行须闭环 / 未命中 N/A。

**机械校验（`./scripts/gate plan` → `check_plan_spec.py`）**：缺 Step 总览/详表关键字、新功能无 materials、UI 命中仍含待实现 → **gate plan 失败**。  
紧急旧 plan 可在文首加 `plan_format: legacy` 或 `--legacy`（仅跳过结构，仍查 AC/HTTP）。

---

## Gate 4 · 开始本 Step 前

1. plan 已落盘
2. 输出 `确认项（<=3）`：无则写「无（口径已闭环）」；命中 UI 门禁时须确认 plan §8.1/§8.2 已无「待实现/未知」
3. 问：「是否 `可以开始` Step N？」

---

## 每 Step 前置：git diff 复核

进入 Step N 前：`git diff` 核对 Step 1…N-1 与 plan 一致；未完成 → **停机**，禁止 Step N。

---

## 资深实现质量自检（11 项 · 停机逐项 Pass/Fail）

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
11. **UI字段对账**：未命中 → N/A；命中 → plan §8.2 本 Step 行全为已实现/不需要，且 step-stop §4b Pass

未全 Pass → 禁止停机等用户测试。

---

## Harness 分层（L0→L3 · 停机前仍四门全绿）

| 层级 | 何时 | 脚本 |
|------|------|------|
| L0 契约 | Step 0-B · `确认规划` · 动 `contracts/` | `./scripts/harness --tier contracts` |
| L1 边界 | 动 `src/server/os_core` · `src/integration` | `./scripts/harness --tier boundaries` |
| L2 冗余 | 动 `src/server/os_core` · `src/server/api` 业务 `.py` | `./scripts/harness --tier step` |
| L3 行为 | 每 Step 停机 | `./scripts/gate step --step N -k '<AC-ID>'`（含 verify + static） |

详表：[HARNESS-SCRIPTS.md](./HARNESS-SCRIPTS.md) · 脚本目录：[scripts/README.md](../../scripts/README.md)

---

## Step 停机输出（必用 `templates/step-stop-template.md`）

Step ID · 改动文件 · 11 项自检（含 UI 对账）· 等你进入 **Test 单步验收**

**停机全链**（次序强制）：

```text
step-stop 落盘
  → 【Test·Step N 验收】→ test-*-stepN-regression.md
  → 【Verify回合】Step N → verify-*-stepN.md
  → ./scripts/gate step --step N -k '<AC-ID>' 绿
  → 你：可以继续
```

Verify 细则：[VERIFY-GATES.md](./VERIFY-GATES.md) · Test 细则：[TEST-GATES.md](./TEST-GATES.md)

---

## 架构落位（新目录/模块前）

≤10 行：业务域 · 依赖方向证据 · 为何不漂移。新 `os_core/*` 或 `src/apps/*` 目录 → 先 README → 等你确认再继续。

---

## 注释与 pre-dev 骨架

plan 结构见 `templates/plan-template.md`（**§4 总览 + §6 每 Step 详表为硬要求**）。  
字段注释四要素：语义 / 用法 / 业务说明 / 上下游。
