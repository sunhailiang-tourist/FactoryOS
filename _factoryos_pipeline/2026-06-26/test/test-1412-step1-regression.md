# Step 1 单步验收 · Test 硬性验收报告

- **对照 plan**：`_factoryos_pipeline/2026-06-26/plan/plan-1339-w4-connector-runtime.md` · Step 1
- **命名**：`test-1412-step1-regression.md`
- **口令**：`【Test·Step 1 验收】`（对照 `step-stop-1405-step1.md`）

## 1. git diff 改动面（本 Step）

| 路径 | 变更 | plan 预期落位 | 实际落位 | 结论 |
|------|------|---------------|----------|------|
| `src/os_core/connector_sdk/registry.py` | 新增 | Step1 registry | ✅ | PASS |
| `src/os_core/connector_sdk/runtime/` | 骨架 | Step1 包骨架 | ✅ 仅 `__init__` + README | PASS |
| `src/integration/catalog/conn-mock.yaml` | 扩展 | ConnectorBlueprint | ✅ GOVERNED_WRITE + revert | PASS |
| `src/os_core/shared_contracts/errors.py` | 增码 | BLUEPRINT_INVALID 等 | ✅ | PASS |
| `src/os_core/connector_sdk/__init__.py` | 导出 | registry 公开面 | ✅ | PASS |
| `src/os_core/connector_sdk/runtime/execute.py` | — | Step2 | ❌ 未实现 | 符合分步 |

**超 plan 说明**：`validate_blueprint`（B-04 内核校验）在 Step1 一并落地；无 `execute_op` / HTTP revert，未抢 Step2–4 范围。

## 2. 本 Step 硬性验收计划（执行记录）

| AC ID | 验收项 | pytest / 证据 | 结果 |
|-------|--------|---------------|------|
| B-01 | 加载 conn-mock · ops 含 GOVERNED_WRITE | `test_B01_*` | **PASS** |
| B-04 | L2 无 revert → BLUEPRINT_INVALID | `test_B04_*` | **PASS**（registry 合理超前） |
| B-02/B-03 | Runtime L2 / mapping | `-k B-02 or B-03` | **FAIL**（预期 · Step2） |
| 存量 | W1–W3 非 W4 pending | `-m 'not pending'` | **PASS**（50 passed · 9 W4 红测预期） |

```bash
uv run pytest src/tests/integration/test_connector_blueprint_w4.py -k 'B-01 or B-04' -v   # 2 passed
uv run pytest src/tests/contract src/tests/workflow src/tests/integration -m 'not pending' -q
# 50 passed · 9 failed（W4 Step2–4 预期红）· 1 skipped
```

## 3. 代码落位合理性

| 维度 | 检查 | 结论 |
|------|------|------|
| 分层 | registry 在 os_core；无 apps 业务膨胀 | ✅ |
| 写路径 | Step1 无 Legacy 写；load 只读 catalog | ✅ |
| 红线 | R-01 未新增旁路写 | ✅ |
| 注释 | registry.py 文件头 + 函数说明齐全 | ✅ |
| 模块治理 | runtime/ 有 README；catalog 对齐 schema | ✅ |

## 4. 已改动代码测试报告（本 Step）

| 用例ID | AC/接口 | 步骤 | 结果 |
|--------|---------|------|------|
| B-01 | `load_blueprint` | pack_id=conn-mock | **PASS** |

**B-01 出参（内核）**：

```json
{
  "verbs": ["QUERY_ENTITY", "GOVERNED_WRITE"],
  "pack_id": "conn-mock"
}
```

| 用例ID | AC/接口 | 步骤 | 结果 |
|--------|---------|------|------|
| B-04 | `validate_blueprint` | L2 op 无 revert 块 | **PASS** |

**B-04 出参**：

```json
{
  "valid": false,
  "errors": [
    {
      "code": "BLUEPRINT_INVALID",
      "message": "L2 op GOVERNED_WRITE requires revert declaration"
    }
  ]
}
```

## 5. 架构与代码质量评估（本 Step）

| 维度 | 评估 |
|------|------|
| 分层 | registry 与 runtime 分包清晰；`lru_cache` 按 pack 缓存合理 |
| 落位 | catalog 真源在 `integration/catalog`；与 ADR-004 一致 |
| 耦合 | `get_verb_level` 复用 CMV 真源，无重复枚举 |
| 可维护性 | `tenant_id` 占位待 Step2+ override；可接受 |

## 6. 结论

**结论：通过**

- Step 1 目标 AC **B-01 绿**；B-04 校验同步绿；改动面在 plan 内
- W4 Step2–4 用例仍红（9 项）为预期，不阻断本步

**下一步**：**Verify 新会话** `【Verify回合】Step 1` → `./scripts/gate step --step 1 -k 'B-01'`
