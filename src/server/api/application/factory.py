"""FastAPI 应用工厂。

作用：create_app 构建 FastAPI 实例并触发 assemble。
业务关联：api 进程唯一应用入口。
上游：main.py · pytest fixtures。
下游：application/assemble · config/lifespan。
"""
from __future__ import annotations

from fastapi import FastAPI
from server.api.application.assemble import assemble
from server.api.config.lifespan.hooks import lifespan


def create_app() -> FastAPI:
  """创建并装配 FastAPI 实例。

  功能：构建 FastAPI 并调用 assemble。
  业务含义：HTTP 进程唯一应用工厂。
  上游：main.py · pytest。
  下游：assemble · lifespan hooks。
  """
  app = FastAPI(
    title="FactoryOS API",
    version="0.1.0-w3",
    description="Manufacturing AI execution platform — Modular Monolith entry",
    lifespan=lifespan,
  )
  assemble(app)
  return app


app = create_app()
