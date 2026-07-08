"""Auth FastAPI Depends。

作用：get_current_actor 等依赖注入。
业务关联：RBAC · Actor 上下文。
上游：auth/middleware request.state。
下游：modules/*/controllers Depends。
"""
