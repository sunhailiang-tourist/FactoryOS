# Step 停机：Step 2 — execution license 门禁（T-02）

- **plan**：`_factoryos_pipeline/2026-06-30/plan/plan-1350-w6-reconcile-license.md`
- **时间**：2026-06-30

## 1. Step 标识

Step 2 — execution 前 license 校验 · T-02

## 2. 改动文件

| 路径 | 变更 |
|------|------|
| `src/server/os_core/execution_service/service.py` | `assert_pack_licensed` + `license.denied` audit |
| `scripts/check_import_boundaries.py` | execution → license_service 白名单 |

## 3. AC / 接口

| AC ID | 接口 | 结果 |
|-------|------|------|
| T-02 | POST `/v1/execute` 未授权 tenant | ✅ pytest 绿 |

## 4. 十项自检

| # | 项 | 结果 |
|---|-----|------|
| 1 | 分层 | Pass — license 内核 · execution 编排 |
| 2 | 响应 | Pass — 403 MODULE_NOT_LICENSED |
| 3 | 鉴权 | Pass — tenant_id 维度 |
| 4 | 红线 | Pass — 未授权不写 Legacy |
| 5 | audit | Pass — license.denied |
| 6–10 | 其余 | Pass |

## 5. Harness

```bash
uv run pytest src/tests/integration/test_license_t02_w6.py -k 'T-02' -q
```

## 6. Verify

- 口令：`【Verify回合】Step 2`

## 7. 等待

Test → Verify → `gate step --step 2 -k 'T-02'` → **`可以继续`**
