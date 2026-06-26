# 规格说明·factoryos guide 交互引导

> 版本：**v1.1.0** | 日期：2026-06-16  
> 状态：**Accepted**（过渡 · 平台内部）  
> **定位变更（UI-First）**：本 CLI **不是** 对外实施主路径；实施/客户接入走 **Integration Studio**（管理台 UI）。见 [UI-FIRST-CONFIG-PRINCIPLE](../../.cursor/factoryos/UI-FIRST-CONFIG-PRINCIPLE.md)。  
> 用途：平台研发 **调试 flows.json** · CI 文档生成 · 离线演练 · 逃生舱  
> 结构化镜像：`integration/tools/guide/flows.json`（与 [人工决策 Playbook](./人工决策Playbook.md) 同步；Studio 后端模型见 `src/server/api/data/studio_flows.json`）  
> 实现：`scripts/factoryos` · `scripts/factoryos_cli.py`

---

## 1. 设计目标

| 目标 | 实现 |
|------|------|
| 一眼看懂整条链路（调试） | `factoryos guide map <flow>` 树状总览（👤人审 / 🤖自动 / ⚙协作） |
| 平台研发逐步对照 | `factoryos guide` 交互选链路 → 每步：做什么、跑什么命令、改哪些文件、产出什么 |
| flows 与 Playbook 对齐 | Playbook 语义真源 → export 至 `flows.json`（guide 对账） |
| 验证 onboard flow | `factoryos guide onboard` |
| 验证 extend flow | `factoryos guide extend` |
| 与后端解耦 | W1 即可用；`curl` 占位 API 在 Gate 0 后替换为真实调用 |

**不承诺**：替代人审 Gate（freeze、开写批准）；guide **展示**而非绕过治理。  
**禁止**：作为灯塔厂 D1 或实施顾问的 **主实施路径**（须用 Studio）。

---

## 2. 命令一览

```bash
# 仓库根目录
./scripts/factoryos guide                    # 交互：选要做什么
./scripts/factoryos guide list               # 列出全部链路
./scripts/factoryos guide map                # 所有链路总览图
./scripts/factoryos guide map onboard        # 新客户 D1 一图看懂

./scripts/factoryos guide onboard            # 新客户逐步引导
./scripts/factoryos guide onboard -t hasen   # 替换命令中的 {tenant}
./scripts/factoryos guide onboard -y         # 非交互，一次打印全部步骤

./scripts/factoryos guide import -t new-factory    # 第二家 S1
./scripts/factoryos guide extend -t acme -v kingdee  # 新厂商
./scripts/factoryos guide extend-d2          # D2 定制
./scripts/factoryos guide ops                # 运维事件

./scripts/factoryos guide --json onboard     # CI / 文档生成
```

建议 alias（可选）：

```bash
alias factoryos="$PWD/scripts/factoryos"
```

---

## 3. 链路（flow）定义

| flow id | 场景 | 步骤数 |
|---------|------|--------|
| `onboard` | 第一家 D1 全链路 | 13 |
| `import` | 第二家起 S1 import | 6 |
| `extend-vendor`（`extend`） | 新 ERP/MES 厂商 S2/S3 | 9 |
| `extend-d2` | D2 Pack 化扩展 | 6 |
| `ops` | 对账漂移等运维 | 2 |

新增链路：**Playbook 语义真源** → 同步 export `flows.json` + `studio_flows.json`；无需改 `os_core`。

---

## 4. 单步信息结构

每个 Gate 在终端展示：

```text
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
步骤 3/13 · G-CONNECT · 系统连通
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
角色: integrator, customer_it
👤+🤖 · 系统可自动
禁止: Git 中提交明文密钥

【你要做什么】
  1. …

【执行命令】
  $ cp integration/tenants/_template …

【改哪些配置】
  · Studio：租户 system_relations / connect（落 PostgreSQL Registry）
  · export 镜像（可选）：integration/tenants/{tenant}/system_relations/*.yaml

【API（OpenAPI v1.1.1）】
  · POST /v1/integration/connect/test

【产出物】
  ✓ 连通报告
```

---

## 5. 与 Playbook / 配置枢纽关系

```text
人工决策 Playbook.md     ← 人可读详述、治理红线（语义真源）
Studio API + Registry    ← 生产运行时（Gate 状态 · 配置落库 · ADR-008）
flows.json               ← export 镜像 · guide 调试渲染 · CI 对账
studio_flows.json        ← Studio 后端 export 辅助
配置枢纽 system_relations ← export/import 快照；运行时配置落 PostgreSQL Registry
Integration Studio       ← 对外主路径（Web UI + AI）
```

**变更流程**：改 Playbook Gate 语义 → Studio/Registry publish → 同步 export（`flows.json` · `studio_flows.json` · `contracts/`）→ harness 对账。

---

## 6. 演进（W2+）

| 阶段 | 增强 |
|------|------|
| W1 | flows.json + guide 调试可用；Studio v0 并行（mock API） |
| W2 | Studio 接真实 `/v1/integration/*` API |
| W3 | Studio 内 Gate 状态条高亮当前步骤 |
| Gate 0 后 | guide 保留为 CI/调试；**实施主路径仅 Studio** |

---

## 7. 验收

- [ ] 平台研发可用 `factoryos guide map onboard` 对照 flows 与 Playbook（≤30 分钟）
- [ ] `factoryos guide map onboard` 输出含全部人审 Gate 标记
- [ ] `flows.json` 中每个 onboard 步骤在 Playbook §5 有对应条目
- [ ] CI（可选）：`factoryos guide --json onboard | jq .flow.steps | wc` 与 Playbook 一致
- [ ] **实施顾问无需运行 guide 即可完成 onboard 故事**（Studio 或演示环境）

---

## 8. 参考

- [人工决策 Playbook](./人工决策Playbook.md)
- [配置枢纽与关系模型](../架构/配置枢纽与关系模型.md)
- [Integration Studio 规格](./Integration-Studio规格.md)
