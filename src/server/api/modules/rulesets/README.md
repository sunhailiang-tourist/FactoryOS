# rulesets · 规则集 HTTP 域

> **OpenAPI**：`/v1/rulesets/*` · AC **R-01～R-05**  
> **内核**：`os_core/rule_engine`

## 是什么

**RuleSet（规则集）** 的 HTTP 适配：CRUD draft/frozen、**evaluate** 判定某 actor 对 graph+verb 是否 allow/deny。  
Execution 执行前必经 rule evaluate（deny 优先）。

## 核心功能

| 端点 | 业务含义 |
|------|----------|
| `GET /v1/rulesets` | 按 tenant（+ graph）列表 |
| `POST /v1/rulesets` | 创建 draft |
| `GET/PUT /v1/rulesets/{id}` | 读/改 draft（frozen 改 → 409） |
| `POST .../freeze` | 冻结规则集 |
| `POST .../evaluate` | 授权判定（R-01/R-02/R-03） |

## 怎么用

```bash
curl -X POST http://127.0.0.1:8000/v1/rulesets/{id}/evaluate \
  -H 'Content-Type: application/json' \
  -d '{"graph_id":"g1","graph_version":"v1.0.0","verb":"WORK_REPORT","actor":{...}}'
```

Evaluate 请求体定义在 controller 内 `RuleEvaluateBody`；后续可迁至 `schemas/`。

## 承载业务

- **Harness 授权门**：谁能在哪条 graph 上执行哪个 DSL 动词  
- **与 execution**：execute 内核内调 evaluate，HTTP evaluate 供 Studio/调试

## 上下游

- **上游**：Studio 规则编辑 · Harness 确认流 · 集成测试  
- **下游**：`os_core/rule_engine` → `rulesets` 表  
- **契约**：`contracts/schemas/规则集.schema.json`

## 门禁

```bash
uv run pytest src/tests/integration/test_rule_w3.py -q
```

## 关联文档

- [规则引擎规格](../../../docs/文档/规格说明/规则引擎.md)
