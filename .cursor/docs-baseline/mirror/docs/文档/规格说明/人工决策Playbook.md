# 规格说明·人工决策 Playbook

> 版本：**v1.0.0** | 日期：2026-06-16  
> 状态：**Accepted**  
> 用途：扩展与新客户接入中 **必须人工** 的节点——统一 **触发条件 · 角色 · 步骤 · 产出物 · 下一步**  
> 原则：**机器跑自动化，人只出现在红线；人来了不用翻 ADR，只跟本 Playbook**  
> 关联：[04-工厂实施手册](../../准备/2026-06-16/04-工厂实施手册.md) · [Integration-Studio规格](./Integration-Studio规格.md) · [Shadow-Mode与对账规格](./Shadow-Mode与对账规格.md) · [运维Runbook](./运维Runbook.md) · [Evolution-Layer-宪章](../架构/Evolution-Layer-宪章.md) · [配置枢纽与关系模型](../架构/配置枢纽与关系模型.md)

---

## 1. 如何使用

```text
1. 看「当前阶段」列 → 找到 Gate ID
2. 核对「触发条件」是否满足
3. 由「责任角色」按「行为路径」执行（**Studio 为主** / CLI 调试 / 书面）
4. 收集「产出物」存档
5. 进入「下一 Gate」
```

**主路径**：**Integration Studio**（管理台 UI）— 见 [UI-FIRST-CONFIG-PRINCIPLE](../../.cursor/factoryos/UI-FIRST-CONFIG-PRINCIPLE.md) · [Integration-Studio规格](./Integration-Studio规格.md)

**CLI 调试**：`./scripts/factoryos guide` 为 **flows.json 终端渲染器**（平台研发/CI 用，**非实施主路径**）；见 [factoryos-guide规格](./factoryos-guide规格.md)。

**自动化边界**：标 ❌ 的 Gate **禁止** 脚本跳过；标 ⚠️ 的可半自动但须签字。

---

## 2. 角色定义

| 角色 | 代码 | 典型岗位 |
|------|------|----------|
| 平台架构/研发 | `platform` | FactoryOS 平台团队 |
| 实施顾问 | `integrator` | 集成实施 |
| 工厂 IT | `customer_it` | 客户信息科 |
| 业务负责人 | `business_owner` | 生产/车间主管 |
| 运维 on-call | `ops` | 7×12 运维 |
| 管理员 | `admin` | 租户 admin（shadow/开写） |

---

## 3. 全生命周期 Gate 总表

| Gate ID | 名称 | 触发 | 责任角色 | 自动？ | 下一 Gate |
|---------|------|------|----------|--------|-----------|
| **G-ADMIT** | 准入评估 | 售前完成系统清单 | integrator + business_owner | ⚠️ | G-PATH |
| **G-PATH** | 写入路径裁定 | 准入通过 | integrator + platform | ⚠️ | G-CONNECT |
| **G-CONNECT** | 系统连通 | tenant 创建 | integrator + customer_it | ✅ | G-DISCOVER |
| **G-DISCOVER** | 动词发现 | connect 成功 | integrator | ✅ | G-MAP |
| **G-MAP** | 字段映射 | discover 有候选 CMV | integrator | ⚠️ | G-BRONZE-REVIEW |
| **G-BRONZE-REVIEW** | Blueprint 人审 | S2 Agent 产出 / 新 mapping | integrator + platform | ❌ | G-GRAPH-DRAFT |
| **G-GRAPH-DRAFT** | Graph 工作坊 | 试点链路选定 | integrator + business_owner | ❌ | G-FREEZE |
| **G-FREEZE** | Graph 冻结 | Draft 逐节点确认 | business_owner | ❌ | G-RULE-BIND |
| **G-RULE-BIND** | 规则绑定 | Graph frozen | integrator | ⚠️ | G-PROVE |
| **G-PROVE** | Shadow 验证 | Rule 绑定完成 | integrator | ⚠️ | G-WRITE-APPROVE |
| **G-WRITE-APPROVE** | 批准生产写 | Shadow ≥14d + 对账无未解释 drift | admin + business_owner | ❌ | G-UAT |
| **G-UAT** | 试点 UAT | 开写已批准 | business_owner + operator | ❌ | G-EXPORT |
| **G-EXPORT** | D1 结案导出 | UAT 签字 | integrator | ✅ | G-HANDOVER |
| **G-IMPORT** | 第二家导入 | 有 Silver Package | integrator | ✅ | G-PROVE |
| **G-HANDOVER** | 运维移交 | D1 结案 | ops + customer_it | ⚠️ | — |
| **G-DRIFT** | 对账漂移 | drift_detected | ops + integrator | ❌ | G-PROVE |
| **G-REVERT** | 撤回失败 | revert_failed | ops + integrator | ❌ | — |
| **G-CIRCUIT** | 熔断恢复 | circuit_open | ops | ⚠️ | G-PROVE |
| **G-D2-PACK** | D2 Pack 化评审 | 定制需求 | platform + integrator | ❌ | G-FREEZE |
| **G-SYSTEM-ENUM** | 新 Legacy 类型 | 10 类 enum 外系统 | platform | ❌ | ADR 流程 |

---

## 4. 接入与扩展主路径（按 GIP 模式）

```text
                    ┌─────────────┐
                    │  G-ADMIT    │
                    └──────┬──────┘
                           ▼
                    ┌─────────────┐
              ┌─────│   G-PATH    │ Path A / B / C（ADR-005）
              │     └──────┬──────┘
              │            ▼
              │     ┌─────────────┐
              │     │ G-CONNECT   │ system_relations draft
              │     └──────┬──────┘
              │            ▼
              │     ┌─────────────┐
         S1   │     │ G-DISCOVER  │
    (≤1周)    ├────►│ G-MAP       │ 可跳过若 Silver 全匹配
              │     └──────┬──────┘
              │            ▼
         S2   │     ┌─────────────┐
    (≤2周)    ├────►│G-BRONZE-REVIEW│ Connector-Agent PR
              │     └──────┬──────┘
         S3   │            ▼
    (1-2周)   └────► Python Pack + meta blueprint
                           ▼
                    ┌─────────────┐
                    │G-GRAPH-DRAFT│ workshop
                    └──────┬──────┘
                           ▼
                    ┌─────────────┐
                    │  G-FREEZE   │ ❌ 不可自动
                    └──────┬──────┘
                           ▼
                    ┌─────────────┐
                    │ G-RULE-BIND │
                    └──────┬──────┘
                           ▼
                    ┌─────────────┐
                    │   G-PROVE   │ Shadow ≥14d
                    └──────┬──────┘
                           ▼
                    ┌─────────────┐
                    │G-WRITE-APPROVE│ ❌ 不可自动
                    └──────┬──────┘
                           ▼
                    ┌─────────────┐
                    │   G-UAT     │
                    └──────┬──────┘
                           ▼
                    ┌─────────────┐
                    │  G-EXPORT   │ Package + 配置枢纽目录
                    └─────────────┘
```

| 模式 | 跳过/简化 | 仍必经 Gate |
|------|-----------|-------------|
| **S1** import Package | G-MAP（若 mapping 已 Silver） | G-FREEZE、G-PROVE、G-WRITE-APPROVE |
| **S2** 新 Blueprint | 无 | + G-BRONZE-REVIEW |
| **S3** Python Connector | 无 | + G-BRONZE-REVIEW、contract test |

---

## 5. 各 Gate 行为路径（详）

### G-ADMIT · 准入评估

| 项 | 内容 |
|----|------|
| **触发** | 新客户意向；系统清单已收集 |
| **责任** | `integrator` 主笔；`business_owner` 确认试点产线 |
| **禁止** | 未评估即 connect 生产 Legacy |
| **步骤** | ① 填 [04 §Step 0](../../准备/2026-06-16/04-工厂实施手册.md) 系统清单 ② 判定 S/A/B/C ③ 核对 ERP 在认证目录 ④ 确认 License Pack ⑤ 输出《准入评估报告》 |
| **产出物** | 准入报告 PDF + `tenant.yaml` 草案（`lifecycle=planned`） |
| **下一** | G-PATH |

---

### G-PATH · 写入路径裁定

| 项 | 内容 |
|----|------|
| **触发** | G-ADMIT 通过 |
| **责任** | `integrator` + `platform`（Path C 须 platform 确认） |
| **步骤** | ① 有 ERP 无 MES → **Path A** ② 有 MES → **Path B** ③ 无 ERP B-Lite → **Path C** ④ 写入 `tenant.yaml spec.path` ⑤ 选定 Starter Pack 列表 |
| **产出物** | `tenant.yaml` 中 `path` + `licensed_packs` |
| **下一** | G-CONNECT |

---

### G-CONNECT · 系统连通

| 项 | 内容 |
|----|------|
| **触发** | tenant 已 provision |
| **责任** | `integrator` + `customer_it`（凭证） |
| **步骤** | ① 创建 `integration/tenants/{id}/system_relations/*.yaml`（draft） ② 配置 `secrets_ref`（Vault，不进 Git） ③ 私网 ERP：部署 Edge Agent ④ `POST /v1/integration/connect/test` ⑤ 记录连通报告 |
| **CLI（W2+）** | `factoryos integration connect --tenant {id} --relation erp-kingdee` |
| **产出物** | 连通报告；relation `lifecycle=draft`；Audit `integration.connect_ok` |
| **下一** | G-DISCOVER |

---

### G-DISCOVER · 动词发现

| 项 | 内容 |
|----|------|
| **触发** | connect 成功 |
| **责任** | `integrator` |
| **步骤** | ① 上传厂商 OpenAPI 或选 catalog Blueprint ② `POST /v1/integration/discover` ③ `POST /v1/integration/blueprint/validate` ④ 输出 CMV 候选清单 |
| **CLI** | `factoryos integration discover --tenant {id} --openapi vendor.yaml` |
| **产出物** | CMV 候选表；Blueprint validate 报告 |
| **下一** | G-MAP 或 G-BRONZE-REVIEW（S2） |

---

### G-MAP · 字段映射

| 项 | 内容 |
|----|------|
| **触发** | discover 完成；CMV 候选已确认 |
| **责任** | `integrator`；AI 建议须人确认（Evolution EVO-02） |
| **步骤** | ① Studio map 或编辑 `mapping_overrides` ② `PUT /v1/integration/mappings/{packId}` ③ 跑 contract test 样例 ④ 差异记入 overrides |
| **CLI** | `factoryos integration map --tenant {id} --pack {pack_id} --file mapping.yaml` |
| **产出物** | `mapping_overrides` 或 `overrides.yaml` 补丁 |
| **下一** | G-GRAPH-DRAFT（Silver 已存在）或 G-BRONZE-REVIEW（新 Blueprint） |

---

### G-BRONZE-REVIEW · Blueprint 人审

| 项 | 内容 |
|----|------|
| **触发** | Connector-Agent 产出；或新 vendor Blueprint PR |
| **责任** | `integrator` + `platform` |
| **禁止** | 自动 promote Bronze → Silver（EVO-X04） |
| **步骤** | ① Review `integration/catalog/` PR ② 跑 contract tests 全绿 ③ 核对 CMV 动词已注册 ④ 无 vendor 私有动词 ⑤ merge + 更新认证分级 |
| **产出物** | merged Blueprint；catalog 认证等级（bronze/silver） |
| **下一** | G-GRAPH-DRAFT |

---

### G-GRAPH-DRAFT · Graph 工作坊

| 项 | 内容 |
|----|------|
| **触发** | 试点业务链选定（如报工） |
| **责任** | `integrator` 引导；`business_owner` 确认节点 |
| **禁止** | Agent 自动认定链路（08 红线）；EVO-X01 |
| **步骤** | ① 导入行业模板（若有）② AI 生成 Draft ③ 1～3 场 workshop ④ 记录差异清单 ⑤ Draft 存 `integration/packs/` 或 Graph API draft |
| **产出物** | Graph Draft JSON；《差异清单》 |
| **下一** | G-FREEZE |

---

### G-FREEZE · Graph 冻结

| 项 | 内容 |
|----|------|
| **触发** | Draft 经业务逐节点确认 |
| **责任** | `business_owner` 签字；`integrator` 操作 API |
| **禁止** | ❌ **任何脚本/Agent 自动 freeze**（ADR-002 R-09） |
| **步骤** | ① [04 §2.3 Checklist](../../准备/2026-06-16/04-工厂实施手册.md) 全勾 ② `POST .../submit` ③ `POST .../freeze` ④ 存档 checksum ⑤ 绑定 RuleSet 版本 |
| **CLI** | `factoryos graph freeze --tenant {id} --graph {graph_id} --version {v}` |
| **产出物** | frozen Graph；checksum 记录；Audit `graph.frozen` |
| **下一** | G-RULE-BIND |

---

### G-RULE-BIND · 规则与 DSL 绑定

| 项 | 内容 |
|----|------|
| **触发** | Graph frozen |
| **责任** | `integrator` |
| **步骤** | ① 加载 cap-report-l2 Rule 模板 ② 绑定 Graph 节点 allowed_dsl ③ Override 仅改阈值/参数 ④ `POST /v1/rulesets/{id}/evaluate` 冒烟 |
| **产出物** | active RuleSet；License Pack 校验通过 |
| **下一** | G-PROVE |

---

### G-PROVE · Shadow 验证

| 项 | 内容 |
|----|------|
| **触发** | Rule 绑定完成；`tenant.shadow_mode=true` |
| **责任** | `integrator` |
| **步骤** | ① 确认 shadow_mode=true（默认）② 跑 Harness 场景 + contract test ③ `POST /v1/integration/prove/run` ④ 每日对账 K-01 ≥14 天 ⑤ drift 须归零或可解释 |
| **CLI** | `factoryos integration prove --tenant {id} --min-shadow-days 14` |
| **产出物** | Prove 报告；Reconciliation 日报 |
| **下一** | G-WRITE-APPROVE（无未结案 drift） |

---

### G-WRITE-APPROVE · 批准生产写

| 项 | 内容 |
|----|------|
| **触发** | Prove 通过；Shadow ≥14d；Contract Test 全绿 |
| **责任** | `admin` + `business_owner` 双签 |
| **禁止** | ❌ CLI 直接 `shadow_mode=false` 无 Audit 签字 |
| **步骤** | ① 审 Prove 报告 + 对账 ② 业务负责人书面/电子签 ③ `POST` 开写批准（或 `factoryos integration approve-write`）④ 系统写 Audit `integration.write_approved` ⑤ `PUT /v1/tenants/{id}/settings` `shadow_mode=false` |
| **产出物** | 开写批准书；Audit 事件；`tenant.yaml status.write_approved=true` |
| **下一** | G-UAT |

---

### G-EXPORT · D1 结案导出

| 项 | 内容 |
|----|------|
| **触发** | UAT 完成；D1 签字 |
| **责任** | `integrator` |
| **步骤** | ① `POST /v1/packages/export` ② 打 Git tag `tenant-{id}-d1-v1` ③ 归档 `integration/tenants/{id}/` ④ 写入 [配置枢纽](../架构/配置枢纽与关系模型.md) 清单 |
| **CLI** | `factoryos pack export --tenant {id} --delivery D1 --out impl-package.json` |
| **产出物** | Implementation Package；配置枢纽目录快照 |
| **下一** | G-HANDOVER 或 下一家 G-IMPORT |

---

### G-IMPORT · 第二家导入（S1）

| 项 | 内容 |
|----|------|
| **触发** | 新 tenant；已有 Silver impl-package |
| **责任** | `integrator` |
| **步骤** | ① 复制 tenant 模板目录 ② `POST /v1/packages/import` ③ 更新 `system_relations` 凭证与 base_url ④ **仍须** G-PROVE → G-WRITE-APPROVE（治理不省略） |
| **CLI** | `factoryos pack import --tenant {new_id} --file impl-package.json` |
| **产出物** | import 报告；draft relations |
| **下一** | G-PROVE |

---

### G-HANDOVER · 运维移交

| 项 | 内容 |
|----|------|
| **触发** | G-EXPORT 完成 |
| **责任** | `ops` + `customer_it` |
| **步骤** | ① [04 Step 7](../../准备/2026-06-16/04-工厂实施手册.md) ② 交接监控/告警联系人 ③ 确认 Runbook 可达 ④ 约定 drift/revert SLA |
| **产出物** | 《运维移交清单》签字 |
| **下一** | 生产运维（G-DRIFT / G-REVERT / G-CIRCUIT） |

---

## 6. 运维 Gate（事件驱动）

> 详步骤见 [运维 Runbook](./运维Runbook.md)；本节只定 **入口与升级**。

| Gate | 触发 | 第一步（30 分钟内） | 升级 |
|------|------|---------------------|------|
| **G-DRIFT** | `drift_detected` | `shadow_mode=true` 冻结新写 | L2：24h 未结案 → platform |
| **G-REVERT** | `revert_failed` | 停止同 legacy_ref 重试 | L3：财务争议 → 书面报告 |
| **G-CIRCUIT** | `circuit_open` | Edge/Legacy 连通检查 | L1：4h 未恢复 → on-call |

**共性收尾**：修复 → G-PROVE 试跑 → 解除冻结 → Audit 结案事件。

---

## 7. D2 与平台变更 Gate

### G-D2-PACK · 定制 Pack 化评审

| 项 | 内容 |
|----|------|
| **触发** | 客户特异需求；Override 无法表达 |
| **责任** | `platform` + `integrator` |
| **步骤** | ① 评估是否 `override-scope` ② 否则新 Skill/Graph Pack ③ 登记 [追溯矩阵](../架构/能力-模块包-模块追溯矩阵.md) ④ ≥70% 须 Pack 化（08）⑤ 再走 G-FREEZE |
| **产出物** | 新 Pack ID；D2 书面范围 |

### G-SYSTEM-ENUM · 新 Legacy 系统类型

| 项 | 内容 |
|----|------|
| **触发** | 需求超出 erp/mes/wms/oa 等 10 类 enum |
| **责任** | `platform` |
| **步骤** | ① 新 ADR ② 更新 CMV/Schema ③ **非**实施顾问自行加枚举 |
| **产出物** | ADR Accepted |

---

## 8. 与 04 七步 / Studio 六步对照

| 04 七步 | Studio 六步 | 本 Playbook Gate |
|---------|-------------|------------------|
| Step 0 准入 | — | G-ADMIT, G-PATH |
| Step 1 接入 | connect | G-CONNECT, G-DISCOVER |
| Step 2 冻结 | discover, map, freeze | G-MAP, G-BRONZE-REVIEW, G-GRAPH-DRAFT, G-FREEZE |
| Step 3 绑规则 | — | G-RULE-BIND |
| Step 4 影子 | prove | G-PROVE |
| Step 5 UAT | — | G-WRITE-APPROVE, G-UAT |
| Step 6 推广 | — | （工厂内推广，复用 G-UAT 签字扩展） |
| Step 7 运维 | export | G-EXPORT, G-HANDOVER |

---

## 9. 实施速查卡（打印用）

```text
新客户 D1：
  G-ADMIT → G-PATH → G-CONNECT → G-DISCOVER → G-MAP
  → G-GRAPH-DRAFT → G-FREEZE ❌ → G-RULE-BIND → G-PROVE
  → G-WRITE-APPROVE ❌ → G-UAT → G-EXPORT → G-HANDOVER

第二家 S1：
  G-IMPORT → 改 system_relations 凭证 → G-PROVE → G-WRITE-APPROVE ❌ → G-EXPORT

新 ERP 厂商 S2：
  … → G-BRONZE-REVIEW ❌ → … → G-FREEZE ❌ → …

生产事故：
  G-DRIFT / G-REVERT / G-CIRCUIT → 修 → G-PROVE → 解除冻结

永远禁止自动：
  freeze · 开写 · Bronze→Silver · 绕过 Rule/Execution 写 Legacy
```

---

## 10. 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0.0 | 2026-06-16 | 初版：全 Gate 表 · 主路径图 · 与 04/Studio/Runbook 对齐 |
