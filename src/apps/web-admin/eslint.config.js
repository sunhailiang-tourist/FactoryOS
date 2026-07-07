import js from "@eslint/js";
import globals from "globals";
import reactHooks from "eslint-plugin-react-hooks";
import tseslint from "typescript-eslint";

/** web-admin ESLint — sector 矩阵 import 边界（W-10）。 */
export default tseslint.config(
  { ignores: ["dist/**", "node_modules/**", "scripts/**", "storybook-static/**", ".playwright-browsers/**", "test-results/**"] },
  js.configs.recommended,
  ...tseslint.configs.recommended,
  {
    files: ["src/**/*.{ts,tsx}"],
    languageOptions: {
      ecmaVersion: 2020,
      globals: globals.browser,
    },
    plugins: {
      "react-hooks": reactHooks,
    },
    rules: {
      ...reactHooks.configs.recommended.rules,
      "@typescript-eslint/no-unused-vars": [
        "error",
        { argsIgnorePattern: "^_", varsIgnorePattern: "^_" },
      ],
    },
  },
  {
    files: ["src/pages/**/*.{ts,tsx}"],
    rules: {
      "no-restricted-globals": [
        "error",
        {
          name: "fetch",
          message: "pages 禁止直接 fetch；使用 @/api/query/hooks",
        },
      ],
      "no-restricted-imports": [
        "error",
        {
          paths: [
            {
              name: "echarts",
              message: "pages 禁止直接 import echarts；使用 @/components/charts",
            },
            {
              name: "echarts/core",
              message: "pages 禁止直接 import echarts；使用 @/components/charts",
            },
            {
              name: "@tanstack/react-query",
              message: "pages 禁止直引 react-query；使用 @/api/query/hooks",
            },
            {
              name: "i18next",
              message: "禁止直引 i18next；使用 @/i18n/core/useT",
            },
            {
              name: "react-i18next",
              message: "禁止直引 react-i18next；使用 @/i18n/core/useT",
            },
          ],
          patterns: [
            {
              group: ["echarts/*"],
              message: "pages 禁止直接 import echarts；使用 @/components/charts",
            },
            {
              group: ["@/api/functions", "@/api/functions/*"],
              message: "pages 禁止直引 api/functions；使用 @/api/query/hooks",
            },
          ],
        },
      ],
    },
  },
  {
    files: ["src/api/functions/**/*.{ts,tsx}"],
    rules: {
      "no-restricted-imports": [
        "error",
        {
          patterns: [
            {
              group: ["@/pages", "@/pages/*", "@/store", "@/store/*", "@/components", "@/components/*"],
              message: "api/functions 禁止依赖 pages/store/components",
            },
            {
              group: ["@/api/query", "@/api/query/*"],
              message: "api/functions 禁止依赖 query 层（防循环）",
            },
          ],
        },
      ],
    },
  },
  {
    files: ["src/api/query/**/*.{ts,tsx}"],
    rules: {
      "no-restricted-imports": [
        "error",
        {
          patterns: [
            {
              group: ["@/pages", "@/pages/*"],
              message: "api/query 禁止依赖 pages",
            },
          ],
        },
      ],
    },
  },
  {
    files: ["src/components/**/*.{ts,tsx}"],
    rules: {
      "no-restricted-imports": [
        "error",
        {
          patterns: [
            {
              group: ["@/pages", "@/pages/*", "@/api/query/hooks", "@/api/query/hooks/*"],
              message: "components 禁止依赖 pages 或 query hooks（保持 dumb UI）",
            },
          ],
        },
      ],
    },
  },
  {
    files: ["src/api/request/**/*.{ts,tsx}"],
    rules: {
      "no-restricted-imports": [
        "error",
        {
          patterns: [
            {
              group: [
                "@/pages",
                "@/pages/*",
                "@/components",
                "@/components/*",
                "@/api/query",
                "@/api/query/*",
                "@/api/functions",
                "@/api/functions/*",
              ],
              message: "api/request 仅传输层，禁止上层依赖",
            },
          ],
        },
      ],
    },
  },
  {
    files: ["e2e/**/*.ts"],
    languageOptions: {
      globals: globals.node,
    },
  },
);
