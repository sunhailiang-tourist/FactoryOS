# Gate 结论：`gate-step_harness-full_step4`

- 时间(UTC): 2026-06-30T05:10:29Z → 2026-06-30T05:10:29Z
- exit_code: 1
- cmd: `/opt/homebrew/opt/python@3.14/bin/python3.14 /Users/sunhailiang/hasen-project/FactoryOS/scripts/check_harness.py --tier full --pytest H-03`

## stdout
```text
OpenAPI schema refs OK (14 files)
CMV OK: 8 verbs @ CMV注册表.yaml
Import boundaries OK
OK: kernel registry aligned (10 modules)
OK: router registry aligned (10 providers)
OK: integration registry aligned
FactoryOS Harness · full · step stop / CI · 11 check(s)

── OpenAPI schema refs (check_openapi_schema_refs.py)

── CMV sync (check_cmv_sync.py)

── Import boundaries (check_import_boundaries.py)

── os_core kernel registry (check_kernel_registry.py)

── api router registry (check_router_registry.py)

── integration GIP registry (check_integration_registry.py)

── legacy path cleanup (check_legacy_paths.py)
```

## stderr
```text
FAIL: PyYAML required — run: uv run python scripts/...

Harness FAILED at legacy path cleanup
```
