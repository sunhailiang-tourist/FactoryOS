# 产品宪法 · UI-First 配置平面（硬性规定）

> **版本** v1.0.0 · **状态**：Accepted · **优先级**：高于 guide/CLI/仓库手工配置叙事  
> **产品核心不变**：Overlay · Graph/Rule · 唯一写路径 · Audit/Revert · Pack 复制。  
> **变的是表现形态**：接入/扩展/tenant/Graph/Rule/开写批准 → **管理平台界面 + 内置 AI**。

---

## 一、两条平面（彻底分离）

| 平面 | 谁 | 主路径 | 沉淀什么 |
|------|-----|--------|----------|
| **配置/实施平面** | 实施顾问 · 客户 IT · 业务负责人 | **Integration Studio（web-admin）** | 界面易用性 · 向导 · 模板 · 复制速度 |
| **平台研发平面** | FactoryOS 平台团队 | SH-步步流 · Contract Registry · `os_core` | 内核 · 红线 · 执行语义 · API |

**硬性规定**：配置/实施平面 **禁止** 以「改仓库 · 记命令 · 读厚文档」作为对外主路径。

---

## 二、五条宪法（不可违背）

### U1 · 对外唯一主路径 = 管理台 UI

接入新客户、扩展系统、映射字段、绑定 Graph/Rule、Shadow 验证、freeze、开写批准、Package import/export —— **均在界面完成**。

### U2 · AI 提案 · 界面确认 · Audit 落库

- AI 可生成：映射草案 · Blueprint 草案 · Graph 草稿  
- **禁止** AI 或脚本静默 freeze / 静默开写 / 静默写 Legacy  
- 人确认 = UI 操作（按钮/签字/表单）→ `audit_service` 可查询事件  

### U3 · 策略与红线在代码里约束，不在实施手册里记忆

R-01～R-11、Rule deny、Shadow 14d、Compensator 等由 **内核 + API 权限** 强制执行。  
实施人员 **不需要** 理解 REDLINES 条文才能安全操作——点不了的按钮就是不允许。

### U4 · CLI / 文档 / 仓库配置仅为内部或逃生舱

| 手段 | 允许用途 | **禁止**用途 |
|------|----------|--------------|
| `./scripts/factoryos guide` | 平台研发调试 · 离线演练 · CI 文档生成 | 灯塔厂 D1 **主实施路径** |
| `docs/` Playbook 长文 | 平台团队设计参考 · ADR | 实施顾问日常操作手册 |
| 手改 `integration/tenants/*.yaml` | 平台导出快照 · 契约测试 fixture | 客户接入日常配置 |
| SH-步步流 / `gate` | **仅平台研发团队** 写内核 | 对外宣称「接入流程」 |

### U5 · 从第一天起可增量交付 Studio

- W1 起 **并行** 交付 Studio 可点击页面（可先 mock API）  
- **禁止**「等 Gate 0 再做界面」作为默认排期  
- 沉淀 KPI：**第二家接入比第一家少几步、少几次误操作**  

---

## 三、真源链（避免 UI 与 CLI 双轨漂移）

```text
人工决策 Playbook（Gate 语义）
        ↕ 同步
src/integration/tools/guide/flows.json   ← export 镜像
src/server/api/data/studio_flows.json        ← Studio 状态机后端模型
        ↕
contracts/openapi export  /v1/integration/*   ← UI 与 AI 共用 API
        ↕
PostgreSQL Registry + audit_service      ← contract/pack/tenant 与人审落库
```

**实施界面只认 API + DB**；仓库 YAML 仅为 export/import 快照，不是编辑真源。

---

## 四、与终端用户界面的关系

| 用户 | 界面 |
|------|------|
| 工人/主管 | `h5-worker`（钉钉/企微）· 0 智多模态 |
| 实施/IT/平台管理员 | **web-admin / Integration Studio** |
| 平台研发 | Cursor + SH-步步流（不对客户可见） |

---

## 五、Studio MVP 节奏（与内核并行）

| 阶段 | 界面能力 | 说明 |
|------|----------|------|
| **v0**（W5+ 并行） | Tenant · Connect · Gate 状态条 | 可演示完整 onboard 故事 |
| **v1**（Gate 0 后） | Map（AI 草案）· Prove · Freeze/开写签字 | Playbook 人审 Gate 上屏 |
| **v2**（D1） | Package import · 第二家复制 | 目标：近零仓库操作 |

---

## 六、厚文档索引（设计细节，非实施主路径）

| 文档 | 路径 |
|------|------|
| Studio 规格 | `docs/文档/规格说明/Integration-Studio规格.md` |
| guide 规格（CLI 过渡） | `docs/文档/规格说明/factoryos-guide规格.md` |
| 人工 Gate | `docs/文档/规格说明/人工决策Playbook.md` |
| 实施链说明 | [INTEGRATION-CHAIN.md](./INTEGRATION-CHAIN.md) |
| 架构 §9 人机协同 | `docs/文档/架构/FactoryOS完整架构设计.md` |

---

## 七、研发纪律（平台团队仍遵守）

写 `src/apps/web-admin` Studio 页面 **仍走 SH-步步流**（plan · test · gate step）。  
本宪法约束的是 **产品对外形态**，不削弱内核研发门禁。
