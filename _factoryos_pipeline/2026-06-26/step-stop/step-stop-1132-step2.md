# Step 停机：Step 2 — Graph 生命周期 HTTP + G-03/06/08

- **plan**：`_factoryos_pipeline/2026-06-26/plan/plan-1121-w3-graph-rule.md`
- **时间**：2026-06-26 11:32（补录 · 对照终轮 `test-1132`）

## 1. Step 标识

Step 2 — Graph 生命周期 HTTP + G-03/06/08（harness `-k 'G-05'`）

## 2. 改动文件

| 路径 | 变更 |
|------|------|
| `src/os_core/graph_service/service.py` | submit · freeze · clone · deprecate |
| `src/apps/api/routes/graphs.py` | Graph HTTP 薄路由 |
| `src/apps/api/routes/error_handlers.py` | `PlatformError` → HTTP |
| `src/apps/api/main.py` | 注册 graphs 路由 |
| `src/tests/integration/test_graph_w3.py` | G-02～G-08 用例 |

## 3. AC / 接口

| AC ID | 接口 / 行为 | 结果 |
|-------|-------------|------|
| G-02 | `PUT` draft 可改 | **PASS** |
| G-03 | draft graph execute → 409 `GRAPH_NOT_FROZEN` | **PASS** |
| G-04 | submit → in_review | **PASS** |
| G-05 | freeze + frozen ruleset + checksum | **PASS** |
| G-06 | frozen PUT → 409 | **PASS** |
| G-07 | clone → v1.0.1 draft | **PASS** |
| G-08 | deprecated execute → 409 | **PASS** |

## 4. 十项自检（Pass/Fail）

| # | 项 | 结果 |
|---|-----|------|
| 1 | 分层/写路径 | Pass — HTTP 委托 service |
| 2 | 响应契约 | Pass — 生命周期状态码对齐 OpenAPI |
| 3 | 鉴权/租户 | Pass — plan 范围外 |
| 4 | 红线 | Pass — G-03 阻断未 freeze 写 |
| 5 | Schema | Pass — freeze 绑定 ruleset |
| 6 | 输入校验 | Pass |
| 7 | Shadow | N/A |
| 8 | 幂等/补偿 | N/A |
| 9 | 静态检查 | Pass |
| 10 | 注释 | Pass — routes/graphs.py 文件头 |

## 5. Harness 结果

```bash
./scripts/gate step --step 2 -k 'G-05'
```

```text
gate step : PASS（G-05 + G-03/06/08 同套件绿）
```

## 6. 最短验证路径

```bash
uv run pytest src/tests/integration/test_graph_w3.py -k 'G-0' -v
```

## 7. Verify（必填）

- 落盘：`verify/verify-1140-step2.md`
- 结论：通过

## 8. 等待

请回复：`可以继续`
