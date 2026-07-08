"""modules/execution 包根。

作用：Execution 域 HTTP 模块命名空间与 get_routers 导出。
业务关联：E-02 L2 执行 · E-04/E-05 revert。
上游：router/v1/registry · ROUTER_PROVIDERS。
下游：controllers · os_core.execution_service。
"""
from server.api.modules.execution.routers import get_routers

__all__ = ["get_routers"]
