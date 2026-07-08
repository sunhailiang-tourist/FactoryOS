"""modules/probes 包根。

作用：Probes 域 HTTP 模块命名空间与 get_routers 导出。
业务关联：K8s 进程/就绪探针（非 OpenAPI 正式域）。
上游：router/v1/registry · ROUTER_PROVIDERS。
下游：controllers · 无（进程内自检）。
"""
from server.api.modules.probes.routers import get_routers

__all__ = ["get_routers"]
