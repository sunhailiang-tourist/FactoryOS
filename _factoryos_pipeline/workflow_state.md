# SH-步步流 · 工作流状态机

> Agent **每次收到关键词后必须更新本文件**。Hook 据此机械拦截越权写码。  
> 真源说明：[ACTIVATION.md](../.cursor/factoryos/ACTIVATION.md)

```yaml
phase: STEP0
agent: dev
step: 0
plan:
test_plan:
updated: 2026-06-16
```

## phase 取值

| phase | 解锁条件（用户关键词） | 允许写入 |
|-------|------------------------|----------|
| `STEP0` | 初始 / 新一轮 | `_factoryos_pipeline/` · `contracts/` · `scripts/` · `.cursor/` · `docs/` · `*.md` |
| `PLANNING` | `可以继续`（Step0 通过） | + `plan/` 落盘 |
| `CAN_TEST` | `确认规划` | + `test/` · `src/tests/**` |
| `CAN_CODE` | `可以开始` | + `src/os_core/**` · `src/apps/**` · `src/integration/**` 业务代码 |
| `DELIVERY` | 整体测试通过 | summary；准备 PR |

## agent 取值

| agent | 激活口令 | 写权限 |
|-------|----------|--------|
| `dev` | `【Dev模式启动】` | 按 phase；业务码需 `CAN_CODE` |
| `test` | `【Test模式启动】` | **仅** `src/tests/**` + `_factoryos_pipeline/` |

## 变更日志

- 2026-06-16 初始化 · 治理包落地
