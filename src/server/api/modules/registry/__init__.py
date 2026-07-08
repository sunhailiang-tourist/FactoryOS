"""modules/registry 包根。

作用：Registry 域 HTTP 模块命名空间与 get_routers 导出。
业务关联：Platform Registry 读 + 变更请求人审。
上游：router/v1/registry · ROUTER_PROVIDERS。
下游：controllers · os_core.platform_registry。
"""
from server.api.modules.registry.routers import get_routers

__all__ = ["get_routers"]
