# PR 变更摘要：W7 — Gate 0（Shadow · Package · MCP · DSL · 负向安全）

- **plan**：`_factoryos_pipeline/2026-07-01/plan/plan-0900-w7-gate0-gip-mcp.md`
- **日期**：2026-07-01
- **分支**：`dev_sunhailiang_core_260624`（W6 已 commit · 同分支续开）

## 标题建议（PR title）

`feat(w7): Gate 0 — shadow · package · MCP · DSL D-04 · N-* security`

## 变更背景（Why）

W6 已具备 license/reconciliation stub；W7 补齐 AC-BASE-001 **剩余 14 项 P0**（T-01/T-03 · P-01～P-03 · M-01/M-02 · D-04/E-08 · N-01～N-04），达成 **Gate 0 / core-v1.0.0** 技术前提。

## 主要改动（What）

| 模块 | 路径 | 说明 |
|------|------|------|
| tenant_service | `os_core/tenant_service/` | shadow_mode 真源 · GET/PUT settings（T-01） |
| license_service | 升级 | tenant_pack_entitlements · CONNECTOR_NOT_CONFIGURED（T-03） |
| package_service | `os_core/package_service/` | export/import 快照（P-01～P-03） |
| mcp_gateway | `os_core/mcp_gateway/` | JSON-RPC tools/list · tools/call（M-01/M-02） |
| cmv_registry | `register_dsl_verb` | L2 无 compensator → 422（D-04） |
| param_safety | `shared_contracts/param_safety.py` | SQL injection 模式拒绝（N-04） |
| execution_service | tenant 隔离 GET | 跨 tenant 读 execution → 403（N-03） |
| API 域 | tenant · package · integration · mcp · registry | 薄路由 |
| 结构 | 内核 **13** 模块 · import_boundaries | PATH-SNAPSHOT 同步 |
| 工作流 | stamp 门禁 plan/test/code.ok | Hook + gate_cli |
| 测试 | `test_*_w7.py` × 6 | Step1–7 + 终轮 |

## AC 通过情况

| AC ID | Step | 结果 |
|-------|------|------|
| T-01 | 1 | **PASS** shadow_mode simulated |
| T-03 | 2 | **PASS** CONNECTOR_NOT_CONFIGURED |
| P-01～P-03 | 3–4 | **PASS** export/import/override |
| M-01/M-02 | 5 | **PASS** MCP tools → DslPlan |
| D-04/E-08 | 6 | **PASS** CMV 422 · Agent 红线 |
| N-01～N-04 | 7 | **PASS** 负向安全 |

W1–W6 存量：终轮 `test-1140-final-regression.md` **107 passed**。

## 业务口径确认

- **Shadow**：tenant.shadow_mode → L2 effective_shadow，不写 Legacy（与 dry_run 合并）。
- **Package**：Graph/Rule/Connector 快照 export/import；connector_overrides 运行时生效。
- **MCP**：内部 stub；tools/call → orchestrator DslPlan；Y2 OAuth 扩展点保留。
- **安全**：无 internal execute 旁路；params SQL 模式拒绝；execution 读 tenant 隔离。

## 测试结论

```bash
./scripts/gate step --step 1 -k 'T-01' … --step 7 -k 'N-01'   # 全绿
./scripts/gate delivery                                          # 终轮
./scripts/gate pr
```

## Summary（3 条，可贴 PR）

1. 新增 tenant/package/mcp 三内核 + HTTP 域：Shadow 开关、Implementation Package 交付、MCP tools/list|call 内部 GA（T-01 · P-* · M-*）。
2. DSL D-04 CMV 注册校验 + execution param/tenant 安全门禁（D-04 · N-03/N-04）；内核扩至 13 模块。
3. W7 七步 gate + 终轮 107 pytest 绿；Gate 0 pending AC 清零，可 tag `core-v1.0.0`（人工）。
