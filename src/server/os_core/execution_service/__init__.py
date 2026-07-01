"""execution_service 包入口。

作用：对外暴露 execute 公开 API。
业务关联：W2 写路径唯一入口。
上游：server/api
下游：audit_service · connector_sdk
"""
from __future__ import annotations

from os_core.execution_service.service import (
  assemble_evidence,
  assemble_evidence_for_tenant,
  execute,
  get_execution_for_tenant,
  revert_execution,
)

__all__ = [
  "assemble_evidence",
  "assemble_evidence_for_tenant",
  "execute",
  "get_execution_for_tenant",
  "revert_execution",
]
