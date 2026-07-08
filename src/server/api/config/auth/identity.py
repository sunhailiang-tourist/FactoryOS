"""身份解析（JWT/API Key stub）。

作用：从 Authorization 解析 Actor 身份。
业务关联：统一鉴权入口。
上游：HTTP Authorization header。
下游：auth/middleware · audit actor 字段。
"""
