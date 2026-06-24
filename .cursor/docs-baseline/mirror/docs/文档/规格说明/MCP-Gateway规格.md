# 规格说明·MCP Gateway

| 版本 | **v1.0.1** |
|------|------------|
| 范围 | Platform-L1 治理型 MCP 暴露层 |
| 决策 | ADR-004 |
| 模块 | `os_core/mcp_gateway/` |

## 1. 职责

将 **已授权 CMV（Canonical Manufacturing Verbs）** 以 [Model Context Protocol](https://modelcontextprotocol.io/) 工具形式暴露给外部 Agent / Copilot / 钉钉机器人。

**差异化**：Celonis MCP 偏 PI **读**；FactoryOS MCP 偏 **受治理的制造写动词**——但 **tools/call 不直写 Legacy**。

## 2. 写路径（不可变）

```text
MCP Client
  → MCP Gateway tools/call
  → agent_orchestrator（产出 DSL Plan JSON）
  → Harness confirm（R-11）
  → Rule → execution_service → Connector
```

## 3. 工具面

| MCP 能力 | 行为 |
|----------|------|
| `tools/list` | 返回 tenant License 已授权的 **CMV 子集** |
| `tools/call` | 输入 CMV + params → 返回 **DSL Plan JSON**（非执行结果写 Legacy） |
| `resources/list` | （Y2）只读 Graph 摘要、对账状态 |

工具名 = CMV 动词名（如 `WORK_REPORT`），schema 来自 [CMV注册表.yaml](../数据结构/CMV注册表.yaml)。

## 4. 安全

| 项 | Phase |
|----|-------|
| tenant scope | Y1 内部：API key + tenant header |
| OAuth 2.1 + PKCE | Y2 对外；对齐 MCP 2026-07 RC |
| 工具级 ACL | Rule Engine 二次判定 |
| Audit | 每次 tools/call append audit（含 plan_id） |
| 禁止 token passthrough | 硬拒绝 |

## 4.1 OpenTelemetry · MCP SEP-414

FactoryOS MCP Gateway **MUST** 实现 [SEP-414](https://modelcontextprotocol.io/seps/414-request-meta) 约定的 W3C Trace Context 传播：

| `_meta` 键 | 格式 | 方向 |
|------------|------|------|
| `traceparent` | W3C Trace Context | Client → Gateway → agent_orchestrator span 父上下文 |
| `tracestate` | W3C Trace Context | 同上（可选） |
| `baggage` | W3C Baggage | 同上（可选） |

**规则**：

1. `tools/call` 的 `params._meta` 携带上述键（**不**使用 DNS 前缀如 `io.modelcontextprotocol.traceparent`）。
2. Gateway 提取 `_meta` 作为 `mcp.tools.call` span 的 remote parent；产出 DslPlan 时写入 `plan_id` 属性，与 [可观测性规范](./可观测性规范.md) §2 对齐。
3. Streamable HTTP 传输层可 **额外** 设 HTTP `traceparent` 头（SEP-2028 方向）；**MCP 层以 `_meta` 为准**。
4. Y1 stub 可 no-op 提取；Phase 1 代码须保留 `_meta` 解析钩子。

**示例**（`tools/call`）：

```json
{
  "jsonrpc": "2.0",
  "id": 2,
  "method": "tools/call",
  "params": {
    "name": "WORK_REPORT",
    "arguments": { "work_order_id": "WO-1", "quantity": 50 },
    "_meta": {
      "traceparent": "00-0af7651916cd43dd8448eb211c80319c-00f067aa0ba902b7-01"
    }
  }
}
```

## 5. 路由

```text
/mcp/v1/{tenant_id}     # Streamable HTTP（Y1 末）
```

内部 Skill 可先经同 Gateway，避免两套工具注册。

## 6. 验收

AC-BASE-001 **M-01**（tools/list）、**M-02**（call 不直写）、**M-03**（`_meta.traceparent` 关联 audit/plan_id）。

## 7. 时间表

| 里程碑 | 内容 |
|--------|------|
| Y1 末 | 内部 GA；mock CMV |
| Y2 | 对外 + OAuth |
| Y3 | Partner Pack 签名 + Registry 目录 |
