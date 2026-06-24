# Step 0 · 全量理解闭环（Dev）

> v2 · 通过后才允许 Gate 1 或合并规划。结束时等你 `可以继续`。

## 呈现方式

先 **≤8 行执行摘要**（落点模块 · 风险 1–3 · 文档是否对齐 · 是否缺材料），再附附录证据。

---

## Step 0-0（可选）需求诊断

输入明显不足以落地时触发。输出 ≤5 条：目标一句话 · 缺口 A/B/C · 默认推断+证据 · 材料待补（1 个总问项）· 等你 `可以继续`/`补齐`/`反对+更正`。

---

## Step 0-A · 架构与模块（不依赖本轮需求材料）

必须给出结论+证据路径：

1. **写路径**：`perception/agent → DslPlan → harness/confirm → rule → execution → connector → audit`（R-01–R-11）
2. **本轮落点**：`MODULE-MAP.md` 中哪些模块；`apps/api` 是否仅路由
3. **integration 边界**：禁 import os_core 私有 API；仅 OpenAPI + connector_sdk 公开面
4. **关键入口**：本轮将改的 `src/os_core/*`、`src/apps/api/*`、`src/integration/*` 路径清单
5. **状态机/Graph**：是否涉及 freeze、Rule deny、Shadow/simulated

---

## Step 0-DB · 数据库只读（有 PG/Alembic 后强制执行）

`可以开始` 前仅只读（schema introspection / SELECT）：

1. 连接证据：配置路径、库名、迁移 head
2. ORM vs 真实库：表/字段/约束 — `已一致/缺失/不一致/不可核对`
3. 关键状态字段分布（轻量统计）
4. 缺口分级：**A 类**（缺表/缺字段阻断）→ 停 Step 0 等你拍板

无库时：写明「Schema 以 `contracts/schemas` + 计划迁移为准」，不跳过 0-A/0-B。

---

## Step 0-B · 契约与 AC 对齐

对照 **`contracts/openapi`** · **`contracts/acceptance`** · 本轮 AC ID（`AC-P0-INDEX.md`）：

| 核对项 | 真源 |
|--------|------|
| 路径/方法/参数/响应 | OpenAPI + JSON Schema |
| 验收断言 | AC 文档 WHEN/THEN |
| 红线负向 | REDLINES.md + AC E-08 等 |
| 代码侧定义（已有代码时） | Pydantic / 路由返回模型交叉核对 |

**快速路径**（单点 Bug/联调）：仅核对本次 HTTP 入口 + 至少 1 组关键字段。

### 缺口分级

| 级 | 含义 | 处置 |
|----|------|------|
| **A** | 外部契约不可推断 | 等你补齐或拍板 |
| **B** | 可推断但影响安全/一致性 | 默认假设+证据，标注待确认 |
| **C** | 内部细节 | 可写入 plan 标注推断点 |

### docs 基线漂移（可选）

大改 `docs/` 后运行 `./scripts/docs_baseline workflow-check`。若报 **Tier-A** 未同步 `.cursor/factoryos/` → 标 **B 类缺口**，等你拍板。详见 [docs-baseline/BASELINE.md](../docs-baseline/BASELINE.md)。

### UI 字段对账（仅 `apps/h5-worker` / UX 迭代）

有原型/截图时：界面字段表 + 接口字段对账表（参考 `rules/coder-expert-workflow` 图片门禁）。**kernel / os_core 迭代不强制**。

---

## Step 0 结束

输出「全量理解确认单」，等你：

- `可以继续` → 进入规划（Gate 1–4 或合并模式）
- `不可以/有问题` → 补齐后重做 Step 0
