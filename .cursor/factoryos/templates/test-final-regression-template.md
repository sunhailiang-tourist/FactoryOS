# 终轮全量回归 · Test 兜底验收报告

- **对照 plan**：`_factoryos_pipeline/<date>/plan/plan-*.md`（全 Step）
- **命名**：`test-<HHmm>-final-regression.md`（HHmm=落盘当下本地时间）
- **口令**：`【Test·终轮回归】`（全部 Step `可以继续` 之后 · commit 之前）

## 1. 本轮 git diff 全量改动面

```bash
git diff --name-only <base>...HEAD
```

| 路径 | 变更 | plan Step | 落位合理 | 备注 |
|------|------|-----------|----------|------|
| | | | | |

## 2. 新增功能正确性（本轮 AC 全量）

| AC ID | Step | 业务验收 | pytest 证据 | 结果 |
|-------|------|----------|-------------|------|
| | | | | |

## 3. 存量功能回归（不影响原功能）

| 域 | 回归范围 | 命令 | 结果 |
|----|----------|------|------|
| workflow | 红线/门禁/健康检查 | `pytest src/tests/workflow/` | |
| contract | OpenAPI/Schema/CMV | `pytest src/tests/contract/` | |
| integration | 本轮触及 + 全量存量 | `pytest src/tests/integration/` | |

```bash
./scripts/gate delivery
```

## 4. 代码落位与优雅性（终轮）

| 维度 | 结论 | 说明 |
|------|------|------|
| 模块边界 | | os_core / apps / integration |
| 重复逻辑 | | ≥2 处相同须抽取 |
| 注释可读性 | | 读码像读业务流程 |
| 与 plan 一致 | | 无超 scope 文件 |

## 5. 接口分区（终轮交付）

### 📦 本次新增接口

### 🔁 本次需求涉及到的接口（字段调整）

（全量入参/出参 JSON · 禁止 `...`）

## 6. 文件 ↔ 接口对账表

| 文件 | 接口/AC | 说明 |
|------|---------|------|
| | | |

## 7. 结论

**结论：通过** | **需改进** | **阻断**

- 阻断 → 禁止 `可以提交` · Dev 回修后重跑终轮
- 需改进 → 列可执行项；须 `风险接受并继续` 才可提交
- 通过 → 允许 `./scripts/gate delivery` 绿后提示 **可以 commit**
