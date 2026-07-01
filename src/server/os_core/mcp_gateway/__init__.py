"""mcp_gateway 公开 API（JSON-RPC tools/list · tools/call）。"""
from os_core.mcp_gateway.service import handle_mcp_json_rpc

__all__ = ["handle_mcp_json_rpc"]
