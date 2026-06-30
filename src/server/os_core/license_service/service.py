"""license_service：Pack 授权 stub（W6 Step1 · 静态 licensed 列表）。

作用：assert_pack_licensed 供 execution 前门禁。
业务关联：T-02 MODULE_NOT_LICENSED · BASE-001。
上游：execution_service（Step2）
下游：shared_contracts PlatformError
关联文档：src/server/os_core/license_service/README.md · ADR-003
"""
from __future__ import annotations

from os_core.shared_contracts.errors import ErrorCode
from os_core.shared_contracts.exceptions import PlatformError

# tenant_id → 已授权 Pack ID（W6 stub；W7+ 读 integration/tenants）
_LICENSED_BY_TENANT: dict[str, frozenset[str]] = {
  "default": frozenset({"conn-mock"}),
}


def is_pack_licensed(*, tenant_id: str, pack_id: str) -> bool:
  """判断 tenant 是否授权 pack_id。

  功能：只读校验，不抛异常。
  业务含义：Harness / 编排层可预检。
  参数 tenant_id：租户 ID
  参数 pack_id：Connector Pack ID（如 conn-mock）
  返回：True 表示已授权
  """
  licensed = _LICENSED_BY_TENANT.get(tenant_id, frozenset())
  return pack_id in licensed


def assert_pack_licensed(*, tenant_id: str, pack_id: str) -> None:
  """未授权 Pack 时抛出 MODULE_NOT_LICENSED（403）。

  功能：execution 写路径前强制门禁。
  业务含义：T-02 负向断言真源。
  上游：execution_service.execute（Step2）
  参数 tenant_id/pack_id：同 is_pack_licensed
  """
  if is_pack_licensed(tenant_id=tenant_id, pack_id=pack_id):
    return
  raise PlatformError(
    ErrorCode.MODULE_NOT_LICENSED,
    f"Pack {pack_id} not licensed for tenant {tenant_id}",
    http_status=403,
  )
