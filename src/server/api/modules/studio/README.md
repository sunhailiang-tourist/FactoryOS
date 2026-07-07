# studio · Integration Studio HTTP 域

> **OpenAPI 扩展**：`GET /v1/studio/flows` · AC **STU-09**  
> **前端**：`src/apps/web-admin` `/studio/*`

## 是什么

Studio 六步向导的 **HTTP 导航真源** 与 **RBAC 门**：integrator/admin 可访问；operator 403。

## 核心功能

| 端点 | 业务含义 |
|------|----------|
| `GET /v1/studio/flows` | 返回 connect→export 六步定义（`studio_wizard_steps.json`） |

## 上下游

- **上游**：web-admin `/studio/*` · integrator 浏览器  
- **下游**：`data/studio_wizard_steps.json` · `AuthMiddleware` 解析 `X-Actor-Role`  
- **不负责**：integration/registry 业务写入（Step2+）

## 门禁

```bash
uv run pytest src/tests/integration/test_stu001_step1_stu09.py -q
./scripts/gate step --step 1 -k 'STU-09'
```

## 关联文档

- [Integration-Studio 规格](../../../../docs/文档/规格说明/Integration-Studio规格.md) §2 · §4
