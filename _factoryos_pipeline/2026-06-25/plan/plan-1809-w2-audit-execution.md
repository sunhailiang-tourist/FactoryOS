# 预开发说明：W2 — audit_service · execution shadow/幂等

- **日期**：2026-06-25
- **对照契约**：`contracts/openapi/工厂操作系统-v1.1.yaml` · `contracts/acceptance/验收用例-BASE-001-平台底座.md`
- **架构入口**：`docs/文档/架构/FactoryOS完整架构设计.md` §16 W2 行
- **依赖 W1**：`shared_contracts` · Alembic S-01～S-04 · mock `connector_sdk` · C-01 ✅

---

## 1. 迭代目标

**一句话**：落地 append-only 审计 + 唯一写入口 execution（试跑/幂等/mock 写），为 W3 Rule/Graph 铺路。

**可测要点**：

1. `audit_service` append-only 落库 + `GET /v1/audit/events`
2. `execution_service` 经 `POST /v1/execute`：`dry_run` 不写 Legacy（E-06）
3. 同 `idempotency_key` 不重复写（E-07）
4. 每次执行产生 audit 记录（E-03）
5. `GET /v1/executions/{execId}/evidence` 返回 ExecutionEvidence（E-09）

**不在 W2**：Graph freeze · Rule evaluate · E-02/E-04 真写+Revert · D-01～D-04 · E-08（已有静态）· 52 P0 全绿

---

## 2. AC 对账表

| AC ID | 标题 | 本迭代 | 验证方式 |
|-------|------|--------|----------|
| E-03 | Audit 产生 | **是** Step 2+ | pytest `-k 'E-03'` |
| E-06 | dry_run 不写 | **是** Step 3 | pytest `-k 'E-06'` |
| E-07 | idempotency | **是** Step 3 | pytest `-k 'E-07'` |
| E-09 | Evidence 可重建 | **是** Step 4 | pytest `-k 'E-09'` |
| E-01～E-02 | Graph/真写 | **否** W3/W4 | pending |
| E-04～E-05 | Revert | **否** W4+ | pending |
| D-01～D-04 | DSL registry | **否** W3+ | pending |
| workflow | import_boundaries | **是** 每 Step | harness boundaries |
| 52 P0 其余 | — | **否** | pending |

---

## 3. 红线对账

| 主题 | 本迭代 | 负向/静态 |
|------|--------|-----------|
| 写经 execution_service | execute 唯一入口 | import 矩阵 · apps/api 无写规则 |
| audit append-only | 仅 insert + 查询 | 无 PATCH/DELETE |
| Shadow/dry_run | status=simulated，Legacy 不变 | E-06 |
| Agent 禁直写 | 不涉及 agent 写 | E-08 pending |
| integration 禁私有 API | 路由只调 os_core public | boundaries |

---

## 4. 接口清单

| 方法 | 路径 | 用途 | Step |
|------|------|------|------|
| GET | `/v1/audit/events` | 查询审计 | 2 |
| POST | `/v1/execute` | 执行 DSL（含 dry_run · idempotency_key） | 4 |
| GET | `/v1/executions/{execId}` | 单条 ExecutionRecord | 4 |
| GET | `/v1/executions` | 列表 | 4 |
| GET | `/v1/executions/{execId}/evidence` | ExecutionEvidence | 4 |

---

## 5. 模块与文件

| 模块 | 路径 | 变更 |
|------|------|------|
| 迁移 | `alembic/versions/002_audit_execution.py` | audit_events · execution_records 表 |
| audit | `os_core/audit_service/` | store · public API |
| execution | `os_core/execution_service/` | execute · idempotency · dry_run · evidence |
| connector | `os_core/connector_sdk/` | mock write 适配（dry_run 跳过） |
| API | `apps/api/routes/audit.py` · `executions.py` | 薄路由 |
| 测试 | `src/tests/integration/` · `contract/` | E-03/06/07/09 |

---

## 6. 分步计划

### Step 1 — Alembic + audit_service 内核

| 项 | 内容 |
|----|------|
| AC ID | workflow |
| 接口 | （无 HTTP，内核 API） |
| 模块路径 | `alembic/versions/002_*` · `os_core/audit_service/` |
| Harness 验收盘 | `./scripts/gate step --step 1 -k 'workflow'` |
| 风险 | 表字段与 `AuditEvent.schema.json` / ExecutionRecord schema 对齐 |
| 验收标准 | migration upgrade 绿 · audit append + 按 tenant/exec_id 查询 |

### Step 2 — audit HTTP + E-03

| 项 | 内容 |
|----|------|
| AC ID | E-03 |
| 接口 | GET `/v1/audit/events` |
| 模块路径 | `apps/api/routes/audit.py` |
| Harness 验收盘 | `./scripts/gate step --step 2 -k 'E-03'` |
| 风险 | tenant_id 隔离 |
| 验收标准 | 执行后查 audit 有 append-only 记录 |

### Step 3 — execution_service dry_run + 幂等

| 项 | 内容 |
|----|------|
| AC ID | E-06 · E-07 |
| 接口 | （os_core public execute，暂不接 HTTP） |
| 模块路径 | `os_core/execution_service/` · `connector_sdk` mock write |
| Harness 验收盘 | `./scripts/gate step --step 3 -k 'E-06'` |
| 风险 | idempotency_key 唯一约束 · simulated 状态 |
| 验收标准 | dry_run Legacy 不变 · 重复 key 不重复写 |

### Step 4 — execute/evidence HTTP + E-09

| 项 | 内容 |
|----|------|
| AC ID | E-09 · E-03 端到端 |
| 接口 | POST `/v1/execute` · GET executions/evidence |
| 模块路径 | `apps/api/routes/executions.py` · `main.py` 注册 |
| Harness 验收盘 | `./scripts/gate step --step 4 -k 'E-09'` |
| 风险 | ExecuteRequest 与 OpenAPI 一致 |
| 验收标准 | evidence JSON 过 ExecutionEvidence schema |

---

## 7. Harness 验收盘（全局）

```bash
./scripts/gate step --step 1 -k 'workflow'
./scripts/gate step --step 2 -k 'E-03'
./scripts/gate step --step 3 -k 'E-06'
./scripts/gate step --step 4 -k 'E-09'
./scripts/gate delivery   # 终轮
./scripts/gate pr
```

---

## 8. 编码纪律

同 W1 plan §1.1：`apps/api` 薄路由 · 中文注释 · 新目录 README · 无 tenant 分支
