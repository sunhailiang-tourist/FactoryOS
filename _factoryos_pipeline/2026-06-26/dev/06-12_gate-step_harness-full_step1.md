# Gate 结论：`gate-step_harness-full_step1`

- 时间(UTC): 2026-06-26T06:12:54Z → 2026-06-26T06:12:54Z
- exit_code: 1
- cmd: `/opt/homebrew/opt/python@3.14/bin/python3.14 /Users/sunhailiang/hasen-project/FactoryOS/scripts/check_harness.py --tier full --pytest B-01`

## stdout
```text
OpenAPI schema refs OK (14 files)
CMV OK: 8 verbs @ CMV注册表.yaml
Import boundaries OK
Code redundancy check OK
FactoryOS Harness · full · step stop / CI · 4 check(s)

── OpenAPI schema refs (check_openapi_schema_refs.py)

── CMV sync (check_cmv_sync.py)

── Import boundaries (check_import_boundaries.py)

── Code redundancy (check_code_redundancy.py)

── pytest -k 'B-01'
```

## stderr
```text
/opt/homebrew/opt/python@3.14/bin/python3.14: No module named pytest

Harness FAILED at pytest
```
