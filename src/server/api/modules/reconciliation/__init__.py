"""modules/reconciliation 包根。

作用：Reconciliation 域 HTTP 模块命名空间与 get_routers 导出。
业务关联：K-01/K-02 对账 Job。
上游：router/v1/registry · ROUTER_PROVIDERS。
下游：controllers · os_core.reconciliation_service。
"""
from server.api.modules.reconciliation.routers import get_routers

__all__ = ["get_routers"]
