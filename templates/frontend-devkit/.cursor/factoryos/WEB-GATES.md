# WEB-GATES（L1 关键词 + L4 stamp）

> **独立于** 仓库根 `./scripts/gate` / `_factoryos_pipeline`。  
> stamp 仅 `./scripts/web_gate` 可写 → `_web_pipeline/.gates/*.ok`

## 关键词

| 关键词 | 阶段 | 允许行为 |
|--------|------|----------|
| `材料已齐` | 材料准入 | **`./scripts/web_gate materials`** → materials.ok |
| `可以继续` | Step0 / Step 验收 | 进入规划或下一 Step |
| `确认规划` | 规划关 | plan 落盘 + **`./scripts/web_gate plan`（plan.ok）** · 须 materials.ok |
| `可以开始` | 编码关 | **`./scripts/web_gate start --step N`（code.ok）** |
| `确认结构变更` | 架构锁 | sector/技术版图 |
| `确认越权` | 边界 | 跨 FactoryOS 写 |
| `测试不通过` | 失败 | 回当前 Step |
| `可以提交` | 终轮 | activate / check 全绿后 |

## 四重 stamp（垂直不可跳）

```text
材料已齐 → web_gate materials → materials.ok
  → 确认规划 → web_gate plan → plan.ok
  → web_gate test → test.ok
  → 可以开始 → web_gate start → code.ok
  → Test → Verify → web_gate step → 作废 code.ok
```

## L4 外环

```bash
./scripts/web_gate harness-eval   # WHE-01～10
./scripts/web_gate harness-gc
```

税则：[WEB-FAILURE-TAXONOMY.md](./WEB-FAILURE-TAXONOMY.md) · Eval：[WEB-HARNESS-EVAL.md](./WEB-HARNESS-EVAL.md)
