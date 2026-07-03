# Gate 结论：`gate-pr_pytest`

- 时间(UTC): 2026-06-30T07:12:36Z → 2026-06-30T07:12:52Z
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
collecting ... collected 34 items

src/tests/contract/test_openapi_contract.py::test_openapi_file_exists PASSED [  2%]
src/tests/contract/test_openapi_contract.py::test_openapi_has_v1_paths PASSED [  5%]
src/tests/contract/test_openapi_contract.py::test_openapi_w5_agent_harness_paths PASSED [  8%]
src/tests/contract/test_openapi_contract.py::test_harness_contracts_tier_green PASSED [ 11%]
src/tests/contract/test_openapi_contract.py::test_gate_plan_script_exists PASSED [ 14%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-ExecutionRecord] PASSED [ 17%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-AuditEvent] PASSED [ 20%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-DslPlan] PASSED [ 23%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-BusinessGraph] PASSED [ 26%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-RuleSet] PASSED [ 29%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-DomainEvent] PASSED [ 32%]
src/tests/contract/test_shared_contracts.py::test_shared_contract_model_required_fields_match_schema[contract-ExecutionEvidence] PASSED [ 35%]
src/tests/workflow/test_api_health.py::test_health_endpoint_returns_200 PASSED [ 38%]
src/tests/workflow/test_plan_gate_absolute.py::test_plan_gate_lib_validate_detects_missing_plan_ok PASSED [ 41%]
src/tests/workflow/test_plan_gate_absolute.py::test_check_pipeline_step_enforces_plan_absolute_gate PASSED [ 44%]
src/tests/workflow/test_plan_gate_absolute.py::test_workflow_state_documents_plan_absolute_gate PASSED [ 47%]
src/tests/workflow/test_redlines_static.py::test_import_boundaries_script_passes PASSED [ 50%]
src/tests/workflow/test_redlines_static.py::test_workflow_state_template_exists PASSED [ 52%]
src/tests/workflow/test_registry_harness.py::test_kernel_registry_harness_green PASSED [ 55%]
src/tests/workflow/test_registry_harness.py::test_router_registry_harness_green PASSED [ 58%]
src/tests/workflow/test_registry_harness.py::test_main_has_no_include_router PASSED [ 61%]
src/tests/workflow/test_registry_harness.py::test_os_core_registry_lists_kernel_modules PASSED [ 64%]
src/tests/workflow/test_registry_harness.py::test_integration_registry_harness_green PASSED [ 67%]
src/tests/workflow/test_registry_harness.py::test_legacy_paths_harness_green PASSED [ 70%]
src/tests/workflow/test_registry_harness.py::test_repo_structure_harness_green PASSED [ 73%]
src/tests/workflow/test_registry_harness.py::test_path_consistency_harness_green PASSED [ 76%]
src/tests/workflow/test_registry_harness.py::test_structure_change_gate_green PASSED [ 79%]
src/tests/workflow/test_step_chain_gate.py::test_step_chain_requires_dev_before_test PASSED [ 82%]
src/tests/workflow/test_step_chain_gate.py::test_step_chain_closed_needs_all_three_artifacts PASSED [ 85%]
src/tests/workflow/test_step_chain_gate.py::test_can_start_step2_blocked_without_step1_chain PASSED [ 88%]
src/tests/workflow/test_step_chain_gate.py::test_check_pipeline_step_uses_plan_scoped_chain PASSED [ 91%]
src/tests/workflow/test_step_chain_gate.py::test_workflow_state_documents_step_chain_gate PASSED [ 94%]
src/tests/workflow/test_structure_commit_gate.py::test_staged_paths_ignore_os_core_root_files_via_script PASSED [ 97%]
src/tests/workflow/test_structure_commit_gate.py::test_structure_check_manual_mode_green PASSED [100%]

============================= 34 passed in 15.07s ==============================
```

## stderr
```text

```
