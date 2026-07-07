# api/generated

OpenAPI SSOT 镜像类型（**禁止手改**）。

| 项 | 值 |
|----|-----|
| 源 | `contracts/openapi/工厂操作系统-v1.1.yaml` |
| 命令 | `pnpm codegen:api` |
| 校验 | `pnpm codegen:check` · harness `openapi_codegen_fresh` |

未纳入 OpenAPI 的扩展 path（如 `GET /v1/studio/flows`）暂保留在 `api/functions/*/flows.types.ts`，待契约 export 后迁入 generated。
