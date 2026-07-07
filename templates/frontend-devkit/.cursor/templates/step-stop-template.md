# step-stop-<HHmm>-stepN.md

## Step N — <名>

| 项 | 内容 |
|----|------|
| 状态 | 待 Test 验收 |
| 改动文件 | |
| AC | W-xx |

## 10 项自检

| # | 项 | Pass/Fail |
|---|-----|-----------|
| 1 | 层界 | |
| 2 | 追踪链 | |
| 3 | i18n | |
| 4 | rbac | |
| 5 | query | |
| 6 | MSW | |
| 7 | 边界无越权 | |
| 8 | 结构无漂移 | |
| 9 | lint/tsc | |
| 10 | 无重复逻辑 | |

## 命令结果

```bash
python scripts/check_boundary_lock.py
python scripts/check_harness.py
pnpm vitest run ...
```

## 风险 / 待确认

- 无 / 须用户 `确认结构变更` / `确认越权`

## 下一步

→ `【WebTest·Step N 验收】` 新会话
