# Step 停机：Step 4 — mock connector_sdk + C-01

- **plan**：`_factoryos_pipeline/2026-06-25/plan/plan-0116-w1-base.md`
- **时间**：2026-06-25

## 1. Step 标识

Step 4 — Connector 接入占位（mock health · C-01）

## 2. 改动文件

| 路径 | 变更 |
|------|------|
| `src/server/os_core/connector_sdk/__init__.py` | 包导出 |
| `src/server/os_core/connector_sdk/health.py` | `check_connector_health` mock |
| `src/server/api/modules/*/controllers/connectors.py` | `GET /v1/connectors/{pack_id}/health` |
| `src/server/api/main.py` | 挂载 connectors router |
| `src/integration/catalog/conn-mock.yaml` | mock Pack 占位 |

## 3. AC

| AC ID | 结果 |
|-------|------|
| C-01 | PASS — 200 · status=ok · pack_id 回显 |

## 4. 十项自检

全 Pass（api 薄路由 · 无 Legacy 写 · 无业务规则 · 注释齐全）

## 5. Harness

```bash
.venv/bin/python scripts/gate_cli.py step --step 4 -k 'C-01'
```

harness + pytest：**PASS** · verify：**MISSING**

## 6. 验证

```bash
uv run pytest src/tests/integration/test_connector_c01.py -v
```

## 7. Verify

`【Verify回合】Step 4`

## 8. W1 完成

Step 4 gate + Verify 全绿后 → **W1 plan 四 Step 完工** → 可写 `summary/` · `gate pr`
