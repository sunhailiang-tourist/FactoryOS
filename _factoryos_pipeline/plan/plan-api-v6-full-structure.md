# Plan · API v6-full 结构落位 + Registry Harness 闭环

> 状态：**已确认规划**（2026-06-26）  
> 目标：按 v6-full 落位 `server/api` + `os_core/registry` + harness 闭环，**零 API 行为变更**

## AC（回归锚点 · 零行为变更）

| ID | 验收 |
|----|------|
| C-01 | `GET /v1/connectors/{packId}/health` 行为不变 |
| G-01 | `POST /v1/graphs` 行为不变 |
| E-03 | `GET /v1/audit/events` 行为不变 |
| workflow | `GET /health` 200（W1 Step1） |

结构门禁（harness）：

- `check_kernel_registry.py` — os_core/registry.py ↔ 磁盘 10 模块
- `check_router_registry.py` — router/v1/registry.py ↔ modules/*/routers.py
- `main.py` 禁止 `include_router`

## Steps

### Step 1 — 骨架 + registry + harness 脚本
- application/ · router/ · config/ · modules/probes
- os_core/registry.py · integration/registry.py
- scripts/check_*_registry.py · check_harness 注册

### Step 2 — 域迁移 routes → modules/*/controllers
- 8 业务域 + probes
- deps → config/dependencies/db.py
- error_handlers → config/status_code/handlers.py

### Step 3 — 纵向 config 占位（S0 pass-through）
- auth/tenant/quota middleware 骨架
- shared_contracts/context.py

### Step 4 — 文档同步 + 删废止 routes/

## 废止

- `server/api/modules/*/controllers/` 平铺
- `main.py` 手写 include_router
