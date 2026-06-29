# Step 停机：Step 1 — Alembic 003 + graph_service 内核 CRUD

- **plan**：`_factoryos_pipeline/2026-06-26/plan/plan-1121-w3-graph-rule.md`
- **时间**：2026-06-26 11:32（补录 · 对照终轮 `test-1132`）

## 1. Step 标识

Step 1 — Alembic 003 + `graph_service` 内核 CRUD（G-01）

## 2. 改动文件

| 路径 | 变更 |
|------|------|
| `src/server/db/migrations/versions/003_graphs_rulesets.py` | 新增 `business_graphs` · `rulesets` 表 |
| `src/server/os_core/graph_service/__init__.py` | 包入口 |
| `src/server/os_core/graph_service/store.py` | Graph ORM · CRUD |
| `src/server/os_core/graph_service/service.py` | draft 创建 · 版本查询 |
| `src/server/os_core/graph_service/checksum.py` | sha256 校验和 |
| `src/server/os_core/graph_service/README.md` | 模块说明 |
| `src/tests/integration/w3_helpers.py` | W3 测试夹具 |
| `src/tests/integration/test_graph_w3.py` | G-01 用例（Step1 范围） |

## 3. AC / 接口

| AC ID | 接口 / 证据 | 结果 |
|-------|-------------|------|
| G-01 | `POST /v1/graphs` → draft | **PASS** |
| harness | `-k 'G-01'` | **PASS** |

## 4. 十项自检（Pass/Fail）

| # | 项 | 结果 |
|---|-----|------|
| 1 | 分层/写路径 | Pass — 业务在 `os_core/graph_service` |
| 2 | 响应契约 | Pass — 201 + status=draft |
| 3 | 鉴权/租户 | Pass — W3 plan 未要求本步鉴权 |
| 4 | 红线 | Pass — Graph 不写 Legacy |
| 5 | Schema | Pass — 003 对齐 OpenAPI Graph |
| 6 | 输入校验 | Pass — Pydantic 校验 graph body |
| 7 | Shadow | N/A |
| 8 | 幂等/补偿 | N/A — 本步仅 CRUD 内核 |
| 9 | 静态检查 | Pass — ruff · pyright 绿 |
| 10 | 注释 | Pass — README + 文件头 |

## 5. Harness 结果

```bash
./scripts/gate step --step 1 -k 'G-01'
```

```text
gate step : PASS（补录前已跑录 · test_G01_create_draft_graph 绿）
```

## 6. 最短验证路径

```bash
uv run pytest src/tests/integration/test_graph_w3.py -k G-01 -v
```

## 7. Verify（必填）

- 落盘：`verify/verify-1140-step1.md`
- 结论：通过
- 口令：`【Verify回合】Step 1`

## 8. 等待

请回复：`可以继续` 或 `测试不通过` + 现象
