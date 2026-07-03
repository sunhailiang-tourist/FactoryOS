# Gate 结论：`gate-pr_deptry`

- 时间(UTC): 2026-06-30T03:28:01Z → 2026-06-30T03:28:01Z
- exit_code: 1
- cmd: `/Users/sunhailiang/hasen-project/FactoryOS/.venv/bin/python3 /Users/sunhailiang/hasen-project/FactoryOS/scripts/check_deptry.py`

## stdout
```text

── deptry (DEP001 · declared imports)
  $ /Users/sunhailiang/hasen-project/FactoryOS/.venv/bin/python3 -m deptry src/server src/tests --ignore DEP002,DEP003,DEP004,DEP005 --optional-dependencies-dev-groups dev
```

## stderr
```text
Scanning 170 files...

[1msrc/tests/workflow/test_structure_commit_gate.py[m[36m:[m13[36m:[m10[36m:[m [1m[31mDEP001[m 'repo_structure' imported but missing from the dependency definitions
[1m[31mFound 1 dependency issue.[m

For more information, see the documentation: https://deptry.com/

deptry FAILED — declare deps with: uv add <pkg>  or  uv add --dev <pkg>
```
