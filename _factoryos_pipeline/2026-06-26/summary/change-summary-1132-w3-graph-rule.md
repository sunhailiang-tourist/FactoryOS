# PR 变更摘要：W3 — graph freeze · rule evaluate · DSL 门禁

- **plan**：`_factoryos_pipeline/2026-06-26/plan/plan-1121-w3-graph-rule.md`
- **日期**：2026-06-26

## 标题建议

`feat(w3): graph lifecycle · rule engine · DSL registry · execution gates`

## 主要改动

| 模块 | 说明 |
|------|------|
| `003_graphs_rulesets` migration | graphs · rulesets 表 |
| `graph_service` | G-01～G-08 生命周期 |
| `rule_engine` | R-01～R-05 默认 deny/allow |
| `cmv_registry` + DSL routes | D-01～D-03 |
| `execution_service` | G-03/R-01/E-01 门禁 |
| integration 测试 | 17 项 W3 + W2 回归 |

## AC

G-01～G-08 · R-01～R-05 · D-01～D-03 · E-01 **PASS**；52 P0 其余 **30 pending**。

## 测试

`pytest … -m 'not pending'` → **42 passed** · `gate pr` OK

Test 终轮：`test-1132-w3-final-regression.md`
