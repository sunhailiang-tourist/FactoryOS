# Step 停机：Step 1 — license_service 内核 stub

- **plan**：`_factoryos_pipeline/2026-06-30/plan/plan-1350-w6-reconcile-license.md`
- **时间**：2026-06-30

## 1. Step 标识

Step 1 — license_service · `assert_pack_licensed`（workflow）

## 2. 改动文件

| 路径 | 变更 |
|------|------|
| `src/server/os_core/license_service/__init__.py` | 包入口 |
| `src/server/os_core/license_service/service.py` | 静态 licensed 列表 stub |

## 3. AC / 接口

| AC ID | 接口 | 结果 |
|-------|------|------|
| workflow | `assert_pack_licensed(tenant, pack)` | ✅ pytest 绿 |

## 4. 架构要点

| 项 | 处理 |
|----|------|
| stub 数据 | `default` → `conn-mock`；其他 tenant 空集 |
| import 边界 | 仅 `shared_contracts` |
| Step2 | execution 钩子 + audit（T-02） |

## 5. Harness 结果

```bash
uv run pytest src/tests/integration/test_license_w6_step1.py -k workflow -q
uv run python scripts/check_import_boundaries.py
```

## 6. Verify

- 口令：`【Verify回合】Step 1`

## 7. 等待

Test 复验 → Verify → `gate step --step 1 -k 'workflow'`
