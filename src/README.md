# src · 核心代码、测试与 integration export 镜像

> **代码根**：`src/server/`（内核 + API + 迁移）· `src/apps/`（Web/H5 客户端壳）  
> **对外实施主路径**：`src/apps/web-admin` Integration Studio — [UI-FIRST](../.cursor/factoryos/UI-FIRST-CONFIG-PRINCIPLE.md)

## 结构

```text
src/
├── server/         # os_core · api · db/migrations · edge-agent（import: os_core.* · server.api.*）
├── apps/           # web-admin · h5-worker
├── integration/    # export/fixture 镜像（非编辑真源 · ADR-008）
└── tests/          # contract · workflow · integration · ac
```

## 门禁

| 改动 | 建议命令 |
|------|----------|
| 任意 Python | `./scripts/harness --tier auto` |
| 仅 tests | `uv run pytest src/tests/ -k 'AC-ID'` |
| Step 停机 | `./scripts/gate step --step N -k 'AC-ID'` |

## 入口 README

| 目录 | 说明 |
|------|------|
| [server/](server/README.md) | 服务端 |
| [apps/](apps/web-admin/README.md) | 客户端壳 |
| [integration/](integration/README.md) | export 镜像 |
| [tests/](tests/README.md) | 测试 |

## 开发前全链路

[.cursor/factoryos/PRE-DEV-CHAIN.md](../.cursor/factoryos/PRE-DEV-CHAIN.md)
