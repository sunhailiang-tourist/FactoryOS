"""apps · 应用层包根。

作用：承载 HTTP API 与前端应用目录。
业务关联：Modular Monolith 对外入口；内核逻辑在 os_core。
上游：部署编排（Uvicorn / 静态托管）
下游：os_core 各 service 公开 API
关联文档：src/apps/README.md
"""
