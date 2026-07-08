"""DslPlan 进程内暂存（W5 Step1 · 确认前不落 execution）。

作用：plan_id → DslPlan 映射；Step2 HTTP 与 Step3 harness 共用。
业务关联：H-01 plan 阶段 · H-02 confirm 读取 plan。
上游：agent_orchestrator.service.create_plan
下游：harness.confirm（Step3）
关联文档：contracts/schemas/DslPlan.schema.json
"""
from __future__ import annotations

from uuid import UUID

from os_core.shared_contracts.models.dsl import DslPlan

# plan_id → DslPlan（单进程测试/开发；生产 W6+ 可换 DB 表）
_PLANS: dict[UUID, DslPlan] = {}


def save_plan(plan: DslPlan) -> None:
  """保存 DslPlan 至进程内暂存。

  功能：plan_id → DslPlan 映射写入 _PLANS。
  业务含义：H-01 plan 阶段；confirm 前禁止 execution 写 Legacy。
  参数 plan：含 plan_id · verb · graph 绑定的 DSL 计划。
  上游：agent_orchestrator.create_plan。
  下游：get_plan · harness confirm（Step3）。
  """
  _PLANS[plan.plan_id] = plan


def get_plan(plan_id: UUID) -> DslPlan | None:
  """按 plan_id 读取暂存计划。

  功能：查询 _PLANS 字典。
  业务含义：confirm 步加载 plan 转 ExecuteRequest。
  参数 plan_id：计划 UUID。
  返回：DslPlan 或 None。
  """
  return _PLANS.get(plan_id)


def clear_plans() -> None:
  """清空进程内全部暂存计划。

  功能：_PLANS.clear()。
  业务含义：pytest fixture teardown；非生产 API。
  上游：测试 harness。
  """
  _PLANS.clear()
