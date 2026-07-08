"""config/dependencies 包。

作用：FastAPI Depends 注入集合（DB · Registry session）。
业务关联：controllers 禁止自建 Session。
上游：settings/loader · platform_registry。
下游：modules/*/controllers Depends(get_db_session)。
"""
