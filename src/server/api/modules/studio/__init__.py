"""modules/studio 包根。

作用：Studio 域 HTTP 模块命名空间与 get_routers 导出。
业务关联：Studio RBAC · 平台管理 API。
上游：router/v1/registry · ROUTER_PROVIDERS。
下游：controllers · os_core.platform_registry · tenant_service。
"""
from server.api.modules.studio.routers import get_routers

__all__ = ["get_routers"]
