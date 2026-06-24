# 规格说明·Edge Agent（私网 ERP 接入）

| 版本 | **v1.0.0** |
|------|------------|
| 日期 | 2026-06-16 |
| 状态 | **P1 PoC**（Hasen 私网 ERP 阻塞项） |
| 决策 | ADR-004 §6 · ADR-006 |
| 对标 | Tulip [OPCH](https://support.tulip.co/docs/on-premise-connector-hosts) 出站模型 |

---

## 1. 为什么需要 Edge Agent

客户 ERP/MES **不出公网** 时，Core ECS 无法直连 Legacy API。Edge Agent 部署在 **客户内网**，由 Core **出站 WebSocket 长连** 下发 Blueprint 调用，结果回传 Core。

```text
FactoryOS Core (cloud/VPC)
  ↔ WSS 出站（Edge 发起）
Edge Agent (customer LAN)
  → HTTPS → ERP/MES API
```

**禁止**：Edge Agent 直写 PostgreSQL 业务表；**必须** 经 Blueprint ops 映射 CMV。

---

## 2. 组件职责

| 组件 | 职责 |
|------|------|
| **Edge Agent** | 维持 WSS；执行 `connector.op`；本地 secrets 注入 |
| **Core `connector_sdk/runtime`** | 路由 tenant+pack 到在线 Edge；超时/熔断 |
| **Integration Studio** | 显示 Edge 在线状态（Connect 步） |

---

## 3. 协议（P1 PoC）

### 3.1 连接

```text
WSS wss://{api_host}/v1/edge/{tenant_id}/connect
Headers:
  Authorization: Bearer {edge_token}
  X-Edge-Agent-Id: {agent_id}
  X-Edge-Version: 1.0.0
```

- Edge **主动出站** 443；客户防火墙无需 inbound 到 Core  
- Token 由 tenant 管理员在 Studio 签发，**可轮换**

### 3.2 健康检查（对标 Tulip OPCH Release 359）

| 端点 | 用途 |
|------|------|
| `GET /health-check` | 进程存活 |
| `GET /ready-check` | 已连 Core + 本地 secrets 可读 |

K8s/Docker 编排 **SHOULD** 使用上述端点。

### 3.3 下行消息（Core → Edge）

```json
{
  "type": "connector.op",
  "request_id": "uuid",
  "pack_id": "conn-erp-kingdee-write",
  "verb": "WORK_REPORT",
  "params": { },
  "idempotency_key": "..."
}
```

### 3.4 上行消息（Edge → Core）

```json
{
  "type": "connector.result",
  "request_id": "uuid",
  "outcome": "success",
  "legacy_ref": "...",
  "before_snapshot": {},
  "after_snapshot": {},
  "latency_ms": 120
}
```

`outcome` 枚举见 [可观测性规范](./可观测性规范.md) §3。

---

## 4. 本地状态

| 项 | 存储 |
|----|------|
| Blueprint 缓存 | `/var/lib/factoryos-edge/blueprints/` |
| Secrets | 环境变量或本地 vault ref（**禁止** 回传 Core 日志） |
| 离线队列 | PoC **不实现**；断连 → Core 返回 `EDGE_OFFLINE` |

---

## 5. 安全

- Edge Token **scoped** 到 `tenant_id` + `pack_id` 列表  
- 日志 **禁止** 全量 Legacy payload（采样 + TTL 7d 可选）  
- Edge **不得** 接受来自局域网的任意执行请求（仅 Core 下行）

---

## 6. Hasen 决策门禁

| 网络形态 | 接入方式 |
|----------|----------|
| ERP API 公网/VPN 白名单可达 Core | 直连 Blueprint，**无需** Edge |
| ERP 仅内网 | **必须** Edge PoC 或客户侧 API 网关 |

写入 [14-一年冲刺路线图](../准备/2026-06-16/14-一年冲刺路线图与并行研发.md) Hasen 首周 checklist。

---

## 7. Phase

| Phase | 范围 |
|-------|------|
| P1 PoC | WSS stub + 单 verb 透传 + health-check |
| Y2 | 多 Edge、离线队列、自动升级 |
| Y3 | 伙伴签名 Edge 包 |

---

## 8. 验收（待 AC-EDGE-001）

| ID | 条件 |
|----|------|
| EA-01 | Edge 出站连上 Core，Studio Connect 显示 online |
| EA-02 | WORK_REPORT 经 Edge 写 ERP 样例，ExecutionRecord 有 connector_trace |
| EA-03 | Edge 断连时 execute 返回可解释错误，不 silent fail |

---

## 9. 参考

- ADR-004 · [Connector-Blueprint规格](./Connector-Blueprint规格.md)  
- [10-阿里云基础设施定版方案](../准备/2026-06-16/10-阿里云基础设施定版方案.md) §VPN
