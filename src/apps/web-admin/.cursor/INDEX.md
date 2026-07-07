# web-admin AI 工作流 · 独立步步流（可迁出包）

> **版本**：WEB-步步流 v1.0 · 锁死 2.0.0-s5  
> **与 FactoryOS 关系**：**节奏对齐** SH-步步流（人机轨+Spec轨+Harness轨），**规则独立**，不绑定后端 gate/pytest。  
> **迁出**：复制本目录 `rules/` + `factoryos/` + `templates/` → 目标项目 `.cursor/` 即可。

---

## 激活口令

| 角色 | 口令 |
|------|------|
| Dev | `【WebDev模式启动】` |
| Test | `【WebTest模式启动】` · `【WebTest·Step N 验收】` · `【WebTest·终轮回归】` |
| Verify | `【WebVerify回合】Step N`（新对话） |

## 三层控制

| 层 | 作用 |
|----|------|
| **L1 人机轨** | 关键词闸门；每 Step 停机；结构/越权须专用词 |
| **L2 Spec 轨** | `pages/*/contracts` · sector `contracts` · `WEB-ARCHITECTURE-LOCK.yaml` |
| **L3 Harness 轨** | `check_boundary_lock` → `check_harness` → `pnpm check` |

## 关键词（缺一不可）

```text
可以继续 → 确认规划 → 可以开始 →（每 Step）可以继续
```

**专用解锁**（绝对门禁）：

| 词 | 解锁 |
|----|------|
| `确认结构变更` | sector/技术版图/lock/profile 变更 |
| `确认越权` | 写 FactoryOS 后端/全局契约/模板 |
| `风险接受并继续` | 已知风险仍推进 |
| `测试不通过` | 回当前 Step 修复 |

## 落盘（反黑盒 · 项目内独立）

```text
_web_pipeline/<YYYY-MM-DD>/{plan,test,step-stop,verify,summary}/
```

**禁止**用 `_factoryos_pipeline/` 代替（保持迁出独立）。

## 验收盘（web-admin 原生 · 非 FactoryOS gate）

```bash
python scripts/check_boundary_lock.py
python scripts/check_harness.py
pnpm check    # 或 ./scripts/activate.sh 全链
```

## 细则索引

| 文档 | 内容 |
|------|------|
| [WEB-步步流.md](./factoryos/WEB-步步流.md) | 总纲 |
| [WEB-STEP0.md](./factoryos/WEB-STEP0.md) | 开工前理解 |
| [WEB-DEV-GATES.md](./factoryos/WEB-DEV-GATES.md) | Dev Gate 1–4 |
| [WEB-TEST-GATES.md](./factoryos/WEB-TEST-GATES.md) | Test 纪律 |
| [WEB-VERIFY-GATES.md](./factoryos/WEB-VERIFY-GATES.md) | Verify 纪律 |
| [WEB-REDLINES.md](./factoryos/WEB-REDLINES.md) | 红线清单 |

## 绝对门禁（始终生效）

- [WEB-00-独立边界绝对门禁.mdc](./rules/WEB-00-独立边界绝对门禁.mdc)
- [WEB-01-架构版图锁死门禁.mdc](./rules/WEB-01-架构版图锁死门禁.mdc)
