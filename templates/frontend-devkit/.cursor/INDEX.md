# web-admin AI 工作流 · 独立步步流（可迁出包）

> **版本**：WEB-步步流 v1.1 · L4 外环 · 锁死见 `contracts/WEB-ARCHITECTURE-LOCK.yaml`  
> **与 FactoryOS**：**节奏对齐**，**规则与 stamp 独立**（`web_gate` ≠ `gate`）。  
> **迁出**：复制 `.cursor/` + `scripts/web_*` + `_web_pipeline/` 骨架 → 目标项目即可。

## 激活口令

| 角色 | 口令 |
|------|------|
| Dev | `【WebDev模式启动】` |
| Test | `【WebTest模式启动】` · `【WebTest·Step N 验收】` · `【WebTest·终轮回归】` |
| Verify | `【WebVerify回合】Step N` |

## 三层 + L4

| 层 | 作用 |
|----|------|
| L1 | 关键词；材料已齐 / 确认规划 / 可以开始 |
| L2 | pages contracts · WEB-ARCHITECTURE-LOCK |
| L3 | boundary · harness · pnpm check · **web_gate step** |
| L4 | `web_gate harness-eval` · 税则 WFT-* · 传感器 · GC |

## 关键词

```text
材料已齐 → 可以继续 → 确认规划 → 可以开始 →（每 Step）可以继续
```

## 落盘

```text
_web_pipeline/<YYYY-MM-DD>/{plan,test,step-stop,verify,summary}/
_web_pipeline/.gates/{materials,plan,test,code}.ok
```

## 验收盘

```bash
./scripts/web_gate materials|plan|test|start|step
./scripts/web_gate harness-eval
python scripts/check_boundary_lock.py
python scripts/check_harness.py
./scripts/activate.sh
```

## 细则

| 文档 | 内容 |
|------|------|
| [WEB-步步流.md](./factoryos/WEB-步步流.md) | 总纲 |
| [WEB-GATES.md](./factoryos/WEB-GATES.md) | stamp + 关键词 |
| [WEB-STEP0.md](./factoryos/WEB-STEP0.md) | 材料 + Step0 |
| [WEB-DEV-GATES.md](./factoryos/WEB-DEV-GATES.md) | Dev |
| [WEB-TEST-GATES.md](./factoryos/WEB-TEST-GATES.md) | Test |
| [WEB-VERIFY-GATES.md](./factoryos/WEB-VERIFY-GATES.md) | Verify |
| [WEB-HARNESS-EVAL.md](./factoryos/WEB-HARNESS-EVAL.md) | WHE 黄金题 |
| [WEB-FAILURE-TAXONOMY.md](./factoryos/WEB-FAILURE-TAXONOMY.md) | WFT 税则 |
| [WEB-REDLINES.md](./factoryos/WEB-REDLINES.md) | 红线 |

## 绝对门禁

- [WEB-00](./rules/WEB-00-独立边界绝对门禁.mdc) · [WEB-01](./rules/WEB-01-架构版图锁死门禁.mdc)
