# src/apps/h5-worker · 工人 H5

## 是什么

钉钉/企微内 **工人多模态入口**：说/拍/扫 → Harness 确认 → 执行。

## 主要功能

- 工单报工、拍照识别、语音入口
- IM OAuth 与 `server/api` perception/harness 对接

## 不负责什么

- 跳过 Harness 确认门（R-11）
- 管理端配置（`web-admin`）

## 上下游

- **上游**：钉钉/企微 WebView
- **下游**：`server/api` perception、harness、agent 路由

## 相关文档

- ADR-002 R-11 · 终端智能极
