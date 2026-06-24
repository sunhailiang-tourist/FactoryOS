# 规格说明·Connector Blueprint

| 版本 | v1.0.0 |
|------|--------|
| 范围 | Platform-L1 GIP：声明式 Connector 契约 |
| 决策 | ADR-004 Accepted |
| 实现 | `os_core/connector_sdk/runtime/` |

## 1. 职责

- **80%** 厂商 ERP/MES/OA 接入通过本 YAML 描述，由 Runtime 解释执行  
- 绑定 **Canonical Manufacturing Verbs（CMV）**，不发明 vendor 私有 DSL 动词  
- 与 Python `Connector` 类 **并存**：复杂协议走 S3 Custom Pack，须伴生 `blueprint.meta.yaml`  

## 2. 文件布局

> **运行时真源**：`integration/catalog/`（与 `16` §2、`integration/README.md` 一致）。  
> **文档侧认证样例**：`文档/连接器/catalog/`（Silver 分级参考，非 Runtime 默认加载路径）。

```text
integration/
  catalog/
    conn-erp-kingdee-write/
      blueprint.yaml
      mapping.yaml          # 可选，复杂映射外置
      tests/
        contract_work_report.json
  packs/
    conn-erp-hasen/
      pack.json
      blueprint.yaml        # 或引用 catalog/ 相对路径
```

## 3. Schema（v1）

```yaml
apiVersion: factoryos.io/v1
kind: ConnectorBlueprint
metadata:
  pack_id: conn-erp-example-write    # 与 Pack ID 一致
  system: erp                         # LegacySystem enum
  vendor: example
  level: L2                           # L0 | L2 | L3
  certification: bronze               # bronze | silver | gold
spec:
  auth:
    type: oauth2_client_credentials   # api_key | custom_sign | none
    secrets_ref: tenant/example/oauth # 不进 Graph/ExecutionRecord
  base_url: "${tenant.config.erp_base_url}"
  ops:
    - verb: WORK_REPORT               # CMV，须在 DSL Registry 已注册
      method: POST
      path: /api/workreport/create
      idempotency_header: X-Idempotency-Key
      mapping:
        work_order_id: $.payload.order_no
        qty: $.payload.completed_qty
      response:
        legacy_id: $.data.bill_id
      revert:
        verb: WORK_REPORT_REVERT
        method: POST
        path: /api/workreport/cancel
      reconcile:
        read_verb: QUERY_REPORT_HISTORY
        match_key: legacy_id
  resilience:
    timeout_ms: 8000
    retry:
      max: 3
      backoff: exponential
      retry_on: [408, 429, 502, 503, 504]
    circuit_breaker:
      failure_threshold: 5
      reset_ms: 60000
```

## 4. 字段规则

| 字段 | 规则 |
|------|------|
| `metadata.pack_id` | 须与 [模块包](../规格说明/模块包.md) 登记一致 |
| `metadata.system` | 仅 `LegacySystem` 10 类 enum |
| `spec.ops[].verb` | 须已在 DSL Registry；L2 须声明 `revert` |
| `mapping` | JSONPath 或外置 `mapping.yaml` |
| `secrets_ref` | 仅引用；明文禁止入库 |
| `resilience` | Runtime 强制默认；可 per-op 覆盖 |

## 5. Runtime 行为

1. Registry 按 `tenant_id` + `pack_id` 加载 blueprint  
2. Override merge：`integration/tenants/{id}/overrides.yaml` 覆盖 `base_url`、mapping 差量  
3. `execution_service` 调用 `runtime.execute(op, payload)` — **唯一写出口不变**  
4. 每次调用写 span：`tenant, pack_id, verb, latency_ms, outcome` → ExecutionRecord trace  
5. 错误映射：`CONNECTOR_TIMEOUT` / `LEGACY_4XX` / `MAPPING_ERROR` / `CIRCUIT_OPEN`  

## 6. Contract Test

每个 `op` 须有 `integration/.../tests/contract_{verb}.json`：

```json
{
  "verb": "WORK_REPORT",
  "input": { "order_no": "WO-001", "completed_qty": 10 },
  "expected_response": { "legacy_id": "string" },
  "reconcile_match": true
}
```

CI：`integration/packs/*/tests/` 变更触发 Pack 级测试，不跑全量 Core。

## 7. 与 Python Connector 关系

| 场景 | 方式 |
|------|------|
| 标准 REST | 仅 blueprint.yaml |
| 复杂签名/二进制 | Python 类 + `blueprint.meta.yaml`（文档化 ops） |
| 注册 | `ConnectorRegistry.register(pack_id, BlueprintRuntime \| PythonConnector)` |

## 8. 验收

见 [AC-BASE-001](../验收/验收用例-BASE-001-平台底座.md) § Blueprint（B-01～B-04）。

## 9. 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0.0 | 2026-06-16 | 初版；ADR-004 |
