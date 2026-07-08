"""Platform Registry 包入口（ADR-008 · Contract/Pack/Tenant DB 真源）。

作用：导出 bootstrap 与 Session 绑定 API。
业务关联：ADR-008 运行时 Registry 真源切换。
上游：server.api lifespan · conftest
下游：shared_contracts loaders · connector_sdk.registry
"""
from os_core.platform_registry.bootstrap import bootstrap_registry
from os_core.platform_registry.session import get_registry_session, set_registry_session

__all__ = [
  "bootstrap_registry",
  "get_registry_session",
  "set_registry_session",
]
