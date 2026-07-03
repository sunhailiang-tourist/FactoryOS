# Gate 结论：`gate-pr_deptry`

- 时间(UTC): 2026-06-29T10:00:08Z → 2026-06-29T10:00:08Z
- exit_code: 0
- cmd: `/Users/sunhailiang/hasen-project/FactoryOS/.venv/bin/python3 /Users/sunhailiang/hasen-project/FactoryOS/scripts/check_deptry.py`

## stdout
```text

── deptry (DEP001 · declared imports)
  $ /Users/sunhailiang/hasen-project/FactoryOS/.venv/bin/python3 -m deptry src/server src/tests --ignore DEP002,DEP003,DEP004,DEP005 --optional-dependencies-dev-groups dev
deptry OK
```

## stderr
```text
Scanning 169 files...

[1m[32mSuccess! No dependency issues found.[m
```
