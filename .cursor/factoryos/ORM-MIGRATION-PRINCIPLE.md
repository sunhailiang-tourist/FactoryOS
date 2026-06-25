# ORM 即设计 · Alembic 即部署

> **状态**：Accepted（2026-06-24）  
> **目标**：开发快 · 迁移稳 · 后期迭代稳字当头  
> **技术栈**：PostgreSQL 16 · SQLAlchemy 2.0 async · asyncpg · **Alembic**（ADR-001 · ADR-007）

---

## 一、一句话

**数据库设计只在代码里做（SQLAlchemy Models）；部署只连库并跑迁移（`alembic upgrade head`）。**  
禁止把「运行时 ORM 自动建表」当作生产 schema 管理手段。

---

## 二、双真源分工（不撕裂）

| 层 | 真源 | 用途 |
|----|------|------|
| **运行库结构** | `src/os_core/**/models` + `alembic/versions/` | 表 · 字段 · 关系 · 索引 · 约束 |
| **对外契约** | `contracts/schemas` · OpenAPI | API/跨语言/验收断言 |
| **厚文档** | `docs/` · ADR | 背景与裁定；**不**手写 DDL 真源 |

改表：**先改 Model → 生成/编写 Alembic revision → 审阅 → 提交 Git**。  
改 API 形状：**同步检查** `contracts/schemas` 与 ORM 是否一致（harness L0）。

---

## 三、开发快：日常怎么做

### 3.1 新建/改表（AI Coding 主路径）

```text
1. 在 os_core 对应模块写/改 SQLAlchemy Model（含 relationship · Index · CheckConstraint）
2. alembic revision --autogenerate -m "s0x_简述"
3. 人工审阅生成的 versions/*.py（见 §五）
4. 本地：alembic upgrade head
5. pytest / gate step 绿后提交（Model + migration 同 commit）
```

### 3.2 仅本地空库快速试验（可选 · 非门禁）

- 允许 `metadata.create_all()` **仅**于本地 disposable DB、单人原型
- **禁止**写入 CI、pre-commit、`gate pr`、生产部署脚本
- 一旦进入 W1 共享分支：**一律走 Alembic**

### 3.3 与 Step 0-DB 的关系

见 [STEP0.md](./STEP0.md) §Step 0-DB：有 PG 后，`可以开始` 前只读核对 **ORM ↔ 真实库 ↔ migration head** 三者一致。

---

## 四、迁移稳：部署怎么做

### 4.1 各环境统一命令

```bash
# 空库或已有库 — 唯一标准入口
alembic upgrade head
```

| 环境 | 数据库 | 纪律 |
|------|--------|------|
| 本地 dev | 可 disposable | `upgrade head`；可 drop 重建 |
| CI | 临时 PG 容器 | 迁移链从头跑 + contract tests |
| staging / prod | 持久库 | **仅** `upgrade head`；禁止 `create_all` |

连接串：`DATABASE_URL`（async 运行时）与 Alembic `env.py` 同步配置，**禁止**硬编码。

### 4.2 Gate 0 首批迁移（W1 · 已裁定）

ADR-007 §15 · AC-BASE-001 **S-01～S-04**：

| ID | 内容 |
|----|------|
| S-01 | `tenants` 增 `cell_id` · `placement_tier` · `region` |
| S-02 | 空表 `connector_instances` |
| S-03 | 空表 `tenant_quotas` · `outbox_events` |
| S-04 | Repository 层 tenant filter（代码门禁，非 DDL） |

W1 交付物：`alembic/` 脚手架 + 上述 revisions + `alembic upgrade head` 可绿。

### 4.3 上线后演进（稳字当头）

生产改 schema 默认 **expand-contract**，避免破坏性一步到位：

```text
expand  → 双写/回填（可选 data migration revision）→ contract  → 删旧列/旧表
```

- **expand**：加列/加表（nullable 或带 default）
- **contract**：应用不再读旧结构后，再删列/改类型
- 大表索引：PostgreSQL 用 `CREATE INDEX CONCURRENTLY`（Alembic 需 `autocommit` 块）

---

## 五、审阅纪律（autogenerate 不是全自动）

Alembic `--autogenerate` **只作草稿**，提交前必须人工检查：

| 风险 | 处理 |
|------|------|
| 列重命名 | 常被识别为 drop+add → **手写** `op.alter_column` / rename |
| 类型收窄 | 可能丢数据 → 分步 migration + 回填 |
| 删列/删表 | PR 必须写明理由；prod 走 contract 阶段 |
| 索引/约束名 | 显式命名，避免 PG 自动名漂移 |
| 数据迁移 | 单独 revision 或同 revision 内分步，与 DDL 可拆分 |

---

## 六、机械门禁（W1 起逐步接入）

| 节点 | 检查（计划） |
|------|----------------|
| PR / `gate pr` | `alembic check`（Model 与 head 无未生成漂移） |
| `gate step`（改 models/alembic 时） | `alembic upgrade head` 对临时库可绿 |
| CI | PG service + `alembic upgrade head` + contract pytest |
| pre-commit（可选） | 改 `models` 未改 `versions/` 时提示 |

> W1 脚手架落地后，在 `scripts/check_harness.py` 注册并更新 [HARNESS-SCRIPTS.md](./HARNESS-SCRIPTS.md)。

---

## 七、多租户备注（FactoryOS 特有）

- **当前（S0）**：shared schema + `tenant_id` 全表；迁移一条链即可。
- **S1+**：若 schema-per-tenant / cell 拆分，迁移需 **fleet 编排**（按租户分批、canary），见 ADR-007 · 多租户文档 — 仍基于 **版本化 migration**，不是 `create_all`。

---

## 八、禁止项

- 生产 / CI / `gate pr` 使用 `Base.metadata.create_all()`
- 手工改 prod/staging DDL 而不回写 Alembic revision
- Model 与 `alembic/versions` 不同 commit 且无说明
- 仅用 `contracts/schemas` 描述表结构却不落 ORM（运行库无真源）

---

## 九、相关文档

| 文档 | 路径 |
|------|------|
| ADR-001 技术栈 | `docs/文档/架构/架构决策记录-001-系统架构总览.md` |
| ADR-007 规模预埋 | `docs/文档/架构/架构决策记录-007-百级千级演进策略.md` §15 |
| AC S-01～S-04 | `contracts/acceptance/验收用例-BASE-001-平台底座.md` |
| Step 0-DB | [STEP0.md](./STEP0.md) |
| 编码绝对门禁 | `.cursor/rules/编码绝对门禁.mdc` |
