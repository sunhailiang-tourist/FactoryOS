"""modules/tenant 包根。

作用：Tenant 域 HTTP 模块命名空间与 get_routers 导出。
业务关联：T-01 Shadow · STU-04 write_approved。
上游：router/v1/registry · ROUTER_PROVIDERS。
下游：controllers · os_core.tenant_service。
"""
from server.api.modules.tenant.routers import get_routers

__all__ = ["get_routers"]
