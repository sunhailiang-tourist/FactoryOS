"""业务域 HTTP 模块包（api/modules）。

作用：OpenAPI /v1/* 各域 HTTP 适配实现根命名空间。
业务关联：薄路由层；业务规则在 os_core。
上游：router/v1/registry · HTTP 客户端。
下游：modules/*/controllers · os_core/*/service。
"""
