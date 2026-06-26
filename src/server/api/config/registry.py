"""config 横切注册唯一入口。"""
from __future__ import annotations

from fastapi import FastAPI
from server.api.config.logs import configure as logs_configure
from server.api.config.middleware.registry import register as register_middleware
from server.api.config.settings.loader import init as init_settings
from server.api.config.status_code.handlers import platform_error_handler

from os_core.shared_contracts.exceptions import PlatformError


def register_config(app: FastAPI) -> None:
  """注册 settings · logs · status_code · middleware。"""
  init_settings()
  logs_configure.init()
  app.add_exception_handler(PlatformError, platform_error_handler)  # type: ignore[arg-type]
  register_middleware(app)
