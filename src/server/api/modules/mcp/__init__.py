"""modules/mcp 包根。

作用：MCP 域 HTTP 模块命名空间与 get_routers 导出。
业务关联：W7 MCP JSON-RPC 网关。
上游：router/v1/registry · ROUTER_PROVIDERS。
下游：controllers · os_core.mcp_gateway。
"""
from server.api.modules.mcp.routers import get_routers

__all__ = ["get_routers"]
