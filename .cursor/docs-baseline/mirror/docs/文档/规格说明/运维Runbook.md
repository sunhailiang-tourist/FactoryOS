# 规格说明·运维 Runbook（P0 场景）

| 版本 | **v1.0.0** |
|------|------------|
| 日期 | 2026-06-16 |
| 范围 | 生产运维 **首版** 三类 P0 事件 |
| 关联 | [可观测性规范](./可观测性规范.md) · [Shadow-Mode与对账规格](./Shadow-Mode与对账规格.md) |

---

## 1. drift_detected（对账漂移）

### 触发

- 每日对账 Job `status=drift_detected`  
- Studio / IM 告警：`drift_count > 0`

### 影响

ExecutionRecord 与 Legacy read-back **不一致**；财务/产量可能不可信。

### 步骤

1. **冻结** 该 tenant 新 L2 写（`tenant.shadow_mode=true` 或运维开关）  
2. 导出 `ReconciliationReport` + 最近 24h `ExecutionRecord`（含 `connector_trace`）  
3. 比对 `match_key`（通常 `completed_qty` / `legacy_ref`）  
4. 分类：**Mapping 错误** → 修 Blueprint Override；**Legacy 延迟** → 重跑对账；**重复写** → 查 idempotency  
5. 修复后 **Shadow 试跑** → Prove → 解除冻结  
6. Audit 记录 `event_type=reconciliation.resolved`

### SLA

- **P1 响应** 4h；**结案** 24h（D1 客户）

---

## 2. revert_failed（撤回失败）

### 触发

- `WORK_REPORT_REVERT` outcome ≠ success  
- 告警 `revert_failed`

### 影响

Legacy 与 FactoryOS 账本 **分叉**；工人端显示已撤但 ERP/MES 仍有数。

### 步骤

1. **停止** 同 `legacy_ref` 的再次 revert 重试（防双撤）  
2. 读 Legacy 当前状态（QUERY_WO / read-back）  
3. 若 Legacy **已撤**：标记 ExecutionRecord `reverted` 补审计  
4. 若 Legacy **未撤**：人工在 Legacy 侧处理 + 记录工单号  
5. 检查 Blueprint `revert` op 与 compensator 映射  
6. 必要时 **主管确认** 后 compensating 手工调整（须 Audit）

### SLA

- **P0 响应** 1h；**24h** 内账本一致或书面例外

---

## 3. circuit_open（Connector 熔断）

### 触发

- `connector_trace.outcome=circuit_open`  
- healthCheck `status=degraded|down`

### 影响

该 `pack_id` 写操作失败；工人报工阻塞。

### 步骤

1. 确认 Legacy 可达（VPN/Edge Agent `/ready-check`）  
2. 查最近 `legacy_5xx` / `timeout` 比例（可观测性 §3）  
3. **降级**：仅 L0 只读；IM 通知「系统维护」  
4. 修复网络/凭证后 **手动半开**：单条 dry_run → 单条 Shadow 写  
5. `failure_threshold` 重置后恢复自动  
6. 记录 `event_type=connector.circuit_recovered`

### SLA

- **P1 响应** 30min；恢复目标 **4h**（Y1 SLO）

---

## 4. 升级路径

| 级别 | 条件 | 通知 |
|------|------|------|
| L1 | 单 tenant、可 Shadow 缓解 | 实施群 |
| L2 | 多 tenant 或 revert_failed | 研发 on-call |
| L3 | 数据不可恢复 / 财务争议 | 客户 IT + 书面报告 |

---

## 5. 参考

- AC-BASE-001 K-02, E-04, E-05  
- [04-工厂实施手册](../准备/2026-06-16/04-工厂实施手册.md) §运维移交
