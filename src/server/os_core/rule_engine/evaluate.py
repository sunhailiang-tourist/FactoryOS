"""Rule 匹配引擎（纯函数 · 无 I/O）。

作用：evaluate 核心；deny 优先于 allow（R-03）。
业务关联：R-01 默认 deny · R-02 allow 通过。
上游：rule_engine.service
下游：RuleEvaluateResponse
"""
from __future__ import annotations

from os_core.shared_contracts.models.common import Actor
from os_core.shared_contracts.models.rule import Rule, RuleEffect, RuleSet


def _subject_matches(rule: Rule, actor: Actor) -> bool:
  """匹配 role:xxx 主体。"""
  role_tag = f"role:{actor.role}"
  return role_tag in rule.subjects or actor.user_id in rule.subjects


def _action_matches(rule: Rule, verb: str) -> bool:
  """动词是否在 rule.actions。"""
  return verb in rule.actions


def evaluate_ruleset(
  ruleset: RuleSet,
  *,
  verb: str,
  actor: Actor,
) -> tuple[RuleEffect, str | None]:
  """评估 RuleSet，返回 (effect, matched_rule_id)。

  功能：deny 规则优先于 allow（R-03）。
  业务含义：无匹配时用 default_effect（R-01 默认 deny）。
  """
  matched_allow: str | None = None
  sorted_rules = sorted(ruleset.rules, key=lambda r: r.priority, reverse=True)
  for rule in sorted_rules:
    if not _subject_matches(rule, actor) or not _action_matches(rule, verb):
      continue
    if rule.effect == RuleEffect.DENY:
      return RuleEffect.DENY, rule.id
    if rule.effect == RuleEffect.ALLOW and matched_allow is None:
      matched_allow = rule.id
  if matched_allow is not None:
    return RuleEffect.ALLOW, matched_allow
  return ruleset.default_effect, None
