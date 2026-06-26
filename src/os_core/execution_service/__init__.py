"""execution_service 包入口。

作用：对外暴露 execute 公开 API。
业务关联：W2 写路径唯一入口。
上游：apps/api
下游：audit_service · connector_sdk
"""
from __future__ import annotations

from os_core.execution_service.service import assemble_evidence, execute

__all__ = ["assemble_evidence", "execute"]
