"""modules/integration 包根。

作用：Integration 域 HTTP 模块命名空间与 get_routers 导出。
业务关联：Studio Connect→Prove 六步。
上游：router/v1/registry · ROUTER_PROVIDERS。
下游：controllers · os_core.connector_sdk。
"""
from server.api.modules.integration.routers import get_routers

__all__ = ["get_routers"]
