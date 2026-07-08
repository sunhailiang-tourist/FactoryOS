"""modules/package 包根。

作用：Package 域 HTTP 模块命名空间与 get_routers 导出。
业务关联：Pack 导入导出。
上游：router/v1/registry · ROUTER_PROVIDERS。
下游：controllers · os_core.package_service。
"""
from server.api.modules.package.routers import get_routers

__all__ = ["get_routers"]
