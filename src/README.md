# src · 代码根目录

> 布局与 [仓库根 README](../README.md) 一致；契约在 `contracts/`，工作流在 `.cursor/factoryos/`。  
> **对外实施主路径**：`apps/web-admin` Integration Studio — [UI-FIRST](../.cursor/factoryos/UI-FIRST-CONFIG-PRINCIPLE.md)

## 结构

```text
src/
├── os_core/        # 平台内核九模块（唯一写 Legacy 经 execution_service）
├── apps/           # api · web-admin · h5-worker · edge-agent
├── integration/    # catalog · packs · tenants · tools（GIP 集成层）
└── tests/          # contract · workflow · ac（Gate 0 验收）
```

## 开发顺序（Phase 1 · W1–W8）

见 `.cursor/rules/工厂操作系统.md` §开发顺序；首轮：**shared_contracts → audit → execution → graph/rule → connector → agent → integration 样例**。

## 门禁

| 改动 | 建议命令 |
|------|----------|
| 任意 Python | `./scripts/harness --tier auto` |
| 仅 tests | `uv run pytest src/tests/ -k 'AC-ID'` |
| Step 停机 | `./scripts/gate step --step N -k 'AC-ID'` |

## 入口 README

| 目录 | 说明 |
|------|------|
| [os_core/](os_core/README.md) | 内核 |
| [apps/](apps/README.md) | 应用 |
| [integration/](integration/README.md) | 集成层 |
| [tests/](tests/README.md) | 测试 |

## 开发前全链路

[.cursor/factoryos/PRE-DEV-CHAIN.md](../.cursor/factoryos/PRE-DEV-CHAIN.md)
