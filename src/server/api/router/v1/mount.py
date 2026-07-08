"""v1 路由挂载辅助。

作用：include_router 封装与前缀策略。
业务关联：保持 v1 路径一致性。
上游：router/v1/registry。
下游：FastAPI app.include_router。
"""
