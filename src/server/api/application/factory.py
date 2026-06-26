"""FastAPI 应用工厂。"""
from __future__ import annotations

from fastapi import FastAPI
from server.api.application.assemble import assemble
from server.api.config.lifespan.hooks import lifespan


def create_app() -> FastAPI:
  """创建并装配 FastAPI 实例。"""
  app = FastAPI(
    title="FactoryOS API",
    version="0.1.0-w3",
    description="Manufacturing AI execution platform — Modular Monolith entry",
    lifespan=lifespan,
  )
  assemble(app)
  return app


app = create_app()
