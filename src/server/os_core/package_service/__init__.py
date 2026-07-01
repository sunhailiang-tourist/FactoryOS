"""package_service 公开 API（REST · MCP 共用 export/import）。"""
from os_core.package_service.service import (
  export_implementation_package,
  import_implementation_package,
)

__all__ = ["export_implementation_package", "import_implementation_package"]
