"""Platform Registry 包（ADR-008 · Contract/Pack/Tenant DB 真源）。"""
from os_core.platform_registry.bootstrap import bootstrap_registry
from os_core.platform_registry.session import get_registry_session, set_registry_session

__all__ = [
  "bootstrap_registry",
  "get_registry_session",
  "set_registry_session",
]
