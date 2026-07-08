"""ErrorCode → HTTP status 映射。

作用：PlatformError.error_code 转 HTTP 状态码。
业务关联：OpenAPI ProblemDetails 对齐。
上游：shared_contracts.errors ErrorCode。
下游：status_code/handlers。
"""
