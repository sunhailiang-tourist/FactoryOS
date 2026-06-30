"""reconciliation_service 包入口。

作用：对账 Job 公开 API。
业务关联：K-01/K-02 · W6 stub。
上游：server/api reconciliation 路由（Step4）
下游：mock_legacy read-back · execution 账本
"""
from __future__ import annotations

from os_core.reconciliation_service.service import run_reconciliation

__all__ = ["run_reconciliation"]
