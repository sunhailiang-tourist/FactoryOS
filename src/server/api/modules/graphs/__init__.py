"""modules/graphs 包根。

作用：Graphs 域 HTTP 模块命名空间与 get_routers 导出。
业务关联：业务图谱 draft→freeze 生命周期。
上游：router/v1/registry · ROUTER_PROVIDERS。
下游：controllers · os_core.graph_service。
"""
from server.api.modules.graphs.routers import get_routers

__all__ = ["get_routers"]
