# PR 变更摘要：W2 — audit_service · execution shadow/幂等

- **plan**：`_factoryos_pipeline/2026-06-25/plan/plan-1809-w2-audit-execution.md`
- **日期**：2026-06-26

## 标题建议

`feat(w2): audit append-only · execution dry_run/idempotency · evidence API`

## 变更背景（Why）

W2 目标：落地 append-only 审计 + 唯一写入口 execution（试跑/幂等/mock），为 W3 Rule/Graph 铺路。

## 主要改动（What）

| 模块 | 路径 | 说明 |
|------|------|------|
| 迁移 | `alembic/versions/002_audit_execution.py` | audit_events · execution_records |
| audit | `os_core/audit_service/` | append-only store |
| execution | `os_core/execution_service/` | execute · assemble_evidence |
| connector | `connector_sdk/mock_legacy.py` | E-06/E-07 写计数 |
| API | `routes/audit.py` · `execute.py` · `executions.py` | E-03 · execute · E-09 |
| 测试 | `tests/integration/` W2 套件 | E-03/06/07/09 |

## AC 通过情况

| AC ID | 结果 | Step |
|-------|------|------|
| E-03 | PASS | 2 |
| E-06 | PASS | 3 |
| E-07 | PASS | 3 |
| E-09 | PASS | 4 |
| 52 P0 其余 | pending（W3+） | — |

## 测试结论

```bash
uv run pytest src/tests/contract src/tests/workflow src/tests/integration -m 'not pending'  # 25 passed
uv run python scripts/gate_cli.py pr   # OK
```

Test 终轮：`test-1105-w2-final-regression.md`

## Summary（3 条）

1. W2 交付 audit append-only + `GET /v1/audit/events`（E-03）。
2. execution_service 唯一入口：dry_run simulated（E-06）+ idempotency（E-07）。
3. `GET /v1/executions/{execId}/evidence` ExecutionEvidence 聚合（E-09）；52 P0 其余仍 pending。
