# Gate 结论：`gate-delivery_pytest-full-regression`

- 时间(UTC): 2026-06-26T03:32:58Z → 2026-06-26T03:33:00Z
- exit_code: 0
- cmd: `/Users/sunhailiang/hasen-project/FactoryOS/.venv/bin/python3 -m pytest src/tests/contract src/tests/workflow src/tests/integration -v --tb=short -m not pending`

## stdout
```text
============================= test session starts ==============================
platform darwin -- Python 3.12.13, pytest-9.1.1, pluggy-1.6.0 -- /Users/sunhailiang/hasen-project/FactoryOS/.venv/bin/python3
cachedir: .pytest_cache
rootdir: /Users/sunhailiang/hasen-project/FactoryOS
configfile: pyproject.toml
plugins: anyio-4.14.0, asyncio-1.4.0
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 42 items

src/tests/contract/test_openapi_contract.py::test_openapi_file_exists PASSED [  2%]
src/tests/contract/test_openapi_contract.py::test_openapi_has_v1_paths PASSED [  4%]
src/tests/contract/test_openapi_contract.py::test_harness_contracts_tier_green PASSED [  7%]
src/tests/contract/test_openapi_contract.py::test_gate_plan_script_exists PASSED [  9%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-ExecutionRecord] PASSED [ 11%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-AuditEvent] PASSED [ 14%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-DslPlan] PASSED [ 16%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-BusinessGraph] PASSED [ 19%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-RuleSet] PASSED [ 21%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-DomainEvent] PASSED [ 23%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-ExecutionEvidence] PASSED [ 26%]
src/tests/workflow/test_api_health.py::test_health_endpoint_returns_200 PASSED [ 28%]
src/tests/workflow/test_redlines_static.py::test_import_boundaries_script_passes PASSED [ 30%]
src/tests/workflow/test_redlines_static.py::test_workflow_state_template_exists PASSED [ 33%]
src/tests/integration/test_audit_e03.py::test_w2_audit_execution_migration_tables PASSED [ 35%]
src/tests/integration/test_audit_e03.py::test_E03_audit_events_after_execute[E-03] PASSED [ 38%]
src/tests/integration/test_audit_e03.py::test_audit_service_append_only_kernel PASSED [ 40%]
src/tests/integration/test_connector_c01.py::test_C01_connector_health_returns_ok[C-01] PASSED [ 42%]
src/tests/integration/test_dsl_w3.py::test_D01_list_dsl_registry[D-01] PASSED [ 45%]
src/tests/integration/test_dsl_w3.py::test_D02_unknown_verb_rejected[D-02] PASSED [ 47%]
src/tests/integration/test_dsl_w3.py::test_D03_verb_not_in_graph_allowed_dsl[D-03] PASSED [ 50%]
src/tests/integration/test_execution_e01.py::test_E01_l0_query_on_frozen_graph[E-01] PASSED [ 52%]
src/tests/integration/test_execution_e06_e07.py::test_E06_dry_run_does_not_write_legacy[E-06] PASSED [ 54%]
src/tests/integration/test_execution_e06_e07.py::test_E07_idempotency_key_no_duplicate_write[E-07] PASSED [ 57%]
src/tests/integration/test_execution_e09.py::test_E09_execution_evidence_rebuildable[E-09] PASSED [ 59%]
src/tests/integration/test_graph_w3.py::test_G01_create_draft_graph[G-01] PASSED [ 61%]
src/tests/integration/test_graph_w3.py::test_G02_update_draft_graph[G-02] PASSED [ 64%]
src/tests/integration/test_graph_w3.py::test_G03_execute_l2_on_draft_graph_rejected[G-03] PASSED [ 66%]
src/tests/integration/test_graph_w3.py::test_G04_submit_to_in_review[G-04] PASSED [ 69%]
src/tests/integration/test_graph_w3.py::test_G05_freeze_graph_with_frozen_ruleset[G-05] PASSED [ 71%]
src/tests/integration/test_graph_w3.py::test_G06_frozen_graph_not_editable[G-06] PASSED [ 73%]
src/tests/integration/test_graph_w3.py::test_G07_clone_new_draft_version[G-07] PASSED [ 76%]
src/tests/integration/test_graph_w3.py::test_G08_execute_on_deprecated_graph_rejected[G-08] PASSED [ 78%]
src/tests/integration/test_rule_w3.py::test_R01_default_deny_no_matching_rule[R-01] PASSED [ 80%]
src/tests/integration/test_rule_w3.py::test_R02_allow_rule_passes[R-02] PASSED [ 83%]
src/tests/integration/test_rule_w3.py::test_R03_deny_priority_over_allow[R-03] PASSED [ 85%]
src/tests/integration/test_rule_w3.py::test_R04_ruleset_graph_version_mismatch[R-04] PASSED [ 88%]
src/tests/integration/test_rule_w3.py::test_R05_frozen_ruleset_not_editable[R-05] PASSED [ 90%]
src/tests/integration/test_scale_s01_s04.py::test_S01_scale_tables_after_migration[S-01] PASSED [ 92%]
src/tests/integration/test_scale_s01_s04.py::test_S02_default_tenant_seed_values[S-02] PASSED [ 95%]
src/tests/integration/test_scale_s01_s04.py::test_S03_tenant_registry_get_cell[S-03] PASSED [ 97%]
src/tests/integration/test_scale_s01_s04.py::test_S04_outbox_port_persists_event[S-04] PASSED [100%]

=============================== warnings summary ===============================
.venv/lib/python3.12/site-packages/fastapi/testclient.py:1
  /Users/sunhailiang/hasen-project/FactoryOS/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================== 42 passed, 1 warning in 1.36s =========================
```

## stderr
```text

```
