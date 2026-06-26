"""Blueprint Runtime op 执行（W4 Step2 · B-02/B-03）。

作用：按 catalog op 执行 CMV verb；GOVERNED_WRITE → entity update。
业务关联：B-02 legacy_refs · B-03 mapping 负向。
上游：registry.load_blueprint
下游：runtime.entity · mock_legacy
"""
from __future__ import annotations

from typing import Any

from os_core.connector_sdk.registry import load_blueprint
from os_core.connector_sdk.runtime.entity import entity_update
from os_core.connector_sdk.runtime.mapping import validate_op_params
from os_core.shared_contracts.errors import ErrorCode
from os_core.shared_contracts.exceptions import PlatformError


def _find_op(blueprint: dict[str, Any], verb: str) -> dict[str, Any]:
  ops = (blueprint.get("spec") or {}).get("ops") or []
  for op in ops:
    if isinstance(op, dict) and op.get("verb") == verb:
      return op
  raise PlatformError(
    ErrorCode.CONNECTOR_NOT_CONFIGURED,
    f"No blueprint op for verb={verb}",
    http_status=403,
  )


def execute_op(
  *,
  pack_id: str,
  tenant_id: str,
  verb: str,
  params: dict[str, Any],
  idempotency_key: str | None = None,
) -> dict[str, Any]:
  """执行 Blueprint op（B-02 · B-03）。"""
  blueprint = load_blueprint(pack_id=pack_id, tenant_id=tenant_id)
  op = _find_op(blueprint, verb)
  validate_op_params(op, params)

  if verb == "GOVERNED_WRITE":
    return entity_update(
      pack_id=pack_id,
      tenant_id=tenant_id,
      entity_type=str(params["entity_type"]),
      entity_id=str(params["entity_id"]),
      fields=dict(params["fields"]),
      idempotency_key=idempotency_key,
    )

  raise PlatformError(
    ErrorCode.CONNECTOR_NOT_CONFIGURED,
    f"Runtime execute not implemented for verb={verb}",
    http_status=501,
  )
