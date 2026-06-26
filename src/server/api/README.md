# server/api · HTTP API

## 是什么

**FastAPI** Control Plane 入口；Modular Monolith **唯一 deployable**（import: `server.api`）。

## 开发者阅读顺序

```text
main.py  →  application/  →  router/  →  modules/  →  config/
```

| 路径 | 职责 | README |
|------|------|--------|
| `main.py` | Uvicorn 入口（仅 export app） | — |
| `application/` | 应用创建与装配 | [application/README.md](./application/README.md) |
| `router/` | **HTTP 路由第一站** | [router/README.md](./router/README.md) |
| `modules/` | 业务域 HTTP 实现 | [modules/README.md](./modules/README.md) |
| `config/` | settings · logs · tenant · middleware 等 | [config/README.md](./config/README.md) |

## 主要功能

- REST `/v1/*` 对齐 OpenAPI v1.1.1
- `/v1/registry/*` Platform Registry 只读 API（ADR-008）
- 调用 `os_core` public API，**不含** 业务规则实现

## 不负责什么

- 在路由层重复 `os_core` 已有能力
- 绕过 Rule / Harness 写 Legacy

## 上下游

- **上游**：`src/apps/web-admin`、`src/apps/h5-worker`、第三方集成
- **下游**：`os_core/*` · Platform Registry · PostgreSQL

## 本地开发

```bash
uv sync --extra dev
uv run uvicorn server.api.main:app --reload --host 127.0.0.1 --port 8000
curl -s http://127.0.0.1:8000/health
curl -s http://127.0.0.1:8000/v1/registry/health
```

## Studio 数据

- `src/server/api/data/studio_flows.json` — Studio 状态机模型（自 `flows.json` 迁入）

## 相关文档

- [ADR-008](../../docs/文档/架构/架构决策记录-008-配置与契约平面DB化.md)
- `contracts/openapi/` export 镜像
