# Step 停机：W2 Step 4 — evidence HTTP + E-09

- **plan**：`_factoryos_pipeline/2026-06-25/plan/plan-1809-w2-audit-execution.md`
- **时间**：2026-06-26

## 1. Step 标识

W2 Step 4 — `GET /v1/executions/{execId}/evidence` · ExecutionEvidence 组装

## 2. 改动文件

| 路径 | 变更 |
|------|------|
| `src/os_core/execution_service/store.py` | `find_by_exec_id` |
| `src/os_core/execution_service/service.py` | `assemble_evidence` |
| `src/os_core/execution_service/__init__.py` | 导出 `assemble_evidence` |
| `src/apps/api/routes/executions.py` | **新增** evidence 薄路由 |
| `src/apps/api/main.py` | 注册 executions router |
| `src/os_core/execution_service/README.md` | E-09 验收盘 |
| `src/apps/api/routes/README.md` | 路由表 |

## 3. AC

| AC ID | 结果 |
|-------|------|
| E-09 | PASS — execute 后 GET evidence 200 · required 字段齐全 · audit_events ≥ 1 |

## 4. 十项自检

| 项 | 结果 |
|----|------|
| 未超 plan | Pass — 仅 evidence 路由 + os_core 组装 |
| apps/api 薄路由 | Pass |
| 业务在 os_core | Pass |
| 中文注释 | Pass |
| import 边界 | Pass |
| 无 tenant 分支 | Pass |
| audit append-only | Pass |
| dry_run/幂等未破坏 | Pass（存量用例复跑） |
| OpenAPI 对齐 | Pass — path + 404 |
| README 更新 | Pass |

## 5. 本地 pytest

```bash
uv run pytest src/tests/integration/test_execution_e09.py -k 'E-09' -v
uv run pytest src/tests/integration/test_audit_e03.py src/tests/integration/test_execution_e06_e07.py -q
```

## 6. Harness（待 Test/Verify）

```bash
./scripts/gate step --step 4 -k 'E-09'
```

## 7. 下一步

1. `【Test·Step 4 验收】`
2. `【Verify回合】Step 4`
3. gate step 4 绿 → W2 终轮 `gate delivery` · `gate pr`
