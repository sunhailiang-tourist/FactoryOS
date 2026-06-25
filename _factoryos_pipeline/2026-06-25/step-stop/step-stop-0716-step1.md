# Step 停机：Step 1 — 工程底座与 import 边界

- **plan**：`_factoryos_pipeline/2026-06-25/plan/plan-0116-w1-base.md`
- **时间**：2026-06-25 15:16（本地）

## 1. Step 标识

Step 1 — 工程底座与 import 边界（Control Plane CI 就绪）

## 2. 改动文件

| 路径 | 变更 |
|------|------|
| `pyproject.toml` · `uv.lock` | + fastapi · uvicorn[standard] · sqlalchemy · alembic · aiosqlite |
| `src/apps/__init__.py` | 新增 |
| `src/apps/api/__init__.py` | 新增 |
| `src/apps/api/main.py` | `create_app()` + `GET /health` |
| `src/apps/api/README.md` | 本地开发命令更新 |
| `src/tests/workflow/test_api_health.py` | httpx→TestClient（httpx 0.28 ASGI 兼容） |
| `src/tests/integration/test_connector_c01.py` | 同上（Step4 前置，消除 pyright 红） |
| `src/tests/conftest.py` | 移除未使用 Session import（ruff） |

## 3. AC / 接口

| AC ID | 接口 | 结果 |
|-------|------|------|
| workflow | `GET /health` | PASS（200, status=ok） |
| workflow | import_boundaries | PASS |

## 4. 十项自检（Pass/Fail）

| # | 项 | 结果 |
|---|-----|------|
| 1 | 分层/写路径 | Pass — api 仅探针，无 os_core 业务 |
| 2 | 响应契约 | Pass — health JSON `{"status":"ok"}` |
| 3 | 鉴权/租户 | Pass — W1 探针无鉴权（符合 plan） |
| 4 | 红线 | Pass — 无 Legacy 写 |
| 5 | Schema | N/A — 本 Step 无新 Schema |
| 6 | 输入校验 | N/A |
| 7 | Shadow | N/A |
| 8 | 幂等/补偿 | N/A |
| 9 | 静态检查 | Pass — ruff + pyright 绿 |
| 10 | 注释 | Pass — main.py 文件头 + 函数 docstring |

## 5. Harness 结果

```bash
.venv/bin/python scripts/gate_cli.py step --step 1 -k 'workflow'
```

```text
harness full + pytest -k workflow : PASS（5 passed）
static quality : PASS
verify : MISSING（待独立 Verify 回合）
gate step : 未全绿（缺 verify 落盘）
```

## 6. 最短验证路径

```bash
uv sync --extra dev
uv run pytest src/tests/workflow/ -k workflow -v
curl -s http://127.0.0.1:8000/health   # 需 uvicorn apps.api.main:app
```

## 7. Verify（必填）

- 落盘：`verify/verify-<HHmm>-step1.md`（**新对话**）
- 口令：`【Verify回合】Step 1`
- 结论：待审阅

## 8. 等待

Verify 落盘且 `gate step` 全绿后，请回复：`可以继续` 或 `测试不通过` + 现象
