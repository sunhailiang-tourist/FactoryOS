# 预开发说明：W3 — graph freeze · rule evaluate

- **日期**：2026-06-26
- **对照契约**：`contracts/openapi/工厂操作系统-v1.1.yaml` · `contracts/acceptance/验收用例-BASE-001-平台底座.md`
- **架构入口**：`docs/文档/架构/FactoryOS完整架构设计.md` §16 W3 行
- **依赖 W2**：audit · execution · evidence · E-03/06/07/09 ✅

---

## 1. 迭代目标

**一句话**：Graph 生命周期 + Rule 授权 + DSL 门禁接入 execute 唯一写路径。

**可测要点**：G-01～G-08 · R-01～R-05 · D-01～D-03 · E-01 · W2 回归不破坏。

**不在 W3**：E-02/E-04 Revert · D-04（OpenAPI 无 POST registry）· 52 P0 全绿

---

## 2. AC 对账表

| AC ID | 本迭代 | Step |
|-------|--------|------|
| G-01～G-08 | 是 | 1–2 |
| R-01～R-05 | 是 | 3 |
| D-01～D-03 | 是 | 4 |
| E-01 | 是 | 4 |
| D-04 | 否 | OpenAPI 仅 GET registry |
| E-02～E-04 | 否 | W4+ |

---

## 3. 分步计划

| Step | 内容 | Harness |
|------|------|---------|
| 1 | Alembic 003 + graph_service 内核 CRUD | `-k 'G-01'` |
| 2 | Graph 生命周期 HTTP + G-03/06/08 | `-k 'G-05'` |
| 3 | rule_engine + rulesets HTTP | `-k 'R-01'` |
| 4 | DSL registry + execution 门禁 + E-01 | `-k 'E-01'` |

---

## 4. Harness 验收盘

```bash
./scripts/gate step --step 1 -k 'G-01'
./scripts/gate step --step 2 -k 'G-05'
./scripts/gate step --step 3 -k 'R-01'
./scripts/gate step --step 4 -k 'E-01'
./scripts/gate delivery
./scripts/gate pr
```
