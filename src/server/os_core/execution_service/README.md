# execution_service · 执行与写门禁

## 是什么

**唯一** 经 Connector **写 Legacy** 的路径：DSL 执行、Saga、Compensator、Shadow、幂等。

## 主要功能

- `execute(session, request)` — W2 Step3：**dry_run → simulated**（E-06）· **idempotency_key 幂等**（E-07）
- `assemble_evidence(session, exec_id)` — W2 Step4：**ExecutionEvidence 聚合**（E-09）
- DSL 解释执行、ExecutionRecord 落库
- Connector 调度（经 `connector_sdk.mock_legacy`）、connector_trace
- Revert / 对账钩子（W4+）

## W3 验收盘

```bash
pytest src/tests/integration/test_graph_w3.py -k 'G-01'
pytest src/tests/integration/test_rule_w3.py -k 'R-01'
pytest src/tests/integration/test_dsl_w3.py -k 'D-01'
./scripts/gate step --step 4 -k 'E-01'
```

## 不负责什么

- Graph freeze 逻辑（`graph_service`）
- Agent 规划（`agent_orchestrator`）

## 上下游

- **上游**：`server/api`、`mcp_gateway`、Harness 确认后的计划
- **下游**：`connector_sdk`、`audit_service`、PostgreSQL

## 相关文档

- ADR-002 R-02、R-05、R-06 · ExecutionRecord v0.2
