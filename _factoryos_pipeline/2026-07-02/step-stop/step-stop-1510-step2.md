# Step 停机：Step 2 — Gate 0 交付仪式

- **plan**：`_factoryos_pipeline/2026-07-02/plan/plan-1000-w8-gate0-m03-trace.md`
- **时间**：2026-07-02

## 1. Step 标识

Step 2 — Gate 0 收口 · change-summary · 终轮回归 · tag 指引

## 2. 交付物

| 路径 | 说明 |
|------|------|
| `summary/change-summary-1500-w8-gate0-m03-trace.md` | PR 变更摘要 |
| `test/test-1505-final-regression.md` | 终轮 108 passed |
| Step 1 代码 | M-03 已绿 · `gate step --step 1` OK |

## 3. Harness

```bash
./scripts/gate delivery
./scripts/gate pr
```

## 4. 最短验证

```bash
uv run pytest src/tests/ -q   # 108 passed
```

## 5. 人工 tag

```bash
git tag -a core-v1.0.0 -m "FactoryOS Core 1.0 — AC-BASE-001 Gate 0"
```

## 6. 等待

用户 **`可以提交`** 后 commit / PR / tag
