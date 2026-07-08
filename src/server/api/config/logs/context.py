"""日志上下文（MDC）。

作用：bind/clear request 级日志字段。
业务关联：trace_id · tenant_id 关联排障。
上游：traces/auth/tenant middleware。
下游：structlog/logging 输出。
"""
from __future__ import annotations
