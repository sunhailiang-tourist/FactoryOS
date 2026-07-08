"""modules/rulesets 包根。

作用：RuleSets 域 HTTP 模块命名空间与 get_routers 导出。
业务关联：R-01～R-05 规则集 CRUD · evaluate。
上游：router/v1/registry · ROUTER_PROVIDERS。
下游：controllers · os_core.rule_engine。
"""
from server.api.modules.rulesets.routers import get_routers

__all__ = ["get_routers"]
