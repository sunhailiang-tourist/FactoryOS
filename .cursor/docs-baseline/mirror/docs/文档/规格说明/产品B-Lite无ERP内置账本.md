# 规格说明·产品 B Lite：无 ERP 内置账本

| 版本 | v0.1.0 |
|------|--------|
| 日期 | 2026-06-16 |
| 状态 | **预埋规格**（Y1 默认不实现；老板拍板后可按本文开工） |
| 关联 | [连接器](./连接器.md) · [DSL执行动词](./DSL执行动词.md) · [06 数据边界](../../准备/2026-06-16/06-数据边界与部署策略.md) · [AC-B-LITE-001](../验收/验收用例-B-LITE-001-无ERP内置账本.md) |

---

## 1. 定位

| 项 | 定义 |
|----|------|
| **产品名** | 产品 B Lite（无 ERP 最小生产体系） |
| **客户** | C 类：无 ERP/MES 或仅 Excel/纸质（见 `01` §2.1） |
| **与 Overlay 关系** | **同一套 OS 内核**（Graph / Rule / DSL / Audit / Revert / Harness）；仅 **Connector 目标** 从外部 Legacy 改为 **内置 PostgreSQL 账本** |
| **不是** | 全栈 ERP、财务自动记账、WMS/QMS 全链路、默认 Layer 3 数仓 |

**一句话**：让无系统小厂以 **D1 同等机制**（报工 + 确认 + Revert + 对账）跑通生产闭环；账本在 FactoryOS 托管的 **最小表集**，而非客户金蝶/用友。

---

## 2. 何时启用（准入）

与 [04 工厂实施手册](../../准备/2026-06-16/04-工厂实施手册.md) C 级原则对齐，**加** B Lite 专用 Gate：

| # | 条件 | 说明 |
|---|------|------|
| B-01 | 书面确认试点产线/车间 | 与 Overlay 相同 |
| B-02 | **编码 workshop 结案** | 物料码、工单号规则、工序清单（客户签字） |
| B-03 | 接受 D1 边界 | 仅报工闭环；**不做**自动财务/采购/库存调整 |
| B-04 | 付费 | 咨询费 + 实施费 + 订阅（高于 Overlay Starter） |
| B-05 | License | 必须含 `conn-mes-builtin` + D1 Pack 组合（§8） |

**禁止开工**：无编码规范、要求 Day1 替代金蝶、拒绝 Shadow / 书面结案。

---

## 3. 架构：只换 Connector，不换内核

```text
钉钉 H5 / 语音 / 扫码
        ↓
感知 + Harness 确认门          ← 与 Overlay 相同
        ↓
agent_orchestrator → DSL 计划   ← 与 Overlay 相同
        ↓
Rule Engine → execution_service ← 与 Overlay 相同
        ↓
conn-mes-builtin (vendor=builtin)  ← 唯一差异：写内置 PG，非外部 MES API
        ↓
builtin_ledger schema（RDS PostgreSQL，tenant 隔离）
```

**红线不变**（ADR-002）：Agent 禁止直写；Graph 未 freeze 禁止写；每次写必有 Audit + Compensator。

### 3.1 Registry 注册

```python
# os_core/connector_sdk/mes/builtin/
registry.register("mes-builtin", BuiltinMesConnector(session_factory))
# 无 ERP 客户不注册 erp-*；QUERY_WO 等只读走 mes-builtin.read
```

| Registry Key | system | vendor | 能力 |
|--------------|--------|--------|------|
| `mes-builtin` | `mes` | `builtin` | L0 读 + L2 写 + Revert |

> **不新增** `LegacySystem` 枚举项；`builtin` 是 **vendor**，不是新 system（遵守 [连接器](./连接器.md) §2.2）。

### 3.2 与 Overlay 租户配置差异

| 配置项 | Overlay（A/B） | B Lite（C） |
|--------|----------------|-------------|
| `connectors.mes` | `mes-{vendor}` | `mes-builtin` |
| `connectors.erp` | `erp-{vendor}-read` | **未配置**（403 或走 builtin 只读） |
| Data-L0 权威 | 客户 ERP/MES | **builtin_ledger 表** |
| 对账 Job | OS ↔ 外部 MES/ERP | OS ExecutionRecord ↔ builtin 表 **内部一致校验** |

---

## 4. 内置账本：最小数据模型

Schema 名：`builtin_ledger`（每 tenant 逻辑隔离，`tenant_id` 列 + RLS 或应用层过滤）。

### 4.1 表清单（B1 首期）

| 表 | 用途 | B1 |
|----|------|-----|
| `material` | 物料主数据（最简） | ✅ |
| `work_center` | 产线/工作中心 | ✅ |
| `work_order` | 工单 | ✅ |
| `work_report` | 报工记录 | ✅ |
| `inventory_balance` | 库存余额 | ❌ B2 可选 |
| `bom` / `routing` | BOM / 工艺路线 | ❌ 不做 |

### 4.2 DDL（PostgreSQL 16）

```sql
CREATE SCHEMA IF NOT EXISTS builtin_ledger;

CREATE TABLE builtin_ledger.material (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       TEXT NOT NULL,
    material_code   TEXT NOT NULL,
    name            TEXT NOT NULL,
    unit            TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (tenant_id, material_code)
);

CREATE TABLE builtin_ledger.work_center (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       TEXT NOT NULL,
    code            TEXT NOT NULL,
    name            TEXT NOT NULL,
    UNIQUE (tenant_id, code)
);

CREATE TABLE builtin_ledger.work_order (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       TEXT NOT NULL,
    wo_no           TEXT NOT NULL,
    material_id     UUID REFERENCES builtin_ledger.material(id),
    work_center_id  UUID REFERENCES builtin_ledger.work_center(id),
    planned_qty     NUMERIC(18, 4) NOT NULL CHECK (planned_qty > 0),
    completed_qty   NUMERIC(18, 4) NOT NULL DEFAULT 0 CHECK (completed_qty >= 0),
    status          TEXT NOT NULL CHECK (status IN ('draft','released','in_progress','closed')),
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (tenant_id, wo_no)
);

CREATE TABLE builtin_ledger.work_report (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id       TEXT NOT NULL,
    wo_id           UUID NOT NULL REFERENCES builtin_ledger.work_order(id),
    quantity        NUMERIC(18, 4) NOT NULL CHECK (quantity > 0),
    reported_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    reported_by     TEXT NOT NULL,
    idempotency_key TEXT NOT NULL,
    status          TEXT NOT NULL DEFAULT 'active' CHECK (status IN ('active','reverted')),
    execution_id    UUID,  -- 关联 ExecutionRecord.id
    UNIQUE (tenant_id, idempotency_key)
);

CREATE INDEX idx_wo_tenant_status ON builtin_ledger.work_order (tenant_id, status);
CREATE INDEX idx_wr_wo ON builtin_ledger.work_report (wo_id);
```

### 4.3 种子数据（实施）

编码 workshop 产出 CSV → `builtin_import` CLI（应急开发时实现）：

```text
materials.csv      material_code,name,unit
work_centers.csv   code,name
work_orders.csv    wo_no,material_code,work_center_code,planned_qty,status
```

---

## 5. `conn-mes-builtin` 接口契约

实现路径：`os_core/connector_sdk/mes/builtin/connector.py`

### 5.1 ReadOperation 映射

| DSL / 用途 | `op.name` | params | 返回 |
|------------|-----------|--------|------|
| `QUERY_WO` | `query_work_order` | `wo_no` 或 `wo_id` | 工单 + 物料 + 已完成量 |
| `QUERY_REPORT_HISTORY` | `query_report_history` | `wo_id`, `limit?` | 报工列表 |
| `QUERY_ENTITY` | `query_entity` | `entity_type`, `entity_id` | 通用实体（测试/扩展） |

样例见 [mes/builtin/samples/](../连接器/mes/builtin/samples/)。

### 5.2 WriteOperation 映射

| DSL | `op.name` | params | 行为 |
|-----|-----------|--------|------|
| `WORK_REPORT` | `work_report` | `work_order_id`, `quantity`, `idempotency_key`, `reported_by` | 插入 `work_report`；`work_order.completed_qty += quantity`；事务 |
| `WORK_REPORT_REVERT` | `work_report_revert` | `legacy_ref`（或 HTTP revert 用 `exec_id` 解析） | `status=reverted`；扣减 `completed_qty`；幂等 |

### 5.3 WORK_REPORT params（与 Overlay 对齐）

```json
{
  "work_order_id": "uuid",
  "quantity": 50,
  "idempotency_key": "wr-2026-06-16-001",
  "reported_by": "actor-uuid"
}
```

### 5.4 WriteResult / 对账

```json
{
  "legacy_system": "mes",
  "legacy_vendor": "builtin",
  "legacy_ref": "builtin_ledger.work_report:{uuid}",
  "before_snapshot": { "completed_qty": 100 },
  "after_snapshot": { "completed_qty": 150 }
}
```

**对账 Job（B Lite）**：`ExecutionRecord.after_snapshot` ↔ `work_report` 行 + `work_order.completed_qty` 汇总；无需外部 API read-back。

### 5.5 health_check

```json
{ "status": "ok", "latency_ms": 5, "details": { "schema": "builtin_ledger" } }
```

---

## 6. Graph / Skill（复用 D1）

| 组件 | Pack ID | 说明 |
|------|---------|------|
| Graph | `graph-d1-core` + `graph-work-report` | 与 Overlay **相同** frozen 结构 |
| Capability | `cap-report-l2` + `cap-perception-v1` | 相同 |
| Skill | `skill-work-report-v1` | 相同 |
| Connector | **`conn-mes-builtin`** | B Lite 专用 |

租户 `connectors.yaml` 示例：

```yaml
tenant_id: shoe-factory-001
connectors:
  mes: mes-builtin
  im: conn-dingtalk
# erp: 不配置
licenses:
  - conn-mes-builtin
  - graph-d1-core
  - cap-report-l2
  - skill-work-report-v1
  - cap-perception-v1
```

---

## 7. 交付阶段（B0～B3）

| 阶段 | 内容 | 周期（估） |
|------|------|------------|
| **B0** | 编码 workshop + Graph freeze 签字 | 2～4 周 |
| **B1** | D1 同等：Shadow → 真实写 → Revert → 对账 → 结案 | 6～12 周 |
| **B2** | 计件草案、简单库存只读（可选） | D1 后 4～10 周 |
| **B3** | 客户长大 → 接 `conn-erp-{vendor}` / `conn-mes-{vendor}`，数据迁移 | 单独立项 |

**B1 验收**：见 [AC-B-LITE-001](../验收/验收用例-B-LITE-001-无ERP内置账本.md)。

---

## 8. 商业 SKU（预埋）

| SKU | 含 Pack | 备注 |
|-----|---------|------|
| **Starter-B** | Platform-L0 + D1 Graph/Cap/Skill + `conn-mes-builtin` + `conn-dingtalk` | 无 `conn-erp-*` |
| **咨询加购** | 编码 workshop、主数据导入 | 必选项 |
| **迁移加购** | B3 接真 ERP/MES | 另合同 |

定价数字首家 B1 结案后回填（与 `09` 一致）。

---

## 9. 应急开发顺序（老板拍板后）

在 **AC-BASE-001 已通过** 前提下增量开发（不重做内核）：

```text
1. Alembic migration：builtin_ledger 四表（§4.2）
2. os_core/connector_sdk/mes/builtin/（read/write/revert）
3. Registry + License：conn-mes-builtin
4. DSL 映射：WORK_REPORT / WORK_REPORT_REVERT → builtin ops（若 Overlay 已做则仅加映射表行）
5. 对账 Job：builtin 内部一致性分支
6. builtin_import CLI + 样例 CSV
7. AC-B-LITE-001 全绿
8. 复用 UX-001 / Harness / perception（无改动）
```

预估增量：**2～4 周**（1～2 人，在底座已就绪后）。

---

## 10. 迁移至真 ERP/MES（B3）

```text
1. 新客户侧部署 ERP/MES，历史 builtin 数据导出
2. 新 Connector Pack 注册（conn-mes-{vendor}）
3. Graph **clone 新版本** + 改 connector_ops 映射（不改 Rule 语义）
4. 切换 tenant connectors 配置；Shadow 再跑 14 天
5. builtin_ledger 只读归档或 TTL 停用
```

**原则**：ExecutionRecord 与 Audit **长期保留**；builtin 表可降级为 Layer 2 缓存。

---

## 11. 明确不做（B Lite B1）

- 财务凭证、应收应付、成本结转  
- 采购订单、销售订单全链路  
- 全量 BOM / APS 排产  
- 跨客户数据汇总（Data-L3 默认不做）  
- Agent 自动 freeze Graph  

---

## 12. 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v0.1.0 | 2026-06-16 | 预埋：数据模型、conn-mes-builtin 契约、SKU、应急开发顺序 |
