# rule_engine · 授权引擎

## 是什么

角色、条件、动作 **授权**；默认 deny；所有 L2 写前必经。

## 主要功能

- RuleSet 评估、Pack/DSL 授权检查
- 与 License 联动（未授权 → 403）

## 不负责什么

- 执行 DSL、写 Legacy
- Agent 自动 freeze（R-09）

## 上下游

- **上游**：`execution_service`、`server/api` harness 确认后
- **下游**：只读 RuleSet 存储；结果传给 `execution_service`

## 相关文档

- ADR-002 R-04、R-10
