# Verify 回合：Step 3 — Alembic 规模预埋 S-01～S-04

> **独立只读审阅**（与 Dev 实现会话隔离）。

- **plan**：`_factoryos_pipeline/2026-06-25/plan/plan-0116-w1-base.md`
- **step-stop**：`_factoryos_pipeline/2026-06-25/step-stop/step-stop-0740-step3.md`
- **对照 AC**：S-01 · S-02 · S-03 · S-04

## 1. 只读输入（Verify Agent 已阅读）

- [x] plan Step 3 段落（§6 Step 3）
- [x] `git diff` 本 Step 改动（`src/server/db/migrations/**` · `tenant_registry.py` · `outbox.py` · `conftest.py` · integration 测试）
- [x] step-stop 十项自检
- [x] ADR-007 表清单与 migration `001_scale_s01_s04.py` 对账

## 2. 核对项（Pass/Fail）

| # | 项 | 结果 | 证据 |
|---|-----|------|------|
| 1 | 未超 plan 范围 | **Pass** | 仅 Alembic 四表 + seed + TenantRegistry/OutboxPort 端口；无新 HTTP、无 connector/Legacy 写。改动与 step-stop §2 一致。 |
| 2 | 写路径 / R-01–R-11 | **Pass** | 仅 DB 预埋与 outbox 行插入（测试/端口）；无 execution 写 Legacy。import_boundaries 绿。 |
| 3 | AC 断言可测 | **Pass** | gate `-k 'S-01'`：**1 passed**；全文件 integration：**4 passed**（S-01～S-04）。四表 + `cell_id/placement_tier/region` 列 · default seed · `get_cell` → `cell-default` · outbox insert 均覆盖。 |
| 4 | 无重复逻辑迹象 | **Pass** | `migrated_db_session` 与 S-01 测试各自独立 upgrade 路径（略重复但职责清晰）；端口类无 api 层重复。redundancy check 绿。 |
| 5 | 注释四要素 | **Pass** | migration · env · tenant_registry · outbox 文件头 + 方法 docstring 齐全；`alembic.ini` 有说明注释。 |

## 3. 机械门禁复跑

```bash
.venv/bin/python scripts/gate_cli.py step --step 3 -k 'S-01'
```

| 子门禁 | 结果 |
|--------|------|
| harness full + pytest `-k 'S-01'` | PASS（1 passed） |
| static quality（ruff + pyright） | PASS |
| verify 落盘 | 本文件 |

**补充**：`pytest src/tests/integration/test_scale_s01_s04.py` 全量 **4 passed**（S-02～S-04 在 gate 子集外，手工复跑绿）。

## 4. 结论（必填 · gate 检查）

结论：通过

阻断理由（若有）：无

## 5. 建议（3 条以内）

1. `gate step --step 3` 仅 `-k 'S-01'` 时 S-02～S-04 不进验收盘；可在 W1 末 `gate pr` 前确认 integration 全绿，或后续扩展 step gate 的 `-k` 覆盖。
2. `TenantRegistry.get_cell` 在 tenant 不存在时回退 `cell-default` 为 S0 设计；S2 跨 Cell 路由前应改为显式失败或审计。
3. `OutboxPort.publish` 内 `commit()` 与调用方事务边界需在 W2 execution 接入时统一（当前 W1 验收足够）。
