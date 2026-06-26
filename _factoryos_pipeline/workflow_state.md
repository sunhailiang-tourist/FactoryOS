# SH-步步流 · 工作流状态机

```yaml
phase: CAN_CODE
agent: dev
step: 1
plan: _factoryos_pipeline/plan/plan-api-v6-full-structure.md
updated: 2026-06-26
goal: v6-full 全库统一 · 文档/SVG/rules/pipeline 对齐 · W1~W4 链路绿
```

## 全量审计结论（2026-06-26 · v6-full）

> **绝对门禁**：须「确认规划」+ `./scripts/gate plan`  
> **联动**：Dev→Test→Verify 节拍不变

### 一、工作流 / rules / 脚本同步

| 检查项 | 状态 | 说明 |
|--------|------|------|
| `.cursor/rules/编码绝对门禁.mdc` | ✅ | `src/server/api` · `src/server/os_core` |
| `.cursor/rules/factoryos-dev/test-workflow.mdc` | ✅ | 无旧路径 |
| `.cursor/rules/工厂操作系统.md` | ✅ 已修 | `server/api` → `server/api` |
| `.cursor/rules/项目结构变更门禁.mdc` | ✅ | 参照 contracts/README |
| `.cursor/factoryos/MODULE-MAP.md` | ✅ 已修 | v6 注册表 + api 四层 |
| `.cursor/factoryos/HARNESS-SCRIPTS.md` | ✅ 已修 | registry + legacy 进 L1 |
| `.cursor/factoryos/templates/*` | ✅ 已修 | server/api 分层表述 |
| `scripts/check_harness.py` | ✅ | 8 checks full tier |
| `scripts/README.md` | ✅ 已修 | 5 registry 脚本入表 |
| `scripts/check_legacy_paths.py` | ✅ | 6 条废止路径 |
| `protect-paths.py` | ✅ | `src/server/os_core` · `src/server/api` |
| `pyproject.toml` pythonpath | ✅ | `src` · `src/server` |
| `CODEOWNERS` | ✅ | `src/server/api` · `src/server/os_core` |
| `docs/文档/架构/命名约定.md` | ✅ 已修 | 废止路径清单 |
| `src/**` 代码注释/README | ✅ 已修 | `server/api` → `server/api` |
| `.cursor/docs-baseline/mirror/` | ✅ 已同步 | 2026-06-26 v6-full 批量对齐 |
| `_factoryos_pipeline/*` 历史 step | ✅ 已勘误 | 路径表述统一为 `src/server/*` |
| `docs/文档/架构/*.svg` · ADR 正文 | ✅ 已统一 | `server/api` 语义 + `src/server/*` 物理路径 |

### 二、W1~W4 功能链路（72/72 全跑 · 非抽检）

| 阶段 | AC/测试 | 数量 | 结果 | API 模块路径 |
|------|---------|------|------|--------------|
| **W1 基座** | S-01~S-04 | 4 | ✅ | config/dependencies · probes |
| **W1 基座** | C-01 | 1 | ✅ | modules/connectors |
| **W1 基座** | /health workflow | 1 | ✅ | modules/probes |
| **W2 审计执行** | E-01~E-09 · E-03 audit | 10 | ✅ | modules/execution · audit |
| **W3 图规则 DSL** | G-01~G-08 | 8 | ✅ | modules/graphs |
| **W3** | R-01~R-05 | 5 | ✅ | modules/rulesets |
| **W3** | D-01~D-03 | 3 | ✅ | modules/dsl |
| **W4 Connector** | B-01~B-04 | 4 | ✅ | os_core/connector_sdk/runtime |
| **W4 Connector** | C-02~C-04 | 3 | ✅ | 同上 |
| **W4 Registry** | ADR-008 读+变更 | 5 | ✅ | modules/registry |
| **契约** | contract openapi/schema | 11 | ✅ | router 全域挂载 |
| **工作流** | plan · step-chain · registry | 14 | ✅ | registry harness |
| **静态** | import boundaries · redundancy | 2 | ✅ | — |
| **合计** | `not pending` | **72** | **全绿** | — |
| pending（预期红） | AC-BASE 等 | 20 | 未跑 | W5+ |

### 三、harness / gate

```bash
pytest not pending: 72 passed
harness --tier full: 8 checks OK
static quality (ruff+pyright): OK
gate plan: OK
check_legacy_paths: OK
```

### 四、开发者入口（v6 真源）

- HTTP：`src/server/api/router/v1/registry.py`
- 内核：`src/server/os_core/registry.py`
- GIP：`src/integration/registry.py`
- Plan：`_factoryos_pipeline/plan/plan-api-v6-full-structure.md`
