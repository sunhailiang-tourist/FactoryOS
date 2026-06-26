# FactoryOS 研发中枢索引

> **B 策略 v2**：认知精髓在 `.cursor/` · 机器契约在 `contracts/`

## 真源优先级

```text
0. 产品宪法（UI-FIRST · 配置平面主路径 = 管理台）
1. ADR 红线（REDLINES.md）
2. Contract Registry（DB）+ `contracts/` export 镜像
3. .cursor/factoryos/（SH-步步流 v2）
4. docs/（厚文档 · 可选外置）
5. docs-baseline/（docs 认知基线 · 漂移检测，非执行真源）
```

## 产品宪法 · 配置平面

| 文档 | 用途 |
|------|------|
| [UI-FIRST-CONFIG-PRINCIPLE.md](./UI-FIRST-CONFIG-PRINCIPLE.md) | **对外主路径 = 管理台 UI**；CLI/文档/仓库 = 内部或逃生舱 |
| [INTEGRATION-CHAIN.md](./INTEGRATION-CHAIN.md) | 接入/扩展 · Gate 上屏 · flows 与 Studio |

## SH-步步流 v2（平台研发轨）

| 文档 | 用途 |
|------|------|
| [PRE-DEV-CHAIN.md](./PRE-DEV-CHAIN.md) | **开发前全链路** · 维护地图 |
| [SH-步步流.md](./SH-步步流.md) | 工作流说明 |
| [GATES.md](./GATES.md) | L1 关键词闸门 |
| [STEP0.md](./STEP0.md) | Dev Step 0 三段 |
| [DEV-GATES.md](./DEV-GATES.md) | Gate 1–4 · 自检 · 停机 |
| [TEST-GATES.md](./TEST-GATES.md) | Gate A–G · 交付 · 回归 |
| [VERIFY-GATES.md](./VERIFY-GATES.md) | Verify 独立审阅回合 |
| [HARNESS-SCRIPTS.md](./HARNESS-SCRIPTS.md) | gate / harness 节点映射 |
| [ORM-MIGRATION-PRINCIPLE.md](./ORM-MIGRATION-PRINCIPLE.md) | **ORM 即设计 · Alembic 即部署**（开发快 · 迁移稳） |
| [docs-baseline](../docs-baseline/BASELINE.md) | **docs 认知基线**（漂移检测 → 工作流同步） |
| [ACTIVATION.md](./ACTIVATION.md) | **完全激活清单**（Hooks · uv · pre-commit） |
| [templates/](./templates/) | plan · test · test-step-regression · test-final-regression · step-stop · verify · bug · summary |
| [scripts/README.md](../../scripts/README.md) | 脚本目录（新人入口） |

## 架构与验收

| 需求 | 路径 |
|------|------|
| ADR-002 红线 | [REDLINES.md](./REDLINES.md) |
| 十内核模块 | [MODULE-MAP.md](./MODULE-MAP.md) |
| 52 P0 | [AC-P0-INDEX.md](./AC-P0-INDEX.md) |
| OpenAPI | [contracts/openapi/](../../contracts/openapi/) |
| 验收全文 | [contracts/acceptance/](../../contracts/acceptance/) |
| 落盘 | [_factoryos_pipeline/](../../_factoryos_pipeline/README.md) |

## 激活 Agent

| 模式 | 口令 | 细则 |
|------|------|------|
| 开发 | `【Dev模式启动】` + 本轮目标 | [DEV-GATES.md](./DEV-GATES.md) |
| 测试 | `【Test模式启动】` · `【Test·Step N 验收】` · `【Test·终轮回归】` | [TEST-GATES.md](./TEST-GATES.md) |
| 审阅 | `【Verify回合】Step N`（Test 之后 · 新对话） | [VERIFY-GATES.md](./VERIFY-GATES.md) |

## Cursor 规则

| 文件 | 加载 |
|------|------|
| `.cursor/rules/SH-步步流.mdc` | alwaysApply |
| `.cursor/rules/factoryos-dev-workflow.mdc` | `【Dev模式启动】` |
| `.cursor/rules/factoryos-test-workflow.mdc` | `【Test模式启动】` · `【Test·Step N 验收】` · `【Test·终轮回归】` |
| `.cursor/rules/编码绝对门禁.mdc` | alwaysApply |
| `.cursor/rules/项目结构变更门禁.mdc` | alwaysApply · 新建目录须用户确认 + README |

## 目录入口

| 路径 | 说明 |
|------|------|
| [../README.md](../README.md) | `.cursor/` 三区说明 |
| [../../src/README.md](../../src/README.md) | 代码根 |
| [../../rules/README.md](../../rules/README.md) | 参考存档（非真源） |

## 参考存档（非真源）

`rules/`（仓库根）· `rules/coder-expert-workflow.mdc` — ai-elephant 参考，已吸收纪律层。见 [rules/README.md](../../rules/README.md)
