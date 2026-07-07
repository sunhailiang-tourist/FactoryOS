#!/usr/bin/env node
/**
 * 交互式创建业务模块体系（各板块独立 registry）。
 * 用法：pnpm create:module
 *       pnpm create:module --domain studio --step my-step --label "My Step"
 * 落盘：router · pages · store · api · mocks · i18n · rbac · contracts 追踪链
 */
import { access, mkdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import readline from "node:readline/promises";
import { stdin as input, stdout as output } from "node:process";

const ROOT = path.resolve(import.meta.dirname, "..");
const SRC = path.join(ROOT, "src");
const APP_ID = path.basename(ROOT);

function fileHeader(modulePath, fields) {
  const labels = ["模块", "作用", "怎么用", "解决", "上游", "下游", "关联"];
  const lines = ["/**"];
  for (const key of labels) {
    const value = String(fields[key] ?? "TODO").replace(/\*\//g, "·").replace(/\*/g, "×");
    lines.push(` * ${key}：${value}`);
  }
  lines.push(" */");
  return lines.join("\n") + "\n";
}

function toPascal(step) {
  return step
    .split("-")
    .map((s) => s.charAt(0).toUpperCase() + s.slice(1))
    .join("");
}

function viewPermission(domain, step) {
  return `${domain}.${step.replace(/-/g, ".")}.view`;
}

async function fileExists(p) {
  try {
    await access(p);
    return true;
  } catch {
    return false;
  }
}

async function appendContractTableRow(contractPath, row) {
  if (!(await fileExists(contractPath))) return;
  let text = await readFile(contractPath, "utf8");
  const idCell = row.match(/`([^`]+)`/)?.[1];
  if ((idCell && text.includes(`\`${idCell}\``)) || text.includes(row)) return;
  const marker = "\n\n## 变更规则";
  const markerIdx = text.indexOf(marker);
  if (markerIdx < 0) return;
  const head = text.slice(0, markerIdx);
  const tail = text.slice(markerIdx);
  const lines = head.split("\n");
  let lastTableIdx = -1;
  for (let i = lines.length - 1; i >= 0; i--) {
    if (lines[i].startsWith("|")) {
      lastTableIdx = i;
      break;
    }
  }
  if (lastTableIdx < 0) return;
  lines.splice(lastTableIdx + 1, 0, row);
  await writeFile(contractPath, `${lines.join("\n")}${tail}`);
}

async function upsertI18n(moduleId, stepLabel) {
  const i18nDir = path.join(SRC, "i18n", "modules", moduleId);
  await mkdir(i18nDir, { recursive: true });

  const zh = { title: stepLabel, summary: `${stepLabel}步骤` };
  const en = { title: stepLabel, summary: `${stepLabel} step` };
  await writeFile(path.join(i18nDir, "zh-CN.json"), `${JSON.stringify(zh, null, 2)}\n`);
  await writeFile(path.join(i18nDir, "en-US.json"), `${JSON.stringify(en, null, 2)}\n`);

  const registryPath = path.join(SRC, "i18n", "registry.ts");
  if (await fileExists(registryPath)) {
    let reg = await readFile(registryPath, "utf8");
    if (!reg.includes(`"${moduleId}"`)) {
      reg = reg.replace(
        /] as const;/,
        `  "${moduleId}",\n] as const;`,
      );
      await writeFile(registryPath, reg);
    }
  }

  await appendContractTableRow(
    path.join(SRC, "i18n", "contracts", "README.md"),
    `| \`${moduleId}\` | ${moduleId} | ${stepLabel} |`,
  );
}

async function upsertRbacDomainRegistry(domain, moduleId, permission) {
  const domainDir = path.join(SRC, "rbac", "modules", domain);
  await mkdir(domainDir, { recursive: true });
  const registryPath = path.join(domainDir, "registry.ts");
  const domainUpper = domain.toUpperCase().replace(/-/g, "_");
  const allKey = `ALL_${domainUpper}_VIEW`;

  if (!(await fileExists(registryPath))) {
    const body = `${fileHeader(`src/apps/${APP_ID}/src/rbac/modules/${domain}/registry.ts`, {
      模块: `src/apps/${APP_ID}/src/rbac/modules/${domain}/registry.ts`,
      作用: `${domain} 域权限子表`,
      怎么用: "create:module 自动维护；evaluate 读取",
      解决: "module-id ↔ permission 模块化维护",
      上游: `pages/* · router permissions`,
      下游: "rbac/core/evaluate.ts",
      关联: "rbac/contracts/README.md",
    })}import type { Permission, Role } from "@/rbac/core/types";

export const RBAC_DOMAIN = "${domain}" as const;

export const MODULE_PERMISSIONS: Record<string, Permission> = {
  "${moduleId}": "${permission}",
};

const ${allKey}: Permission[] = ["${permission}"];

const ${domainUpper}_VIEW_ROLES: Role[] = [
  "integrator",
  "admin",
  "platform",
  "business_owner",
  "customer_it",
];

export const ROLE_PERMISSIONS: Record<Role, readonly Permission[]> = {
  integrator: ${allKey},
  admin: ${allKey},
  platform: ${allKey},
  business_owner: ${allKey},
  customer_it: ${allKey},
  operator: [],
};
`;
    await writeFile(registryPath, body);
    await wireRbacRegistry(domain);
    await appendContractTableRow(
      path.join(SRC, "rbac", "contracts", "README.md"),
      `| \`${domain}\` | ${domain} 域权限 |`,
    );
    return;
  }

  let text = await readFile(registryPath, "utf8");
  if (text.includes(`"${moduleId}"`)) return;

  text = text.replace(
    /(export const MODULE_PERMISSIONS: Record<string, Permission> = \{)/,
    `$1\n  "${moduleId}": "${permission}",`,
  );
  const allMatch = text.match(/const (ALL_[A-Z0-9_]+): Permission\[\] = \[/);
  if (allMatch) {
    text = text.replace(
      new RegExp(`(const ${allMatch[1]}: Permission\\[\\] = \\[)`),
      `$1\n  "${permission}",`,
    );
  }
  await writeFile(registryPath, text);
}

async function wireRbacRegistry(domain) {
  const aggPath = path.join(SRC, "rbac", "registry.ts");
  if (!(await fileExists(aggPath))) return;
  let text = await readFile(aggPath, "utf8");
  if (text.includes(`modules/${domain}/registry`)) return;

  const alias = domain.toUpperCase().replace(/-/g, "_");
  const importBlock = `import {
  MODULE_PERMISSIONS as ${alias}_MODULE_PERMISSIONS,
  RBAC_DOMAIN as ${alias}_DOMAIN,
  ROLE_PERMISSIONS as ${alias}_ROLE_PERMISSIONS,
} from "@/rbac/modules/${domain}/registry";
`;

  text = text.replace(
    /(import \{[\s\S]*?\} from "@\/rbac\/modules\/studio\/registry";)/,
    `$1\n${importBlock}`,
  );
  text = text.replace(
    /export const RBAC_DOMAINS = \[([^\]]*)\] as const;/,
    (m, inner) => {
      const domains = inner.trim() ? `${inner.trim()}, ${alias}_DOMAIN` : `${alias}_DOMAIN`;
      return `export const RBAC_DOMAINS = [${domains}] as const;`;
    },
  );
  text = text.replace(
    /export const MODULE_PERMISSIONS: Record<string, string> = \{([\s\S]*?)\};/,
    (m, inner) =>
      `export const MODULE_PERMISSIONS: Record<string, string> = {${inner}  ...${alias}_MODULE_PERMISSIONS,\n};`,
  );
  text = text.replace(
    /export function getRolePermissions\(role: string\): readonly string\[\] \{[\s\S]*?\}/,
    `export function getRolePermissions(role: string): readonly string[] {
  const a = STUDIO_ROLE_PERMISSIONS[role] ?? [];
  const b = ${alias}_ROLE_PERMISSIONS[role] ?? [];
  if (!a.length && !b.length) return [];
  return [...new Set([...a, ...b])];
}`,
  );
  await writeFile(aggPath, text);
}

async function ask(rl, question, fallback = "") {
  const answer = (await rl.question(`${question}${fallback ? ` [${fallback}]` : ""}: `)).trim();
  return answer || fallback;
}

function parseCli() {
  const args = process.argv.slice(2);
  const out = {};
  for (let i = 0; i < args.length; i++) {
    const key = args[i];
    if (key === "--domain") out.domain = args[++i];
    else if (key === "--step") out.step = args[++i];
    else if (key === "--label") out.label = args[++i];
  }
  return out;
}

async function main() {
  const cli = parseCli();
  let domain;
  let step;
  let stepLabel;

  if (cli.domain && cli.step) {
    domain = cli.domain;
    step = cli.step;
    stepLabel = cli.label || toPascal(step);
  } else {
    const rl = readline.createInterface({ input, output });
    domain = await ask(rl, "domain", "studio");
    step = await ask(rl, "step (kebab)", "connect");
    stepLabel = await ask(rl, "step label (i18n title)", toPascal(step));
    rl.close();
  }
  const moduleId = `${domain}-${step}`;
  const routeName = `${domain}.${step.replace(/-/g, ".")}`;
  const routePath = `/${domain}/${step}`;
  const pageName = `Studio${toPascal(step)}Page`;
  const layoutId = domain;
  const hookName = `use${toPascal(domain)}${toPascal(step)}`;
  const handlerExport = `${moduleId.replace(/-/g, "")}Handlers`;
  const permission = viewPermission(domain, step);

  const pageDir = path.join(SRC, "pages", moduleId);
  const contractsDir = path.join(pageDir, "contracts");
  const componentsDir = path.join(pageDir, "components");
  const stylesDir = path.join(pageDir, "styles");
  const apiDir = path.join(SRC, "api", "functions", moduleId);
  const queryHooksDir = path.join(SRC, "api", "query", "hooks");
  const mocksDir = path.join(SRC, "mocks", "handlers");
  const routerDir = path.join(SRC, "router", "modules", moduleId);
  const storeDir = path.join(SRC, "store", "modules", moduleId);

  await mkdir(queryHooksDir, { recursive: true });
  await mkdir(mocksDir, { recursive: true });
  await mkdir(contractsDir, { recursive: true });
  await mkdir(componentsDir, { recursive: true });
  await mkdir(stylesDir, { recursive: true });
  await mkdir(apiDir, { recursive: true });
  await mkdir(routerDir, { recursive: true });
  await mkdir(storeDir, { recursive: true });

  await upsertI18n(moduleId, stepLabel);
  await upsertRbacDomainRegistry(domain, moduleId, permission);

  await writeFile(
    path.join(pageDir, `${pageName}.lazy.tsx`),
    `${fileHeader(`src/apps/${APP_ID}/src/pages/${moduleId}/${pageName}.lazy.tsx`, {
      模块: `src/apps/${APP_ID}/src/pages/${moduleId}/${pageName}.lazy.tsx`,
      作用: `${stepLabel} lazy 页面入口`,
      怎么用: `router/modules/${moduleId}/registry.ts lazy import`,
      解决: "模块 UI 与路由解耦，支持 code-split",
      上游: `router/modules/${moduleId}/registry.ts`,
      下游: `api/functions/${moduleId} · store/modules/${moduleId}`,
      关联: `pages/${moduleId}/contracts/README.md`,
    })}import Typography from "@mui/material/Typography";
import { useT } from "@/i18n/core/useT";

export default function ${pageName}() {
  const { t } = useT("${moduleId}");
  return (
    <>
      <Typography variant="h5" gutterBottom>
        {t("title")}
      </Typography>
      <Typography variant="body2" color="text.secondary">
        route ${routeName} · path ${routePath}
      </Typography>
    </>
  );
}
`,
  );

  await writeFile(
    path.join(contractsDir, "README.md"),
    `# ${moduleId}

## 是什么

TODO：一句话说明本页模块职责。

## 功能

- TODO

## 业务含义

TODO

## 用法

TODO

## 追踪链

| 项 | 值 |
|----|-----|
| module-id | \`${moduleId}\` |
| route name | \`${routeName}\` |
| path | \`${routePath}\` |
| layout | \`${layoutId}\` |
| i18n namespace | \`${moduleId}\` |
| rbac permission | \`${permission}\` |
| store key | \`${domain}/${step}\` |
| query hook | \`${hookName}\` |
| api | TODO |

## 上下游

- **上游**：TODO
- **下游**：TODO

## 不负责

- TODO

## 验收（AC）

- TODO

## 变更规则

1. 改 \`router/modules/${moduleId}/registry.ts\` · store · api · i18n · rbac → **同步** 本文件追踪链 + 对应板块 \`*/contracts/README.md\` 登记索引。
2. \`scripts/check_harness.py\` 强制追踪链与 registry 一致。

## 开发说明

- 页面入口：\`${pageName}.lazy.tsx\`
- 文案：\`i18n/modules/${moduleId}/\`
- 权限：\`rbac/modules/${domain}/registry.ts\` + router \`permissions\`
- 路由登记：\`router/modules/${moduleId}/registry.ts\`
`,
  );

  await writeFile(
    path.join(componentsDir, "README.md"),
    `# ${moduleId}/components · 模块私有组件

仅 \`pages/${moduleId}/\` 内页面与本目录组件可 import。
`,
  );

  await writeFile(
    path.join(routerDir, "registry.ts"),
    `${fileHeader(`src/apps/${APP_ID}/src/router/modules/${moduleId}/registry.ts`, {
      模块: `src/apps/${APP_ID}/src/router/modules/${moduleId}/registry.ts`,
      作用: `${moduleId} 路由子表（ROUTE_MODULE_ENTRIES）`,
      怎么用: "登记 permissions · lazy；glob 自动聚合",
      解决: `单模块路由与 pages/${moduleId} 追踪链一一对应`,
      上游: `pages/${moduleId}/${pageName}.lazy.tsx`,
      下游: "router/registry.ts",
      关联: `pages/${moduleId}/contracts/README.md · rbac permission ${permission}`,
    })}import type { RouteModuleEntry } from "@/router/types";

export const ROUTE_MODULE_ENTRIES: RouteModuleEntry[] = [
  {
    name: "${routeName}",
    moduleId: "${moduleId}",
    layoutId: "${layoutId}",
    path: "${step}",
    permissions: ["${permission}"],
    summary: "${stepLabel} · TODO summary",
    lazy: async () => {
      const m = await import("@/pages/${moduleId}/${pageName}.lazy");
      return { Component: m.default };
    },
  },
];
`,
  );

  await appendContractTableRow(
    path.join(SRC, "router", "contracts", "README.md"),
    `| \`${moduleId}\` | ${routeName} | ${routePath} | ${layoutId} |`,
  );

  await writeFile(
    path.join(storeDir, "registry.ts"),
    `${fileHeader(`src/apps/${APP_ID}/src/store/modules/${moduleId}/registry.ts`, {
      模块: `src/apps/${APP_ID}/src/store/modules/${moduleId}/registry.ts`,
      作用: `${moduleId} store 子表登记`,
      怎么用: "导出 STORE_MODULE_ENTRIES；glob 自动聚合",
      解决: `模块 UI 状态与 pages/${moduleId} 契约一致`,
      上游: `pages/${moduleId}`,
      下游: `store/modules/${moduleId}/${moduleId}.store.ts`,
      关联: `pages/${moduleId}/contracts/README.md`,
    })}import type { StoreModuleEntry } from "@/store/types";

export const STORE_MODULE_ENTRIES: StoreModuleEntry[] = [
  {
    key: "${domain}/${step}",
    moduleId: "${moduleId}",
    summary: "TODO store summary",
  },
];
`,
  );

  await writeFile(
    path.join(storeDir, `${moduleId}.store.ts`),
    `${fileHeader(`src/apps/${APP_ID}/src/store/modules/${moduleId}/${moduleId}.store.ts`, {
      模块: `src/apps/${APP_ID}/src/store/modules/${moduleId}/${moduleId}.store.ts`,
      作用: `${moduleId} Zustand store 实现`,
      怎么用: `页面 import use${toPascal(moduleId)}Store`,
      解决: "模块局部 UI 状态与 API 层分离",
      上游: `pages/${moduleId}`,
      下游: "同模块页面组件",
      关联: `pages/${moduleId}/contracts/README.md`,
    })}import { create } from "zustand";

type ${toPascal(moduleId)}State = {
  // TODO
};

export const use${toPascal(moduleId)}Store = create<${toPascal(moduleId)}State>(() => ({}));
`,
  );

  await writeFile(
    path.join(apiDir, "registry.ts"),
    `${fileHeader(`src/apps/${APP_ID}/src/api/functions/${moduleId}/registry.ts`, {
      模块: `src/apps/${APP_ID}/src/api/functions/${moduleId}/registry.ts`,
      作用: `${moduleId} API 子表`,
      怎么用: "登记 id/method/path/fn",
      解决: "端点与实现文件 harness 可追踪",
      上游: `pages/${moduleId}`,
      下游: `api/functions/${moduleId}/*.fn.ts`,
      关联: `pages/${moduleId}/contracts/README.md`,
    })}import type { ApiRegistryEntry } from "@/api/registry.types";

export const API_MODULE_ENTRIES: ApiRegistryEntry[] = [
  // TODO
];
`,
  );

  await writeFile(
    path.join(apiDir, "index.ts"),
    `${fileHeader(`src/apps/${APP_ID}/src/api/functions/${moduleId}/index.ts`, {
      模块: `src/apps/${APP_ID}/src/api/functions/${moduleId}/index.ts`,
      作用: `${moduleId} API barrel`,
      怎么用: `import from '@/api/functions/${moduleId}'`,
      解决: "模块 API 公共出口",
      上游: `api/functions/${moduleId}/registry.ts`,
      下游: `api/query/hooks/${hookName}.ts`,
      关联: `pages/${moduleId}/contracts/README.md`,
    })}export * from "./registry";\n`,
  );

  await writeFile(
    path.join(queryHooksDir, `${hookName}.ts`),
    `${fileHeader(`src/apps/${APP_ID}/src/api/query/hooks/${hookName}.ts`, {
      模块: `src/apps/${APP_ID}/src/api/query/hooks/${hookName}.ts`,
      作用: `${moduleId} Server State hook`,
      怎么用: `pages/${moduleId} import { ${hookName} }`,
      解决: "Query 层唯一 pages 取数入口",
      上游: `api/functions/${moduleId}/*.fn.ts`,
      下游: `pages/${moduleId}`,
      关联: `api/query/contracts/README.md`,
    })}import { useQuery } from "@tanstack/react-query";
import { queryKeys } from "@/api/query/keys";

export function ${hookName}() {
  return useQuery({
    queryKey: queryKeys.module("${moduleId}"),
    queryFn: async () => ({ ok: true as const }),
    staleTime: 30_000,
  });
}
`,
  );

  const handlerFile = path.join(mocksDir, `${moduleId}.ts`);
  await writeFile(
    handlerFile,
    `${fileHeader(`src/apps/${APP_ID}/src/mocks/handlers/${moduleId}.ts`, {
      模块: `src/apps/${APP_ID}/src/mocks/handlers/${moduleId}.ts`,
      作用: `${moduleId} MSW handlers`,
      怎么用: "handlers/index.ts 聚合",
      解决: "无后端时本模块 API mock",
      上游: `api/functions/${moduleId}/*.fn.ts`,
      下游: "mocks/server.ts",
      关联: `pages/${moduleId}/contracts/README.md`,
    })}import { http, HttpResponse } from "msw";

export const ${handlerExport} = [
  http.get("/v1/${domain}/${step}", () => HttpResponse.json({ moduleId: "${moduleId}", ok: true })),
];
`,
  );

  const handlersIndex = path.join(mocksDir, "index.ts");
  if (await fileExists(handlersIndex)) {
    let handlersText = await readFile(handlersIndex, "utf8");
    if (!handlersText.includes(`./${moduleId}`)) {
      const importLine = `import { ${handlerExport} } from "./${moduleId}";`;
      if (!handlersText.includes(importLine)) {
        handlersText = handlersText.replace(
          /import \{ studioShellHandlers \} from "\.\/studio-shell";/,
          `import { studioShellHandlers } from "./studio-shell";\n${importLine}`,
        );
      }
      if (handlersText.includes("export const handlers = [...studioShellHandlers];")) {
        handlersText = handlersText.replace(
          "export const handlers = [...studioShellHandlers];",
          `export const handlers = [...studioShellHandlers, ...${handlerExport}];`,
        );
      } else if (!handlersText.includes(handlerExport)) {
        handlersText = handlersText.replace(
          /export const handlers = \[(.*?)\];/s,
          (_, inner) => `export const handlers = [${inner.trim()}, ...${handlerExport}];`,
        );
      }
      await writeFile(handlersIndex, handlersText);
    }
  }

  console.log(`\n✅ 已创建模块 ${moduleId}`);
  console.log("\n已自动生成：");
  console.log(`  · i18n/modules/${moduleId}/zh-CN.json · en-US.json`);
  console.log(`  · rbac/modules/${domain}/registry.ts（permission: ${permission}）`);
  console.log(`  · router permissions · contracts 追踪链`);
  console.log("\n后续：");
  console.log(`  1. 完善 pages/${moduleId}/contracts/README.md`);
  console.log(`  2. 若新 domain → layout/modules/{domain}/ + config/modules/{domain}/`);
  console.log(`  3. api/functions/${moduleId}/*.fn.ts`);
  console.log("  4. pnpm check && ./scripts/check_harness.py\n");
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
