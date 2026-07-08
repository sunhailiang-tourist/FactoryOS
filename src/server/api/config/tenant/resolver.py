"""租户 ID 解析辅助。

作用：从 Request 提取 tenant_id（与 middleware 对齐）。
业务关联：非 Depends 场景复用。
上游：tenant/middleware request.state。
下游：quota · audit 过滤。
"""
from __future__ import annotations
