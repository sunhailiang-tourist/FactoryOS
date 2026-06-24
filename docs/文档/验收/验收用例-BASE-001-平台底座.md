# 验收用例 BASE-001：平台底座验收

| 版本 | v0.2.0 |
|------|--------|
| 范围 | **平台内核 + GIP Core 1.0**（ADR-004）；不验收具体报工/MES 业务 |
| 通过标准 | Core 1.0 Gate：下列 P0 用例全部通过（含 GIP 扩展） |

**说明**：垂直场景验收（工人报工、Legacy 对账等）在工厂 Graph frozen 后执行 [AC-MVP-001](./验收用例-MVP-001-报工垂直闭环.md)。  
**终端 0 智与多模态体验**见 [UX-001](./验收用例-UX-001-终端体验与多模态.md)；D1 须与 BASE-001 **双 Gate** 同过。

---

## 一、Graph 与 Freeze（P0）

| ID | 用例 | 步骤 | 期望 |
|----|------|------|------|
| G-01 | 创建 draft Graph | POST /v1/graphs | status=draft |
| G-02 | draft 可编辑 | PUT /v1/graphs/{id}/versions/{version} | 200 |
| G-03 | 未 freeze 拒绝 L2 写 | execute GOVERNED_WRITE on draft graph | 409 GRAPH_NOT_FROZEN |
| G-04 | submit 到 in_review | POST .../versions/{version}/submit | status=in_review |
| G-05 | freeze 成功 | POST freeze + 已 frozen RuleSet | status=frozen, checksum 有效 |
| G-06 | frozen 不可改 | PUT nodes on frozen | 409 |
| G-07 | clone 新版本 | POST clone | 新 version draft |
| G-08 | deprecated 拒绝 L2 写 | execute on deprecated | 409 |

---

## 二、Rule Engine（P0）

| ID | 用例 | 步骤 | 期望 |
|----|------|------|------|
| R-01 | 默认 deny | 无匹配 rule | 403 RULE_DENIED |
| R-02 | allow 规则通过 | role 匹配 + action 匹配 | 进入 execution |
| R-03 | deny 优先 | 同时有 allow/deny，deny 优先级高 | 403 |
| R-04 | RuleSet 绑定 graph_version | graph 升级后旧 ruleset | 422 或拒绝 |
| R-05 | frozen RuleSet 不可改 | PUT frozen ruleset | 409 |

---

## 三、DSL Registry（P0）

| ID | 用例 | 步骤 | 期望 |
|----|------|------|------|
| D-01 | 列出底座动词 | GET registry | 含 QUERY_ENTITY, GOVERNED_WRITE |
| D-02 | 未注册动词 | execute UNKNOWN_VERB | 400 DSL_UNKNOWN |
| D-03 | Graph 白名单外 | verb 已注册但不在 graph.allowed_dsl | 403 DSL_NOT_IN_GRAPH |
| D-04 | L2 无 compensator 拒绝注册 | POST registry L2 无 compensator | 422 |

---

## 四、Execution 与 Revert（P0）

| ID | 用例 | 步骤 | 期望 |
|----|------|------|------|
| E-01 | L0 只读成功 | QUERY_ENTITY on frozen graph | 200, 无 ExecutionRecord 写 Legacy |
| E-02 | L2 写成功 | GOVERNED_WRITE mock | success + before/after snapshot |
| E-03 | Audit 产生 | E-02 后查 audit | 有 append-only 记录 |
| E-04 | Revert 成功 | revert E-02 | 原记录 reverted, Legacy 恢复 |
| E-05 | 重复 revert 失败 | revert 已 reverted | 409 |
| E-06 | dry_run 不写 | dry_run=true | Legacy 不变, 返回模拟结果 |
| E-07 | idempotency | 相同 key 重试 | 不重复写 Legacy |
| E-08 | Agent 不可直写 | orchestrator 直接调 connector.write | 编译/测试拦截 |
| E-09 | Evidence 可重建 | E-02 成功后 GET `/v1/executions/{execId}/evidence` | 200；body 通过 `ExecutionEvidence.schema.json`；含 execution + audit_events + rule_snapshot |

---

## 五、Connector Mock（P0）

| ID | 用例 | 步骤 | 期望 |
|----|------|------|------|
| C-01 | healthCheck | GET connector health | ok |
| C-02 | read entity | entity.get | 返回 snapshot |
| C-03 | write entity | entity.update | legacy_refs  populated |
| C-04 | revert read-back | write 后 read | 与 after_snapshot 一致 |

---

## 六、Harness 最小环（P1，Phase 1 后半）

| ID | 用例 | 步骤 | 期望 |
|----|------|------|------|
| H-01 | 感知→计划 | 输入意图 → orchestrator | 输出 DSL 计划，不执行 |
| H-02 | 确认门 | 计划 → 待确认 → 确认后 execute | 未确认不执行 |
| H-03 | 验证记录 | execute 后 harness 记录 | 全链路可追踪 |

---

## 七、对账 Job（P0，Core 1.0 · ADR-004）

| ID | 用例 | 步骤 | 期望 |
|----|------|------|------|
| K-01 | 无 drift | reconciliation run | status=ok |
| K-02 | 模拟 drift | 篡改 mock 数据后 run | drift_detected + 明细 |

---

## 八、Blueprint Runtime（P0，GIP · ADR-004）

| ID | 用例 | 步骤 | 期望 |
|----|------|------|------|
| B-01 | 加载 mock blueprint | Registry load `conn-mock` blueprint | 200, ops 列表含 WORK_REPORT |
| B-02 | Runtime 执行 L2 op | execute via blueprint WORK_REPORT | legacy_refs populated |
| B-03 | mapping 错误 | 缺必填 mapping 字段 | MAPPING_ERROR |
| B-04 | revert/reconcile 声明 | L2 op 无 revert 声明 | 422 BLUEPRINT_INVALID |

---

## 九、Package import/export（P0，GIP · ADR-004）

| ID | 用例 | 步骤 | 期望 |
|----|------|------|------|
| P-01 | export Package | export tenant A | JSON 含 graphs/rulesets/connector_configs |
| P-02 | import 到 tenant B | import Package | tenant B 可 resolve Pack |
| P-03 | Override 差量 | tenant B overrides.yaml 改 base_url | Runtime 用新 URL |

---

## 十、GIP Trust（P0，ADR-004）

| ID | 用例 | 步骤 | 期望 |
|----|------|------|------|
| T-01 | shadow_mode | tenant.shadow_mode=true, L2 write | Legacy 不变, ExecutionRecord 有 simulated |
| T-02 | 未授权 Pack | execute 未 license pack | 403 + audit |
| T-03 | Connector 未配置 | 未注册 pack_id | 403 CONNECTOR_NOT_CONFIGURED |

---

## 十一、MCP Gateway 内部（P0，Core 1.0 · ADR-004）

| ID | 用例 | 步骤 | 期望 |
|----|------|------|------|
| M-01 | tools/list | GET MCP tools | 仅已授权 CMV |
| M-02 | tools/call 不直写 | call WORK_REPORT tool | 返回 DSL Plan JSON；Legacy 未变直至 execution 确认 |
| M-03 | SEP-414 `_meta` | call 带 `params._meta.traceparent` | audit/plan span 可关联同一 trace_id |

> **M-03 为 P1**：Y1 MCP stub 须保留 `_meta` 解析钩子；Y1 末 internal GA 前升 P0。

---

## 十二、规模预埋（P0，ADR-007 · Gate 0 migration）

| ID | 用例 | 步骤 | 期望 |
|----|------|------|------|
| S-01 | 规模表 migration | 跑 Alembic upgrade head | 存在 `tenants.cell_id/placement_tier/region`；空表 `connector_instances` · `tenant_quotas` · `outbox_events` |
| S-02 | tenant 默认值 | 创建或 seed 默认 tenant | `cell_id=cell-default`, `placement_tier=pool` |
| S-03 | TenantRegistry | `get_cell(default_tenant)` | 返回 `cell-default`（S0 单 Cell no-op 路由） |
| S-04 | FactoryOS Queue 接口 | 注册 in-process 实现；写入 outbox 行 | outbox 可持久化；S0 不依赖 Redis；S1 换 Redis Streams 实现不改调用方 |

---

## 十三、负向与安全（P0）

| ID | 用例 | 期望 |
|----|------|------|
| N-01 | 绕过 `rule_engine` 调 execution 内部写 | 不可达 / 403 |
| N-02 | 篡改 frozen graph checksum | freeze 校验失败 |
| N-03 | 跨 tenant 读 execution | 403 |
| N-04 | SQL injection in params | 校验拒绝 / 无害化 |

---

## 十四、Gate 判定

**Core 1.0 冻结（tag `core-v1.0.0`）**：

```text
P0：G-01~G-08, R-01~R-05, D-01~D-04, E-01~E-09, C-01~C-04,
    K-01~K-02, B-01~B-04, P-01~P-03, T-01~T-03, M-01~M-02,
    S-01~S-04, N-01~N-04 全部 PASS
```

**Phase 1 完成（Gate 1 技术前提）**：

```text
Core 1.0 P0 全部 PASS + H-01~H-03 + M-03（P1 钩子）
→ 可开始工厂 D1 实施（需另 frozen 业务 Graph + 真实 Connector Pack）
```

---

## 十五、测试实现建议

```text
tests/
  contract/     # Schema 校验
  integration/  # API + PostgreSQL + mock connector
  e2e/          # 全链路 G→R→D→E
```

每个用例 ID 对应一个 `describe('G-01')` 或 `it('G-01')` 便于追溯。
