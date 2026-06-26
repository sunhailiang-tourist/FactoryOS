"""Blueprint mapping 校验（W4 Step2 · B-03）。

作用：按 op.mapping 键检查 params 必填字段。
业务关联：缺 entity_id/fields → MAPPING_ERROR。
上游：runtime.execute
下游：PlatformError
"""
from __future__ import annotations

from typing import Any

from os_core.shared_contracts.errors import ErrorCode
from os_core.shared_contracts.exceptions import PlatformError


def validate_op_params(op: dict[str, Any], params: dict[str, Any]) -> None:
  """校验 params 覆盖 mapping 声明的字段名（B-03）。"""
  mapping = op.get("mapping") or {}
  for field_name in mapping:
    if field_name not in params or params[field_name] is None:
      raise PlatformError(
        ErrorCode.MAPPING_ERROR,
        f"Missing mapping field: {field_name}",
        http_status=422,
      )
