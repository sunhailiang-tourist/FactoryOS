"""license_service：Pack 授权（W7 Step2 · tenant_pack_entitlements 真源）。

作用：assert_pack_licensed 供 execution 前门禁。
业务关联：T-02 MODULE_NOT_LICENSED · T-03 前序 connector 已配置。
上游：execution_service · platform_registry.tenant_config_store
下游：shared_contracts PlatformError
关联文档：src/server/os_core/license_service/README.md · ADR-003
"""
from __future__ import annotations

from sqlalchemy.orm import Session

from os_core.platform_registry import tenant_config_store
from os_core.platform_registry.session import get_registry_session
from os_core.shared_contracts.errors import ErrorCode
from os_core.shared_contracts.exceptions import PlatformError

# 无 Registry Session 时 fallback（单测 import 门禁 · 非 integration 路径）
_LICENSED_BY_TENANT_FALLBACK: dict[str, frozenset[str]] = {
  "default": frozenset({"conn-mock"}),
}


def _resolve_session(session: Session | None) -> Session | None:
  return session if session is not None else get_registry_session()


def is_pack_licensed(
  session: Session | None,
  *,
  tenant_id: str,
  pack_id: str,
) -> bool:
  """判断 tenant 是否授权 pack_id。

  功能：只读校验，不抛异常。
  业务含义：Harness / 编排层可预检；真源 tenant_pack_entitlements。
  """
  sess = _resolve_session(session)
  if sess is None:
    licensed = _LICENSED_BY_TENANT_FALLBACK.get(tenant_id, frozenset())
    return pack_id in licensed
  return tenant_config_store.is_pack_entitled(
    sess,
    tenant_id=tenant_id,
    pack_id=pack_id,
  )


def assert_pack_licensed(
  session: Session | None = None,
  *,
  tenant_id: str,
  pack_id: str,
) -> None:
  """未授权 Pack 时抛出 MODULE_NOT_LICENSED（403）。

  功能：execution 写路径前强制门禁（须 connector 已配置之后调用）。
  业务含义：T-02 负向断言真源。
  """
  if is_pack_licensed(session, tenant_id=tenant_id, pack_id=pack_id):
    return
  raise PlatformError(
    ErrorCode.MODULE_NOT_LICENSED,
    f"Pack {pack_id} not licensed for tenant {tenant_id}",
    http_status=403,
  )
