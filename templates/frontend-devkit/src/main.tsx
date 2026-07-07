/**
 * 模块：src/apps/web-admin/src/main.tsx
 * 作用：Vite 应用入口，挂载 React 根
 * 怎么用：pnpm dev（.env.development 默认 VITE_MSW=1）
 * 解决：首屏 boot shell → React 接管无白屏
 * 上游：index.html · Vite · mocks/browser.ts
 * 下游：bootstrap.tsx
 * 关联：ENGINEERING.md §10 S4
 */
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "@/styles/global.css";
import { Bootstrap } from "@/bootstrap";

async function enableMswWhenRequested(): Promise<void> {
  if (import.meta.env.VITE_MSW !== "1") {
    return;
  }
  const { worker } = await import("@/mocks/browser");
  await worker.start({ onUnhandledRequest: "bypass", quiet: true });
}

function clearBootShell(): void {
  document.getElementById("fos-boot-shell")?.remove();
}

function mountApp(): void {
  const root = document.getElementById("root");
  if (!root) {
    throw new Error("root element #root not found");
  }
  clearBootShell();
  createRoot(root).render(
    <StrictMode>
      <Bootstrap />
    </StrictMode>,
  );
}

async function bootstrap(): Promise<void> {
  await enableMswWhenRequested();
  mountApp();
}

void bootstrap();
