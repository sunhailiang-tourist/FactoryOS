"""apps.api · FastAPI 生产 HTTP 入口。

作用：路由装配、依赖注入、请求校验（无业务规则）。
业务关联：对齐 contracts/openapi v1.1.1。
上游：web-admin、h5-worker、第三方集成
下游：os_core/* public API
关联文档：src/apps/api/README.md
"""
