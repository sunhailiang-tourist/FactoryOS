# ADR-002 执行红线（违反即拒绝）

优先级：`可靠性 > 安全性 > 可追溯 > 可回滚 > AI 能力`

| ID | 红线 |
|----|------|
| R-01 | Agent / orchestrator **禁止** Connector.write 或直接写 DB |
| R-02 | 所有 Legacy **写** 仅经 `execution_service` |
| R-03 | Graph `status !== frozen` → **禁止** L2 写 |
| R-04 | Rule Engine **不可绕过**；默认 deny |
| R-05 | 每个 L2 DSL **必须** 有 Compensator |
| R-06 | 每次写 → ExecutionRecord + Audit |
| R-07 | Shadow/dry_run 先于生产写 |
| R-08 | **禁止** 原地改 frozen Graph / RuleSet |
| R-09 | **禁止** Agent 自动 freeze Graph |
| R-10 | 未授权 Pack/DSL/Connector → 403 + Audit |
| R-11 | 多模态 **不得** 跳过 Harness 确认 + Rule |

## 写路径（唯一）

```text
perception/agent → DslPlan → harness/confirm → rule → execution → connector_sdk.write → audit
```

## 负向测试（AC 必覆盖）

- E-08 Agent 直写拦截
- G-03 未 freeze → 409
- R-01 无 Rule → 403
- T-01 shadow 不写 Legacy
