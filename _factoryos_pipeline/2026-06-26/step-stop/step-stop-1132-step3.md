# Step 停机：Step 3 — rule_engine + rulesets HTTP

- **plan**：`_factoryos_pipeline/2026-06-26/plan/plan-1121-w3-graph-rule.md`
- **时间**：2026-06-26 11:32（补录 · 对照终轮 `test-1132`）

## 1. Step 标识

Step 3 — `rule_engine` + rulesets HTTP（R-01～R-05 · harness `-k 'R-01'`）

## 2. 改动文件

| 路径 | 变更 |
|------|------|
| `src/server/os_core/rule_engine/__init__.py` | 包入口 |
| `src/server/os_core/rule_engine/store.py` | RuleSet ORM |
| `src/server/os_core/rule_engine/evaluate.py` | deny 优先 · allow 匹配 |
| `src/server/os_core/rule_engine/service.py` | CRUD · freeze · evaluate |
| `src/server/os_core/rule_engine/README.md` | 模块说明 |
| `src/server/api/modules/*/controllers/rulesets.py` | RuleSet HTTP 薄路由 |
| `src/tests/integration/test_rule_w3.py` | R-01～R-05 |

## 3. AC / 接口

| AC ID | 接口 / 行为 | 结果 |
|-------|-------------|------|
| R-01 | 默认 deny → execute 403 `RULE_DENIED` | **PASS** |
| R-02 | allow 规则通过 evaluate | **PASS** |
| R-03 | deny 优先级高于 allow | **PASS** |
| R-04 | graph_version 不匹配 → 422 | **PASS** |
| R-05 | frozen ruleset 不可 PUT | **PASS** |

## 4. 十项自检（Pass/Fail）

| # | 项 | 结果 |
|---|-----|------|
| 1 | 分层/写路径 | Pass — evaluate 纯函数 + service |
| 2 | 响应契约 | Pass — effect allow/deny |
| 3 | 鉴权/租户 | Pass |
| 4 | 红线 | Pass — R-01 默认 deny |
| 5 | Schema | Pass — rules JSON 结构 |
| 6 | 输入校验 | Pass |
| 7 | Shadow | N/A |
| 8 | 幂等/补偿 | N/A |
| 9 | 静态检查 | Pass |
| 10 | 注释 | Pass — rule_engine README |

## 5. Harness 结果

```bash
./scripts/gate step --step 3 -k 'R-01'
```

```text
gate step : PASS
```

## 6. 最短验证路径

```bash
uv run pytest src/tests/integration/test_rule_w3.py -v
```

## 7. Verify（必填）

- 落盘：`verify/verify-1140-step3.md`
- 结论：通过

## 8. 等待

请回复：`可以继续`
