"""modules/harness 包根。

作用：Harness 域 HTTP 模块命名空间与 get_routers 导出。
业务关联：H-02 确认门 → Rule → Execute。
上游：router/v1/registry · ROUTER_PROVIDERS。
下游：controllers · os_core.rule_engine · execution_service。
"""
from server.api.modules.harness.routers import get_routers

__all__ = ["get_routers"]
