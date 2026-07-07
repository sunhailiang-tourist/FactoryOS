# WEB · Test 纪律

> Test Agent **只写测试**；禁止改 `pages/**` 业务实现（除 `*.test.tsx` 同目录测试）。

## 激活

- `【WebTest模式启动】` — 与 plan 对齐，写 failing tests
- `【WebTest·Step N 验收】` — Step N 回归报告
- `【WebTest·终轮回归】` — 全量终轮

## 可写路径

| 允许 | 禁止 |
|------|------|
| `src/**/*.test.ts(x)` | `pages/**/*.lazy.tsx` 业务逻辑 |
| `e2e/**` | `router/**` `store/**` registry |
| `*.stories.tsx` | `os_core` / FactoryOS 任何路径 |
| `_web_pipeline/**/test/**` | 改 `check_harness.py` 规则（须结构确认） |

## 每 Step 验收落盘

`test/test-<HHmm>-stepN-regression.md`

必填：对应用例 AC · 命令 · 预期 · 实际 · 红/绿

## 命令真源

```bash
pnpm vitest run <pattern>
pnpm e2e
python scripts/check_boundary_lock.py
python scripts/check_harness.py
```

## 测试不通过

用户发 `测试不通过` → Dev 回当前 Step；**禁止**开 Step N+1。

## 禁止

偷改业务 · 用 pytest · 用 FactoryOS `src/tests/**` · 未红先宣称绿
