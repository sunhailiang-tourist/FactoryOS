# Test · Gate A–G 与交付纪律

> 正式跑测前须完成 Gate A–G 承诺；Step 0 test-plan **先落盘**。

## Gate A · 全量复盘（只读）

复述覆盖（极简清单即可）：

- 模块：MODULE-MAP 九模块 + 写路径
- 红线：REDLINES R-01–R-11
- 契约：`contracts/openapi` + 本轮 AC ID
- 测试布局：`src/tests/` contract · integration · e2e · ux · harness

## Gate B · 测试目的

必须问你并收到回复：新增 / 缺陷 / 回归 / 验收 / 联调 / 风险评估。

## Gate C · 协作对齐（新增业务强制）

必须已读 Dev plan 路径，输出：

- plan 改动文件/接口/AC 清单
- 必测 / 建议测 / 回归范围
- 触及公共链路 → 标风险等级

## Gate D · 架构质量评估承诺

本轮除功能外，交付「架构与代码质量评估」：通过 / 需改进 / 阻断 + 3–5 条可执行建议。

## Gate E · 最终交付分区承诺

- `## 📦 本次新增接口`
- `## 🔁 本次需求涉及到的接口（字段调整）`
- 全量入参/出参 JSON（多行 `json` 块，禁止 `...`）

## Gate F · 字段调整识别承诺

改动触及 Schema/响应组装 → 自动进入字段调整排查；结论「无调整」须逐文件排除依据。

## Gate G · 命名时间一致性

`test-<HHmm>-<slug>.md`：`<HHmm>`=落盘当下本地时间；mtime 与文件名差 ≤2 分钟。

---

## 执行顺序（Step 0 后）

```text
failing tests（红）
  → 你：可以开始
  → `./scripts/gate step --step N -k '<AC-ID>'`
  → 已改动代码测试报告（优先）
  → 架构评估
  → 扩展回归（次要）
  → 最终总结 + 两类接口分区 + 文件↔接口对账表
```

## 已改动代码测试报告（模板节）

| 用例ID | AC/接口 | 步骤 | 结果 |
|--------|---------|------|------|

每接口：**入参 JSON** + **出参 JSON** + 结构依据（Schema 路径）。

## 架构与代码质量评估

结论：通过 / 需改进 / 阻断。维度：分层 · 注释 · 模块治理 · 耦合 · 红线。

## Bug 报告

用 `templates/bug-template.md`：P0–P3 · AC ID · 复现 · 期望/实际 · 影响面。

## 存量风险门禁

改动影响鉴权/写链路/公共 DTO → 标高/中/低 → 须 `风险接受并继续` 才可继续或给「可合并」。

## 回归触发（自动判断）

| 改动 | 回归 |
|------|------|
| `execution_service` | E-* 全链 + shadow |
| `graph_service` / `rule_engine` | G-* R-* + 未 freeze 409 |
| `agent_orchestrator` | E-08 直写拦截 |
| `connector_sdk` | C-* + mock health |
| `contracts/schemas` | contract tests + OpenAPI ref |
| `integration/packs` | pack contract + Path A/B/C 参数化 |

## FactoryOS 验收盘（替代 curl 烟雾）

Step **停机**用 `./scripts/gate step`（harness + pytest + 静态 + verify 落盘）；**编码中**用 `./scripts/harness --tier auto`。见 [HARNESS-SCRIPTS.md](./HARNESS-SCRIPTS.md)。

```bash
./scripts/gate step --step N -k '<AC-ID>'
```

## 禁止替 Dev 改业务

只报 Bug + 补 `src/tests/**`。评估「阻断」且未 `风险接受并继续` → 不得给可合并结论。
