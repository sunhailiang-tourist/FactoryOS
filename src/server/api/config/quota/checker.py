"""配额检查器。

作用：按 tenant 扣减/校验 API 配额。
业务关联：多租户公平使用。
上游：quota/middleware · tenant_id。
下游：429 Too Many Requests。
"""
