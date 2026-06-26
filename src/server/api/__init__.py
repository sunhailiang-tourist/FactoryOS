"""server.api · FastAPI 生产 HTTP 入口。

作用：Control Plane HTTP 薄路由层。
业务关联：W1+ 唯一 deployable API。
上游：Uvicorn
下游：os_core 各 service
关联文档：src/server/api/README.md
"""
