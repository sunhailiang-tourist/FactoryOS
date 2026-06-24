# .cursor · Agent 与研发治理根目录

> 仓库根 [README.md](../README.md) 是新人第一入口；本目录是 **Cursor Agent 协作真源**。  
> **产品对外主路径**（接入/扩展）= 管理台 UI，见 [factoryos/UI-FIRST-CONFIG-PRINCIPLE.md](factoryos/UI-FIRST-CONFIG-PRINCIPLE.md)。

## 三区隔离

```text
.cursor/
├── factoryos/          # 研发测试工作流（执行真源 · SH-步步流 T4.5+）
├── docs-baseline/      # docs/ 认知基线（漂移检测 · 非执行真源）
├── ai_chat_history/    # 创建期对话归档（决策史 · 非运行时真源）
├── rules/              # Cursor Rules（.mdc · 自动/口令加载）
└── hooks/              # Cursor Hooks（路径保护 · harness 提示）
```

| 区 | 何时读 | 入口 |
|----|--------|------|
| **factoryos** | 每轮 Dev/Test/Verify · 产品宪法 | [factoryos/INDEX.md](factoryos/INDEX.md) |
| **docs-baseline** | 大改 `docs/` 后 | [docs-baseline/BASELINE.md](docs-baseline/BASELINE.md) |
| **rules** | Agent 自动加载 | [rules/SH-步步流.mdc](rules/SH-步步流.mdc) |
| **hooks** | 激活 Cursor 后 | [factoryos/ACTIVATION.md](factoryos/ACTIVATION.md) |
| **ai_chat_history** | 还原创建期决议与行为链 | [ai_chat_history/2026-06-24-FactoryOSCreateChatHistory.md](ai_chat_history/2026-06-24-FactoryOSCreateChatHistory.md) |

## 开发前一条链

详见 **[factoryos/PRE-DEV-CHAIN.md](factoryos/PRE-DEV-CHAIN.md)**（全链路盘点 · 维护地图 · 可追踪线索）。

## 与仓库其他真源

```text
contracts/     机器契约（OpenAPI · Schema · AC）
src/           代码（os_core · apps · integration · tests）
scripts/       gate · harness · docs_baseline
_factoryos_pipeline/   运行时落盘（过程产物 + 强制结论 dev/test/verify）
docs/          厚文档（可选外迁；变更用 docs-baseline 检测）
rules/         参考存档（非真源 · 见 rules/README.md）
```
