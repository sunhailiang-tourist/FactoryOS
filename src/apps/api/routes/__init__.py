"""apps.api.routes · OpenAPI 域路由包。

作用：按域拆分 FastAPI 路由；仅 DI 与校验，无业务规则。
业务关联：对齐 contracts/openapi v1.1.1。
上游：apps/api/main.py create_app
下游：os_core 各模块公开 API
关联文档：apps/api/README.md
"""
