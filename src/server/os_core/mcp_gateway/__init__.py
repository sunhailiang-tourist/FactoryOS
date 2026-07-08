"""mcp_gateway 包导出（JSON-RPC tools/list · tools/call）。

作用：重导出 handle_mcp_json_rpc 公开入口。
业务关联：M-01/M-02 MCP Gateway · W7 stub。
上游：server.api.modules.mcp
下游：os_core.mcp_gateway.service
"""
from os_core.mcp_gateway.service import handle_mcp_json_rpc

__all__ = ["handle_mcp_json_rpc"]
