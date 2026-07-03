# Step 停机：Step 6 — DSL D-04 · Agent E-08

- **plan**：`_factoryos_pipeline/2026-07-01/plan/plan-0900-w7-gate0-gip-mcp.md`
- **时间**：2026-07-01

## 1. Step 标识

Step 6 — L2 无 compensator 拒绝注册 · orchestrator 禁 connector 写路径

## 2. 改动文件

| 路径 | 变更 |
|------|------|
| `shared_contracts/cmv_registry.py` | `register_dsl_verb` · L2/L3 compensator 校验 |
| `api/modules/registry/controllers/registry.py` | POST `/v1/registry/cmv/verbs` 薄路由 |

## 3. 落位说明

- **D-04**：`register_dsl_verb` 对齐 `check_cmv_sync`；L2/L3 无 compensator → `PlatformError` 422
- **E-08**：无代码改动（agent_orchestrator 已不含 forbidden 字符串）

## 4. AC / 接口

| AC ID | 接口 | 结果 |
|-------|------|------|
| D-04 | POST `/v1/registry/cmv/verbs` L2 + compensator=null | ✅ 422 · compensator |
| E-08 | agent_orchestrator 静态扫描 | ✅ 无 connector 写路径 |

## 5. Harness

```bash
uv run pytest src/tests/integration/test_dsl_e08_w7.py -v
```

## 6. Verify

- 口令：`【Verify回合】Step 6`

## 7. 等待

Test Step 6 验收 → Verify → `gate step --step 6 -k 'D-04'`
