import path from "node:path";
import { defineConfig, mergeConfig } from "vitest/config";
import viteConfig from "./vite.config";

export default mergeConfig(
  viteConfig,
  defineConfig({
    test: {
      environment: "node",
      environmentMatchGlobs: [["**/*.test.tsx", "jsdom"]],
      setupFiles: ["src/test/setup.ts"],
      include: ["src/**/*.test.ts", "src/**/*.test.tsx"],
      passWithNoTests: false,
    },
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "./src"),
      },
    },
  }),
);
