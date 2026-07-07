# form

OpenAPI schema → RHF + Zod 表单生成（S7 实施）。契约真源：`contracts/README.md`。

与 `codegen:api`（OpenAPI 类型）分工不同：**本目录只管表单生成**。

```bash
# 计划命令（S7）
pnpm form:generate -- --module demo-crud --schema AssetCreate
pnpm form:check
```
