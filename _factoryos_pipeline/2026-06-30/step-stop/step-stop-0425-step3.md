# Step 停机：Step 3 — POST `/v1/harness/confirm` + H-02

- **plan**：`_factoryos_pipeline/2026-06-30/plan/plan-0330-w5-agent-harness.md`
- **时间**：2026-06-30

## 1. Step 标识

Step 3 — POST `/v1/harness/confirm` · H-02（confirm→execute）

## 2. 改动文件

| 路径 | 变更 |
|------|------|
| `src/server/api/modules/harness/` | 新增 harness 域 · confirm_flow 编排 |
| `src/server/api/router/v1/registry.py` | 登记 `harness.get_routers` |

## 3. AC / 接口

| AC ID | 接口 | 结果 |
|-------|------|------|
| H-02 | POST `/v1/harness/confirm` | ✅ pytest 绿 |

## 4. 架构要点

| 项 | 处理 |
|----|------|
| 编排位置 | API `application/confirm_flow.py`（agent_orchestrator import 边界） |
| 确认门 | `harness.confirmed` audit → `execution_service.execute` |
| reject | 未知 plan → 404 · confirmed=false → audit reject + 返回 plan |

## 5. 十项自检

| # | 项 | 结果 |
|---|-----|------|
| 1 | 分层/写路径 | Pass — confirm 后走 execution |
| 2 | 响应契约 | Pass — ExecutionRecord |
| 3 | 鉴权/租户 | Pass |
| 4 | 红线 R11 | Pass — plan 阶段无写 |
| 5 | Schema | Pass |
| 6 | 输入校验 | Pass |
| 7 | Shadow | Pass — dry_run=true → simulated |
| 8 | 幂等 | Pass — step idempotency_key |
| 9 | 静态 | Pass |
| 10 | 注释 | Pass |

## 6. Harness 结果

```bash
uv run pytest src/tests/integration/test_harness_w5.py -k 'H-02' -q
uv run python scripts/check_import_boundaries.py
```

## 7. Verify

- 口令：`【Verify回合】Step 3`

## 8. 等待

Test 验收 → Verify → `gate step --step 3 -k 'H-02'` → **`可以继续`**
