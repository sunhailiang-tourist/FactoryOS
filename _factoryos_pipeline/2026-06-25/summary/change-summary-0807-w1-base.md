# PR 变更摘要：W1 基座首轮 — 工程骨架与契约落地

- **plan**：`_factoryos_pipeline/2026-06-25/plan/plan-0116-w1-base.md`
- **日期**：2026-06-25

## 标题建议（PR title）

`feat(w1): W1 基座 — shared_contracts · Alembic S-01～S-04 · mock connector health`

## 变更背景（Why）

W1 目标：把「文档契约」变成可编译、可迁移、可测的工程底座，为 W2 audit/execution 铺路；不含 Graph/Rule/Execution 业务闭环。

## 主要改动（What）

| 模块 | 文件/路径 | 说明 |
|------|-----------|------|
| Step1 工程底座 | `pyproject.toml` · `server/api/main.py` | FastAPI + `/health` · uv 依赖封版 |
| Step2 契约 | `os_core/shared_contracts/` | 7 Schema Pydantic · errors · schema_loader |
| Step3 规模预埋 | `alembic/` · `tenant_registry.py` · `outbox.py` | S-01～S-04 四表 + seed + 端口 |
| Step4 Connector | `connector_sdk/health.py` · `server/api/modules/*/controllers/connectors.py` | C-01 mock health |
| 集成占位 | `src/integration/catalog/conn-mock.yaml` | mock Pack |
| 测试 | `src/tests/workflow` · `contract` · `integration` | W1 AC 子集 failing→绿 |
| 治理 | `.cursor/rules/项目结构变更门禁.mdc` | 新建目录须用户确认 + README |

## AC 通过情况

| AC ID | 结果 | Step |
|-------|------|------|
| workflow | PASS | 1 |
| contract | PASS | 2 |
| S-01～S-04 | PASS | 3 |
| C-01 | PASS | 4 |
| 52 P0 其余 | **pending**（预期红，W8 Gate 0） | — |

## 业务口径确认（Behavior）

- 无 Legacy 写；无 execution/graph/rule 运行时
- `GET /health` 探针；`GET /v1/connectors/{packId}/health` mock 返回 `status=ok`
- 默认 tenant `default` → `cell-default` / `pool`

## 风险与兼容性

- SQLite 测试用 `cache=shared` + Alembic connection 注入（见 `alembic/env.py`）
- httpx 0.28 → 集成测试改用 FastAPI `TestClient`
- `alembic/` 为长期 migration 目录，非临时脚手架

## 测试结论（Test）

```bash
.venv/bin/python scripts/gate_cli.py step --step 1 -k 'workflow'  # 绿
.venv/bin/python scripts/gate_cli.py step --step 2 -k 'contract'  # 绿
.venv/bin/python scripts/gate_cli.py step --step 3 -k 'S-01'      # 绿
.venv/bin/python scripts/gate_cli.py step --step 4 -k 'C-01'      # 绿
.venv/bin/python scripts/gate_cli.py pr                           # 绿（2026-06-25）
```

Verify：`verify-1519-step1` · `verify-1532-step2` · step3 · `verify-1558-step4`

## Summary（3 条，可贴 PR）

1. W1 交付 FastAPI 工程底座 + `shared_contracts` 七 Schema Pydantic 对齐 `contracts/schemas`。
2. Alembic `001_scale_s01_s04` 预埋 ADR-007 规模表（S-01～S-04）+ TenantRegistry/OutboxPort。
3. mock `connector_sdk` health 路由通过 C-01；52 P0 其余仍 pending，Gate 0 留 W8。
