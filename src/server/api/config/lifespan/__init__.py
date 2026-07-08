"""config/lifespan 包。

作用：FastAPI lifespan 上下文管理命名空间。
业务关联：启动 bootstrap · 关停清理。
上游：application/factory lifespan 参数。
下游：platform_registry.bootstrap · os_core.registry.init_kernel。
"""
