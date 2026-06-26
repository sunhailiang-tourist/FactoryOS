"""audit_service 包入口。

作用：append-only 审计；对外暴露 store 公开 API。
业务关联：W2 Step1 内核；execution 写路径须落审计（E-03）。
上游：execution_service、server/api
下游：audit_events 表
关联文档：src/server/os_core/audit_service/README.md
"""
from __future__ import annotations

from os_core.audit_service.store import append_audit_event, list_audit_events

__all__ = ["append_audit_event", "list_audit_events"]
