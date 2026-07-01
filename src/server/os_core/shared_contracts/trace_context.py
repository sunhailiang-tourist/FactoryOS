"""W3C Trace Context 解析（MCP SEP-414 · M-03）。

作用：从 MCP params._meta.traceparent 提取 trace_id。
业务关联：mcp_gateway tools/call → DslPlan · audit correlation_id。
上游：mcp_gateway.service.call_tool
下游：agent_orchestrator.create_plan · audit_service
关联文档：docs/文档/规格说明/MCP-Gateway规格.md §4.1
"""
from __future__ import annotations

import re

# W3C traceparent: version-trace_id-parent_id-flags（trace_id 为 32 位 hex）
_TRACEPARENT_RE = re.compile(
  r"^[0-9a-f]{2}-([0-9a-f]{32})-[0-9a-f]{16}-[0-9a-f]{2}$",
  re.IGNORECASE,
)


def trace_id_from_traceparent(traceparent: str | None) -> str | None:
  """从 W3C traceparent 解析 32 位 trace_id。

  功能：校验 SEP-414 格式并返回 trace_id 段。
  业务含义：MCP Client 与 Gateway/Plan/Audit 分布式追踪关联。
  参数 traceparent：params._meta.traceparent 原始字符串。
  返回：小写 trace_id；格式非法或空则 None（忽略，仍产出 Plan）。
  """
  if not traceparent or not isinstance(traceparent, str):
    return None
  text = traceparent.strip()
  match = _TRACEPARENT_RE.match(text)
  if not match:
    return None
  return match.group(1).lower()


def trace_id_from_mcp_meta(meta: object | None) -> str | None:
  """从 MCP tools/call params._meta 对象提取 trace_id。

  功能：读取 _meta.traceparent 并解析。
  业务含义：Gateway 层 SEP-414 钩子入口。
  参数 meta：JSON-RPC params._meta dict。
  返回：trace_id 或 None。
  """
  if not isinstance(meta, dict):
    return None
  raw = meta.get("traceparent")
  if raw is None:
    return None
  return trace_id_from_traceparent(str(raw))
