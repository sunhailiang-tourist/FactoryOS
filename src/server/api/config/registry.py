"""config 横切注册唯一入口。

作用：settings · logs · status_code · middleware 统一注册。
业务关联：register_config 须在 router 之前调用。
上游：application/assemble。
下游：config 各子包 · FastAPI exception_handler。
"""
from __future__ import annotations

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from server.api.config.logs import configure as logs_configure
from server.api.config.middleware.registry import register as register_middleware
from server.api.config.settings.loader import init as init_settings
from server.api.config.status_code.handlers import (
  http_exception_handler,
  platform_error_handler,
  unhandled_exception_handler,
  validation_exception_handler,
)

from os_core.shared_contracts.exceptions import PlatformError


def register_config(app: FastAPI) -> None:
  """注册 settings · logs · status_code · middleware。

  功能：横切能力统一挂载到 FastAPI app。
  业务含义：config 子系统启动真源。
  上游：assemble(app)。
  下游：middleware/registry · exception handlers。
  """
  init_settings()
  logs_configure.init()
  app.add_exception_handler(PlatformError, platform_error_handler)  # type: ignore[arg-type]
  app.add_exception_handler(HTTPException, http_exception_handler)  # type: ignore[arg-type]
  app.add_exception_handler(RequestValidationError, validation_exception_handler)  # type: ignore[arg-type]
  app.add_exception_handler(Exception, unhandled_exception_handler)
  register_middleware(app)
