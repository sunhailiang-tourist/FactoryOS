# Harness 脚本 · 工作流节点映射

> 脚本说明全文：[scripts/README.md](../../scripts/README.md)

## 统一入口

```bash
./scripts/gate plan              # 确认规划
./scripts/gate step --step N -k 'G-01'    # Step 停机
./scripts/harness --tier auto    # 编码中
```

完整激活：[ACTIVATION.md](./ACTIVATION.md)

| tier | 层级 | 检查 |
|------|------|------|
| `contracts` | L0 | openapi refs · cmv sync |
| `boundaries` | L1 | + import boundaries |
| `step` / `full` | L2 | + code redundancy |
| `auto` | 推断 | git diff → 上表最高层；无 diff → `full` |

L3 行为：`gate step` 内含 `--pytest -k '<AC-ID>'` + 静态 + verify 落盘检查

## 节点规则

| 节点 | 命令 |
|------|------|
| Step 0-B 契约对账后 | `./scripts/harness --tier contracts` |
| plan 落盘（`确认规划`） | `./scripts/gate plan` |
| 编码中（按改动面） | `./scripts/harness --tier auto` |
| Step N **停机** | `./scripts/gate step --step N -k '<AC-ID>'` |
| Test 跑测验收 | `./scripts/gate step --step N -k '<AC-ID>'` |
| CI / Gate 0 | `./scripts/gate pr` 或 `./scripts/gate gate0` |

## Step 内按改动面（auto 等价逻辑）

| 若 git diff 含… | tier |
|-----------------|------|
| `contracts/` | `contracts` |
| `src/os_core/` · `src/integration/` | `boundaries` |
| `src/os_core/` · `src/apps/` 业务 `.py` | `step` |

**停机须 `gate step`**（内含 harness full + pytest + verify）；编码中可用 `harness --tier auto`。
