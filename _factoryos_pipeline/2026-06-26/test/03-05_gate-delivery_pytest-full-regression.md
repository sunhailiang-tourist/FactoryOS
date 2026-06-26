# Gate 结论：`gate-delivery_pytest-full-regression`

- 时间(UTC): 2026-06-26T03:05:23Z → 2026-06-26T03:05:24Z
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
collecting ... collected 25 items

src/tests/contract/test_openapi_contract.py::test_openapi_file_exists PASSED [  4%]
src/tests/contract/test_openapi_contract.py::test_openapi_has_v1_paths PASSED [  8%]
src/tests/contract/test_openapi_contract.py::test_harness_contracts_tier_green PASSED [ 12%]
src/tests/contract/test_openapi_contract.py::test_gate_plan_script_exists PASSED [ 16%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-ExecutionRecord] PASSED [ 20%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-AuditEvent] PASSED [ 24%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-DslPlan] PASSED [ 28%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-BusinessGraph] PASSED [ 32%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-RuleSet] PASSED [ 36%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-DomainEvent] PASSED [ 40%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-ExecutionEvidence] PASSED [ 44%]
src/tests/workflow/test_api_health.py::test_health_endpoint_returns_200 PASSED [ 48%]
src/tests/workflow/test_redlines_static.py::test_import_boundaries_script_passes PASSED [ 52%]
src/tests/workflow/test_redlines_static.py::test_workflow_state_template_exists PASSED [ 56%]
src/tests/integration/test_audit_e03.py::test_w2_audit_execution_migration_tables PASSED [ 60%]
src/tests/integration/test_audit_e03.py::test_E03_audit_events_after_execute[E-03] PASSED [ 64%]
src/tests/integration/test_audit_e03.py::test_audit_service_append_only_kernel PASSED [ 68%]
src/tests/integration/test_connector_c01.py::test_C01_connector_health_returns_ok[C-01] PASSED [ 72%]
src/tests/integration/test_execution_e06_e07.py::test_E06_dry_run_does_not_write_legacy[E-06] PASSED [ 76%]
src/tests/integration/test_execution_e06_e07.py::test_E07_idempotency_key_no_duplicate_write[E-07] PASSED [ 80%]
src/tests/integration/test_execution_e09.py::test_E09_execution_evidence_rebuildable[E-09] PASSED [ 84%]
src/tests/integration/test_scale_s01_s04.py::test_S01_scale_tables_after_migration[S-01] PASSED [ 88%]
src/tests/integration/test_scale_s01_s04.py::test_S02_default_tenant_seed_values[S-02] PASSED [ 92%]
src/tests/integration/test_scale_s01_s04.py::test_S03_tenant_registry_get_cell[S-03] PASSED [ 96%]
src/tests/integration/test_scale_s01_s04.py::test_S04_outbox_port_persists_event[S-04] PASSED [100%]

=============================== warnings summary ===============================
.venv/lib/python3.12/site-packages/fastapi/testclient.py:1
  /Users/sunhailiang/hasen-project/FactoryOS/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================== 25 passed, 1 warning in 0.75s =========================
```

## stderr
```text

```
