"""config/status_code 包。

作用：PlatformError → HTTP 响应映射命名空间。
业务关联：统一错误 JSON 契约。
上游：config/registry exception_handler 注册。
下游：status_code/handlers · mapping。
"""
