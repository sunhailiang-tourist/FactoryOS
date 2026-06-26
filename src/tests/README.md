# tests · 验收与契约测试

## 是什么

**AC-BASE-001**（52 P0）、contract test、集成测试根目录；Gate 0 门禁真源。

## 主要功能

- 对照用例 ID 的 pytest 套件
- OpenAPI / Schema 契约测试
- `integration/` contract tests（Pack、tenant 配置）

## 不负责什么

- 生产代码实现（实现在 `os_core`、`apps`）
- 手工 E2E 脚本（见 `文档/规格说明/运维Runbook.md`）

## 上下游

- **上游**：CI `.github/workflows/ci.yml`
- **下游**：被测模块 `os_core/*`、`server/api`

## 目录规划（W1 起）

```text
tests/
  contract/     # Schema、OpenAPI
  integration/  # AC-BASE-001 按模块
  fixtures/     # mock blueprint、tenant
```

## 相关文档

- AC-BASE-001：`contracts/acceptance/` · [AC-P0-INDEX](../../.cursor/factoryos/AC-P0-INDEX.md)
