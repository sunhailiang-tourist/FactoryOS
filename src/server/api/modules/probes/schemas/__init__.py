"""modules/probes/schemas 包。

作用：Probes 域 OpenAPI DTO（Pydantic）命名空间。
业务关联：K8s 进程/就绪探针（非 OpenAPI 正式域）；与 os_core 领域模型分离。
上游：modules/probes/controllers。
下游：OpenAPI 契约 · HTTP 序列化。
"""
