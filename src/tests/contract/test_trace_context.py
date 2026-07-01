"""trace_context 契约：W3C traceparent → trace_id（M-03 · SEP-414）。

业务：MCP _meta 解析须稳定、非法输入忽略。
上游：shared_contracts/trace_context.py
下游：test_mcp_w8 integration
"""
from __future__ import annotations

import pytest

from os_core.shared_contracts.trace_context import (
  trace_id_from_mcp_meta,
  trace_id_from_traceparent,
)

_SPEC_EXAMPLE = "00-0af7651916cd43dd8448eb211c80319c-00f067aa0ba902b7-01"
_EXPECTED = "0af7651916cd43dd8448eb211c80319c"


@pytest.mark.contract
@pytest.mark.parametrize(
  "traceparent",
  [_SPEC_EXAMPLE, _SPEC_EXAMPLE.upper()],
  ids=["lowercase-flags", "uppercase-flags"],
)
def test_trace_id_from_traceparent_parses_w3c_segment(traceparent: str) -> None:
  """合法 traceparent → 32 位 trace_id（小写）。"""
  assert trace_id_from_traceparent(traceparent) == _EXPECTED


@pytest.mark.contract
@pytest.mark.parametrize(
  "invalid",
  ["", "not-a-traceparent", "00-tooshort-00f067aa0ba902b7-01", None],
  ids=["empty", "garbage", "short-trace-id", "none"],
)
def test_trace_id_from_traceparent_rejects_invalid(invalid: str | None) -> None:
  """非法 traceparent 返回 None（Gateway 仍产出 Plan）。"""
  assert trace_id_from_traceparent(invalid) is None


@pytest.mark.contract
def test_trace_id_from_mcp_meta_reads_traceparent_key() -> None:
  """params._meta.traceparent 入口。"""
  meta = {"traceparent": _SPEC_EXAMPLE}
  assert trace_id_from_mcp_meta(meta) == _EXPECTED


@pytest.mark.contract
def test_trace_id_from_mcp_meta_ignores_non_dict() -> None:
  assert trace_id_from_mcp_meta(None) is None
  assert trace_id_from_mcp_meta("string") is None
