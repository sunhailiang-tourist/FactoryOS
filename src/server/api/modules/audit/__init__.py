"""modules/audit 包根。

作用：Audit 域 HTTP 模块命名空间与 get_routers 导出。
业务关联：E-03 append-only 审计查询。
上游：router/v1/registry · ROUTER_PROVIDERS。
下游：controllers · os_core.audit_service。
"""
from server.api.modules.audit.routers import get_routers

__all__ = ["get_routers"]
