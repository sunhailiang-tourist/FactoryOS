"""connector_sdk · 连接器 SDK 包根。

作用：Legacy 读写适配、Blueprint Runtime、健康检查公开面。
业务关联：唯一写 Legacy 经 execution_service 调用本包 write（W4+）。
上游：execution_service、apps/api 路由
下游：Legacy HTTP、integration/catalog Blueprint
关联文档：src/os_core/connector_sdk/README.md
"""
from os_core.connector_sdk.health import (
  ConnectorHealthResponse,
  check_connector_health,
)
from os_core.connector_sdk.registry import load_blueprint, validate_blueprint

__all__ = [
  "ConnectorHealthResponse",
  "check_connector_health",
  "load_blueprint",
  "validate_blueprint",
]

