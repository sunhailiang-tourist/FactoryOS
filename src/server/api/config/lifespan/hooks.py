"""FastAPI lifespan：startup/shutdown。"""
from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from os_core.registry import init_kernel


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
  """应用生命周期：内核 init_kernel。"""
  init_kernel()
  yield
