# alembic · 数据库迁移真源

本目录为 **PostgreSQL / SQLite 表结构演进** 的机器执行真源；与 `contracts/schemas`、Pydantic 模型字段须保持一致。

| 路径 | 内容 |
|------|------|
| `env.py` | Alembic 运行环境；支持 SQLite `:memory:` 与 pytest 共享连接 |
| `versions/` | 按时间序 revision；W1 起 `001_scale_s01_s04`（S-01～S-04） |
| `script.py.mako` | 新 revision 模板 |
| `../alembic.ini` | 入口配置（`script_location = alembic`） |

## 门禁

```bash
uv run alembic upgrade head          # 本地 / CI 临时库
uv run pytest src/tests/integration/ -k 'S-01' -q
./scripts/gate step --step 3 -k 'S-01'
```

## 变更纪律

| 改了 | 必做 |
|------|------|
| `versions/*.py` | 同 commit 更新相关 Pydantic / 文档；禁止 Model 与 migration 分叉 |
| 新表 / 新列 | 对照 ADR-007 §15 · plan AC S-*；补 integration pytest |
| `env.py` | 确认 SQLite 测试池与 `src/tests/conftest.py` 注入一致 |

## 不负责什么

- 业务规则、租户分支逻辑（在 `os_core/*`）
- 生产连接串与密钥（环境变量 / 部署配置）

## 文档链接

- [ORM-MIGRATION-PRINCIPLE](../.cursor/factoryos/ORM-MIGRATION-PRINCIPLE.md)
- ADR-007 百级千级演进 · plan W1 Step3
