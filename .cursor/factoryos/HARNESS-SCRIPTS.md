# Harness 脚本 · 工作流节点映射

> 脚本说明全文：[scripts/README.md](../../scripts/README.md)

## 统一入口

```bash
./scripts/gate plan                              # 确认规划
./scripts/gate step --step N -k 'G-01'           # Step 停机（含单步 Test 落盘检查）
./scripts/gate delivery                          # 终轮回归（commit 前）
./scripts/harness --tier auto                    # 编码中
```

完整激活：[ACTIVATION.md](./ACTIVATION.md)

| tier | 层级 | 检查 |
|------|------|------|
| `contracts` | L0 | openapi refs · cmv sync |
| `boundaries` | L1 | + import boundaries · kernel/router/integration registry · legacy paths |
| `step` / `full` | L2 | + code redundancy |
| `auto` | 推断 | git diff → 上表最高层；无 diff → `full` |

L3 行为：`gate step` 内含 `--pytest -k '<AC-ID>'` + 单步 Test 落盘 + verify + 静态  
L3 终轮：`gate delivery` = workflow + contract + **integration** 全量 pytest + final-regression 落盘

## 节点规则

| 节点 | 命令 |
|------|------|
| Step 0-B 契约对账后 | `./scripts/harness --tier contracts` |
| plan 落盘（`确认规划`） | `./scripts/gate plan` |
| 编码中（按改动面） | `./scripts/harness --tier auto` |
| Dev step-stop 后 | `【Test·Step N 验收】` → `test-*-stepN-regression.md` |
| Verify 后 | `./scripts/gate step --step N -k '<AC-ID>'` |
| 全部 Step 完成后 | `【Test·终轮回归】` → `gate delivery` |
| CI / PR | `./scripts/gate pr`（含 deptry）或 `./scripts/gate gate0` |

## Step 内按改动面（auto 等价逻辑）

| 若 git diff 含… | tier |
|-----------------|------|
| `contracts/` | `contracts` |
| `src/server/os_core/` · `src/server/api/` · `src/integration/` | `boundaries` |
| 上述 + 业务 `.py` 大面积改动 | `step` / `full` |

**停机须 `gate step`**（内含 harness full + pytest + Test/Verify 落盘）；**commit 前须 `gate delivery`**。
