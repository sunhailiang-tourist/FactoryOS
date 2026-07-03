# Gate 结论：`gate-pr_pytest`

- 时间(UTC): 2026-06-26T14:17:16Z → 2026-06-26T14:17:17Z
- exit_code: 0
- cmd: `/Users/sunhailiang/hasen-project/FactoryOS/.venv/bin/python3 -m pytest src/tests/contract src/tests/workflow -v --tb=short`

## stdout
```text
============================= test session starts ==============================
platform darwin -- Python 3.12.13, pytest-9.1.1, pluggy-1.6.0 -- /Users/sunhailiang/hasen-project/FactoryOS/.venv/bin/python3
cachedir: .pytest_cache
rootdir: /Users/sunhailiang/hasen-project/FactoryOS
configfile: pyproject.toml
plugins: anyio-4.14.0, asyncio-1.4.0
asyncio: mode=Mode.AUTO, debug=False, asyncio_default_fixture_loop_scope=None, asyncio_default_test_loop_scope=function
collecting ... collected 28 items

src/tests/contract/test_openapi_contract.py::test_openapi_file_exists PASSED [  3%]
src/tests/contract/test_openapi_contract.py::test_openapi_has_v1_paths PASSED [  7%]
src/tests/contract/test_openapi_contract.py::test_harness_contracts_tier_green PASSED [ 10%]
src/tests/contract/test_openapi_contract.py::test_gate_plan_script_exists PASSED [ 14%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-ExecutionRecord] PASSED [ 17%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-AuditEvent] PASSED [ 21%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-DslPlan] PASSED [ 25%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-BusinessGraph] PASSED [ 28%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-RuleSet] PASSED [ 32%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-DomainEvent] PASSED [ 35%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-ExecutionEvidence] PASSED [ 39%]
src/tests/workflow/test_api_health.py::test_health_endpoint_returns_200 PASSED [ 42%]
src/tests/workflow/test_plan_gate_absolute.py::test_plan_gate_lib_validate_detects_missing_plan_ok PASSED [ 46%]
src/tests/workflow/test_plan_gate_absolute.py::test_check_pipeline_step_enforces_plan_absolute_gate PASSED [ 50%]
src/tests/workflow/test_plan_gate_absolute.py::test_workflow_state_documents_plan_absolute_gate PASSED [ 53%]
src/tests/workflow/test_redlines_static.py::test_import_boundaries_script_passes PASSED [ 57%]
src/tests/workflow/test_redlines_static.py::test_workflow_state_template_exists PASSED [ 60%]
src/tests/workflow/test_registry_harness.py::test_kernel_registry_harness_green PASSED [ 64%]
src/tests/workflow/test_registry_harness.py::test_router_registry_harness_green PASSED [ 67%]
src/tests/workflow/test_registry_harness.py::test_main_has_no_include_router PASSED [ 71%]
src/tests/workflow/test_registry_harness.py::test_os_core_registry_lists_ten_modules PASSED [ 75%]
src/tests/workflow/test_registry_harness.py::test_integration_registry_harness_green PASSED [ 78%]
src/tests/workflow/test_registry_harness.py::test_legacy_paths_harness_green PASSED [ 82%]
src/tests/workflow/test_step_chain_gate.py::test_step_chain_requires_dev_before_test PASSED [ 85%]
src/tests/workflow/test_step_chain_gate.py::test_step_chain_closed_needs_all_three_artifacts PASSED [ 89%]
src/tests/workflow/test_step_chain_gate.py::test_can_start_step2_blocked_without_step1_chain PASSED [ 92%]
src/tests/workflow/test_step_chain_gate.py::test_check_pipeline_step_uses_plan_scoped_chain PASSED [ 96%]
src/tests/workflow/test_step_chain_gate.py::test_workflow_state_documents_step_chain_gate PASSED [100%]

=============================== warnings summary ===============================
.venv/lib/python3.12/site-packages/fastapi/testclient.py:1
  /Users/sunhailiang/hasen-project/FactoryOS/.venv/lib/python3.12/site-packages/fastapi/testclient.py:1: StarletteDeprecationWarning: Using `httpx` with `starlette.testclient` is deprecated; install `httpx2` instead.
    from starlette.testclient import TestClient as TestClient  # noqa

-- Docs: https://docs.pytest.org/en/stable/how-to/capture-warnings.html
======================== 28 passed, 1 warning in 0.82s =========================
```

## stderr
```text

```
