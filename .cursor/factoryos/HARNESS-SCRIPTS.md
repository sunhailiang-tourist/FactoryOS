# Harness 脚本 · 工作流节点映射

> 脚本说明全文：[scripts/README.md](../../scripts/README.md)

## 统一入口

```bash
./scripts/gate materials --materials …           # 材料已齐
./scripts/gate plan                              # 确认规划（须 materials.ok）
./scripts/gate step --step N -k 'G-01'           # Step 停机（含单步 Test 落盘检查）
./scripts/gate delivery                          # 终轮回归（commit 前）
./scripts/gate harness-eval                      # L4：黄金题回归（改门禁后必跑）
./scripts/gate harness-gc                        # L4：熵清理扫描
./scripts/harness --tier auto                    # 编码中
```

完整激活：[ACTIVATION.md](./ACTIVATION.md) · Eval：[HARNESS-EVAL.md](./HARNESS-EVAL.md) · 税则：[FAILURE-TAXONOMY.md](./FAILURE-TAXONOMY.md)

| tier | 层级 | 检查 |
|------|------|------|
| `contracts` | L0 | openapi refs · cmv sync |
| `boundaries` | L1 | + import boundaries · kernel/router/integration registry · legacy paths |
| `step` / `full` | L2 | + repo-structure · **structure commit gate** · path consistency · redundancy · **python comments** |
| `auto` | 推断 | git diff → 上表最高层；无 diff → `full` |

L3 行为：`gate step` 内含 `--pytest -k '<AC-ID>'` + 单步 Test 落盘 + verify + 静态；step-stop 须 **UI字段对账** + **运行时证据**  
L3 终轮：`gate delivery` = workflow + contract + **integration** 全量 pytest + final-regression 落盘  
L4 外环：`gate harness-eval`（10 题）· `gate harness-gc` · PostToolUse `post-edit-sensor.py`

## 节点规则

| 节点 | 命令 |
|------|------|
| Step 0-B 契约对账后 | `./scripts/harness --tier contracts` |
| plan 落盘（`确认规划`） | `./scripts/gate plan`（`check_plan_spec`：AC/HTTP + **v2 结构** · materials · UI §8） |
| 编码中（按改动面） | `./scripts/harness --tier auto`；编辑业务 .py → **传感器** py_compile/ruff |
| Dev step-stop 后 | step-stop 须含 **UI字段对账** + **运行时证据** → `【Test·Step N 验收】` |
| Verify 后 | `./scripts/gate step --step N -k '<AC-ID>'` |
| 改门禁/规则后 | `./scripts/gate harness-eval` |
| 周更卫生 | `./scripts/gate harness-gc` |
| 全部 Step 完成后 | `【Test·终轮回归】` → `gate delivery` |
| CI / PR | `./scripts/gate pr`（含 deptry）或 `./scripts/gate gate0` |

## Step 内按改动面（auto 等价逻辑）

| 若 git diff 含… | tier |
|-----------------|------|
| `contracts/` | `contracts` |
| `src/server/os_core/` · `src/server/api/` · `src/integration/` | `boundaries` |
| 上述 + 业务 `.py` 大面积改动 | `step` / `full` |

**停机须 `gate step`**（内含 harness full + pytest + Test/Verify 落盘）；**commit 前须 `gate delivery`**。
