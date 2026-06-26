# Step 停机：Step 4 — DSL registry + execution 门禁 + E-01

- **plan**：`_factoryos_pipeline/2026-06-26/plan/plan-1121-w3-graph-rule.md`
- **时间**：2026-06-26 11:32（补录 · 对照终轮 `test-1132`）

## 1. Step 标识

Step 4 — DSL registry + execution 门禁链 + E-01（harness `-k 'E-01'`）

## 2. 改动文件

| 路径 | 变更 |
|------|------|
| `src/os_core/shared_contracts/cmv_registry.py` | CMV yaml 动词白名单 |
| `src/os_core/shared_contracts/exceptions.py` | `PlatformError` · `ErrorCode` |
| `src/os_core/execution_service/service.py` | graph→rule→DSL 门禁链 |
| `src/apps/api/routes/dsl.py` | `GET /v1/dsl/registry` |
| `src/tests/integration/test_dsl_w3.py` | D-01～D-03 |
| `src/tests/integration/test_execution_e01.py` | E-01 L0 QUERY |

## 3. AC / 接口

| AC ID | 接口 / 行为 | 结果 |
|-------|-------------|------|
| D-01 | `GET /v1/dsl/registry` | **PASS** |
| D-02 | 未知 verb → 400 `DSL_UNKNOWN` | **PASS** |
| D-03 | graph allowed_dsl 外 → 403 `DSL_NOT_IN_GRAPH` | **PASS** |
| E-01 | `QUERY_ENTITY` on frozen · 0 Legacy write | **PASS** |
| W2 回归 | E-03/06/07/09 | **PASS**（终轮 42/42） |

## 4. 十项自检（Pass/Fail）

| # | 项 | 结果 |
|---|-----|------|
| 1 | 分层/写路径 | Pass — 门禁在 execution_service |
| 2 | 响应契约 | Pass — ErrorCode 映射 HTTP |
| 3 | 鉴权/租户 | Pass |
| 4 | 红线 | Pass — E-01 不写 Legacy |
| 5 | Schema | Pass — CMV 动词表 |
| 6 | 输入校验 | Pass — require_known_verb |
| 7 | Shadow | N/A |
| 8 | 幂等/补偿 | Pass — W2 E-07 未破坏 |
| 9 | 静态检查 | Pass |
| 10 | 注释 | Pass — execution README 更新 |

## 5. Harness 结果

```bash
./scripts/gate step --step 4 -k 'E-01'
```

```text
gate step : PASS · gate pr : PASS · 终轮 42 passed
```

## 6. 最短验证路径

```bash
uv run pytest src/tests/integration/test_dsl_w3.py src/tests/integration/test_execution_e01.py -v
uv run pytest src/tests/integration/test_audit_e03.py test_execution_e06_e07.py test_execution_e09.py -q
```

## 7. Verify（必填）

- 落盘：`verify/verify-1140-step4.md`
- 结论：通过

## 8. 等待

W3 四步闭合 → `【Test·终轮回归】` → `gate delivery`
