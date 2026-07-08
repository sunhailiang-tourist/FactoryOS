"""FastAPI lifespan hooks。

作用：startup/shutdown 编排内核与 Registry 初始化。
业务关联：进程生命周期与 DB 连接池。
上游：factory.create_app lifespan。
下游：platform_registry · os_core.registry.init_kernel。
"""
from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from os_core.registry import init_kernel


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
  """FastAPI lifespan 上下文（startup/shutdown）。

  功能：启动时 bootstrap Registry 与内核 hook。
  业务含义：进程生命周期与连接池管理。
  上游：factory.create_app lifespan 参数。
  下游：platform_registry.bootstrap · init_kernel。
  """
  init_kernel()
  yield
