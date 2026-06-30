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
  """保存计划（未确认前禁止 execution 写 Legacy）。"""
  _PLANS[plan.plan_id] = plan


def get_plan(plan_id: UUID) -> DslPlan | None:
  """按 plan_id 读取；不存在返回 None。"""
  return _PLANS.get(plan_id)


def clear_plans() -> None:
  """测试夹具清空（非生产 API）。"""
  _PLANS.clear()
