# src/apps/web-admin · PC 管理端 / Integration Studio

## 铁律（钉死）

> **新客户接入、扩系统、开写、freeze、Package 导出/导入——全程在本应用 `/studio/*` 完成。**  
> 禁止以改 Git、手改 `integration/tenants/*.yaml`、`factoryos guide` 作为生产实施路径。  
> D1 硬 Gate：[STU-001](../../docs/文档/验收/验收用例-STU-001-Studio配置主路径.md) P0 全绿。

## 是什么

**React 18 + TypeScript + Vite** 管理平台：Graph、Rule、集成、审计只读/配置入口。

## 主要功能

- Graph 版本与 freeze 操作 UI
- 租户集成状态、Shadow 监控
- 调用 `server/api` REST

## 不负责什么

- 直连 Legacy ERP/MES
- 内核业务逻辑

## 上下游

- **上游**：管理员浏览器
- **下游**：`server/api` `/v1/*`

## 本地开发

Phase 1 后半：`pnpm dev`（待 package.json）。

## 相关文档

- AC-UX-001 · Integration-Studio 规格
