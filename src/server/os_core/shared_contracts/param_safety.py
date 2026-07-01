"""执行参数安全校验（N-04 · SQL injection 拒绝）。

作用：execute 前扫描 params 字符串，拒绝明显 SQL 注入模式。
业务关联：BASE-001 N-04 · 参数无害化第一道门禁。
上游：execution_service.execute
下游：PlatformError → HTTP 422
"""
from __future__ import annotations

import re
from typing import Any

from os_core.shared_contracts.errors import ErrorCode
from os_core.shared_contracts.exceptions import PlatformError

_SQL_INJECTION_PATTERNS: tuple[re.Pattern[str], ...] = (
  re.compile(r"';"),
  re.compile(r"--"),
  re.compile(r"(?i)\bdrop\s+table\b"),
  re.compile(r"(?i);\s*(drop|delete|insert|update)\b"),
)


def assert_params_safe(params: dict[str, Any] | None) -> None:
  """递归校验 params；命中 SQL 注入模式 → 422。

  功能：拒绝含 `';` · `--` · DROP TABLE 等模式的字符串值。
  业务含义：ORM 绑定仍须输入层防御；N-04 负向 AC 真源。
  """
  if not params:
    return
  _walk_params("", params)


def _walk_params(prefix: str, value: Any) -> None:
  if isinstance(value, str):
    for pattern in _SQL_INJECTION_PATTERNS:
      if pattern.search(value):
        field = prefix or "params"
        raise PlatformError(
          ErrorCode.MAPPING_ERROR,
          f"Unsafe param value rejected: {field}",
          http_status=422,
        )
    return
  if isinstance(value, dict):
    for key, nested in value.items():
      path = f"{prefix}.{key}" if prefix else str(key)
      _walk_params(path, nested)
    return
  if isinstance(value, list):
    for idx, item in enumerate(value):
      path = f"{prefix}[{idx}]"
      _walk_params(path, item)
