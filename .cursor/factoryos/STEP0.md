# Step 0 · 全量理解闭环（Dev）

> v2 · 通过后才允许 Gate 1 或合并规划。结束时等你 `可以继续`。  
> **新功能**：须先过 **材料准入绝对门禁**，才允许进入本页 0-A / 0-DB / 0-B。

## 呈现方式

先 **≤8 行执行摘要**（落点模块 · 风险 1–3 · 文档是否对齐 · 是否缺材料），再附附录证据。

---

## 材料准入 · 绝对门禁（仅类型 = 新功能 · 先于 Step 0）

> 目标：开发计划 / 需求分析之前，先收齐「要做什么」的文案与资料，并追问补充，避免空转推断。  
> 模板：[templates/materials-intake-template.md](./templates/materials-intake-template.md)

### 触发

`【Dev模式启动】` 后用户选定（或可判定）类型为 **新功能**。  
非新功能（Bug / 联调 / 纯重构且无新能力）→ 本门禁 **N/A**，可按原规则进入 Step 0-0 / 0-A。

### 强制顺序（不可跳）

```text
定类型 = 新功能
  → ① 功能需求文案（必给）
  → ② 需求资料（必给 · ≥1）
  → ③ Agent 追问「是否还有补充需求资料？」→ 用户答有/无补充
  → ④ 用户：材料已齐
  → ⑤ `./scripts/gate materials`（写 materials.ok）
  → 才允许 Step 0-A / 0-DB / 0-B / 写 plan-*.md
```

| # | 要求 | 硬失败 |
|---|------|--------|
| ① | 功能需求文案说清楚：一句话目标 + 2～4 条可测验收；给路径或可引用摘要 | 无文案 |
| ② | 需求资料表至少 1 行有效（PRD/AC/原型/Figma/说明等） | 无资料 |
| ③ | **必须追问补充**；用户明确「有补充+列表」或「无补充」 | 未追问或用户未答 |
| ④ | 用户确认 `材料已齐`（或等价） | 未确认 |
| ⑤ | **`./scripts/gate materials`** 绿（新功能 `--materials`；Bug `--na --reason`） | 无 materials.ok |

落盘：`_factoryos_pipeline/<YYYY-MM-DD>/plan/materials-<HHmm>-<slug>.md`。  
**禁止**：无 materials.ok 时写 `plan-*.md`、升 phase≥PLANNING、跑 `gate plan`、输出「全量理解确认单」冒充可规划。

### 与后续门禁关系

- 材料准入通过 → 进入下方 Step 0-0（若仍不足）/ 0-A / 0-DB / 0-B  
- 若本轮还将 **新增/改 server 接口字段** 且资料含原型图 → 另受 **UI/原型字段对账** 约束（见 0-B）  
- 范围仍不清 → 优先 `【PM模式启动】`，但 **不能**用 PM 建议代替本门禁的①②③④

---

## Step 0-0（可选）需求诊断

输入明显不足以落地时触发。输出 ≤5 条：目标一句话 · 缺口 A/B/C · 默认推断+证据 · 材料待补（1 个总问项）· 等你 `可以继续`/`补齐`/`反对+更正`。

> **新功能**：若尚未过材料准入，**先跑材料准入**，不要用 0-0 代替①②③④。  
> **优先**：功能/原型/范围不清时，先开独立会话 `【PM模式启动】` → 落盘 `pm/`（见 [PM-GATES.md](./PM-GATES.md)），再回 Dev；回到 Dev 仍须材料准入勾选（可引用 `pm/` 路径）。

---

## Step 0-A · 架构与模块（不依赖本轮需求材料）

必须给出结论+证据路径：

1. **写路径**：`perception/agent → DslPlan → harness/confirm → rule → execution → connector → audit`（R-01–R-11）
2. **本轮落点**：`MODULE-MAP.md` 中哪些模块；`src/server/api` 是否仅路由
3. **integration 边界**：禁 import os_core 私有 API；仅 OpenAPI + connector_sdk 公开面
4. **关键入口**：本轮将改的 `src/server/os_core/*`、`src/server/api/*`、`platform_registry/*` 路径清单
5. **状态机/Graph**：是否涉及 freeze、Rule deny、Shadow/simulated

---

## Step 0-DB · 数据库只读（有 PG/Alembic 后强制执行）

`可以开始` 前仅只读（schema introspection / SELECT）：

1. 连接证据：配置路径、库名、迁移 head
2. ORM vs 真实库：表/字段/约束 — `已一致/缺失/不一致/不可核对`
3. 关键状态字段分布（轻量统计）
4. 缺口分级：**A 类**（缺表/缺字段阻断）→ 停 Step 0 等你拍板

无库时：写明「Schema 以 SQLAlchemy Models + Alembic 迁移为准（见 [ORM-MIGRATION-PRINCIPLE](./ORM-MIGRATION-PRINCIPLE.md)）；对外形状以 `contracts/schemas` 为准」，不跳过 0-A/0-B。

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

### UI / 原型字段对账（服务端开/改接口时 · 命中即强制）

> 目标：在 **server 业务接口**新增或改响应/入参字段时，按需求图做像素级字段对账，保证 OpenAPI/实现不漏字段。  
> **非** core/kernel 日常门禁；**非**纯前端联调主门禁。  
> 渊源：ai-elephant `coder-expert-workflow` 图片门禁 · FactoryOS 化（绑定 `contracts/` + `src/server/api`）。

**适用范围（须同时满足）**：

1. 本轮改 `src/server/api/**` 或 `contracts/openapi` / `contracts/schemas` 的接口字段形状（或 os_core 仅为支撑该接口的读模型）  
2. 有可对账资料：原型截图 / 字段标注 / UI 线框 / 流程图字段标注 / Figma（含 PDF 内图）  
3. 图上字段需落入本轮 request/response（否则标 `不需要` + 业务理由）

未命中 → Step 0 写 `UI对账：N/A` + 理由，跳过下列产出。

命中时 Step 0-B **必须**产出（缺一 → Step 0 未通过，禁止进 Gate 1–4）：

1. **《图片材料清单 + 覆盖确认》**  
   枚举本轮全部图片类输入（含 PDF 页码 / Figma `fileKey:nodeId`）。  
   每项：`文件或节点 / 页码或区域 / 用途（页面或流程节点） / 归属接口（如适用）`。

2. **《界面字段表》（一图一表）**  
   写入后续 `plan-*.md` §8（或独立路径并在 plan 引用）。列（缺一不可）：

   | 视图ID | 图/页码/位置 | UI元素/文案 | 字段标识（key） | 数据来源（表/模型/契约） | 归属接口 |
   |--------|--------------|-------------|-----------------|--------------------------|----------|

3. **缺口**：对账中无法映射到 OpenAPI/`contracts/schemas` 的字段 → **A 类**（停 Step 0）或 **B 类**（默认假设 + 待确认）。

**禁止**：只说「看过图」但无上述落盘；把字段当「先不做」却未标 `不需要` + 业务理由。

---

## Step 0 结束

输出「全量理解确认单」，等你：

- `可以继续` → 进入规划（Gate 1–4 或合并模式）
- `不可以/有问题` → 补齐后重做 Step 0
