# apps/web-admin · PC 管理端

## 是什么

**React 18 + TypeScript + Vite** 管理平台：Graph、Rule、集成、审计只读/配置入口。

## 主要功能

- Graph 版本与 freeze 操作 UI
- 租户集成状态、Shadow 监控
- 调用 `apps/api` REST

## 不负责什么

- 直连 Legacy ERP/MES
- 内核业务逻辑

## 上下游

- **上游**：管理员浏览器
- **下游**：`apps/api` `/v1/*`

## 本地开发

Phase 1 后半：`pnpm dev`（待 package.json）。

## 相关文档

- AC-UX-001 · Integration-Studio 规格
