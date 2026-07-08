"""modules/dsl 包根。

作用：DSL 域 HTTP 模块命名空间与 get_routers 导出。
业务关联：CMV 动词注册表只读。
上游：router/v1/registry · ROUTER_PROVIDERS。
下游：controllers · os_core.shared_contracts.cmv_registry。
"""
from server.api.modules.dsl.routers import get_routers

__all__ = ["get_routers"]
