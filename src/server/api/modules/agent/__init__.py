"""modules/agent 包根。

作用：Agent 域 HTTP 模块命名空间与 get_routers 导出。
业务关联：H-01 意图→DslPlan（不写 Legacy）。
上游：router/v1/registry · ROUTER_PROVIDERS。
下游：controllers · os_core.agent_orchestrator。
"""
from server.api.modules.agent.routers import get_routers

__all__ = ["get_routers"]
