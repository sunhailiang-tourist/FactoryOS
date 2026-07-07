import path from "node:path";
import tailwindcss from "@tailwindcss/vite";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

/** FactoryOS 管理台 · 路径别名 · 按 module/api 分包 */
export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks(id) {
          if (
            id.includes("node_modules/react/")
            || id.includes("node_modules/react-dom/")
            || id.includes("node_modules/react-router")
            || id.includes("node_modules/@tanstack/react-query")
            || id.includes("node_modules/scheduler/")
          ) {
            return "vendor-react";
          }
          if (id.includes("node_modules/@mui") || id.includes("node_modules/@emotion")) {
            return "vendor-mui";
          }
          if (id.includes("node_modules/echarts") || id.includes("node_modules/zrender")) {
            return "vendor-echarts";
          }
          if (id.includes("node_modules/animate.css")) {
            return "vendor-animate";
          }
          const moduleMatch = id.match(/\/src\/pages\/([^/]+)\//);
          if (moduleMatch) {
            return `module-${moduleMatch[1]}`;
          }
          const apiMatch = id.match(/\/src\/api\/functions\/([^/]+)\//);
          if (apiMatch) {
            return `api-${apiMatch[1]}`;
          }
        },
      },
    },
  },
  server: {
    port: 5173,
    proxy: {
      "/v1": {
        target: "http://127.0.0.1:8000",
        changeOrigin: true,
      },
    },
  },
});
