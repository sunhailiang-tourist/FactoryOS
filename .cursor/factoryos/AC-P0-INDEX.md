# AC-BASE-001 · 52 P0 索引（Gate 0）

真源全文（export 镜像）：`contracts/acceptance/验收用例-BASE-001-平台底座.md` · **published** = Contract Registry frozen AC set（ADR-008）  
通过 → tag `core-v1.0.0`

| 段 | ID 范围 | 条数 | 要点 |
|----|---------|------|------|
| Graph | G-01～G-08 | 8 | draft/freeze/409 |
| Rule | R-01～R-05 | 5 | deny/allow/frozen |
| DSL | D-01～D-04 | 4 | registry/whitelist |
| Execution | E-01～E-09 | 9 | 写/revert/idempotency/evidence |
| Connector | C-01～C-04 | 4 | mock health/read/write |
| Reconcile | K-01～K-02 | 2 | ok/drift |
| Blueprint | B-01～B-04 | 4 | load/mapping/revert |
| Package | P-01～P-03 | 3 | export/import/override |
| Trust | T-01～T-03 | 3 | shadow/license/connector |
| MCP | M-01～M-02 | 2 | tools/list · plan not write |
| Scale | S-01～S-04 | 4 | migration/cell/outbox |
| Security | N-01～N-04 | 4 | bypass/checksum/tenant |

**测试命名**：`pytest -k 'G-01'` 或 `def test_G_01()`。

## 其他验收（Gate 0' / D1）

| 文档 | 用途 |
|------|------|
| `验收用例-MVP-001-*` | Path A/B 报工闭环 |
| `验收用例-UX-001-*` | 终端 Harness 双 Gate |
| `验收用例-B-LITE-001-*` | Path C 内置账本 |
