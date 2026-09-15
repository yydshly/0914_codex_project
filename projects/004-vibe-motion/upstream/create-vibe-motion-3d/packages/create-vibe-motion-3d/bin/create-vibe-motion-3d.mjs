#!/usr/bin/env node

import {
  cpSync,
  existsSync,
  lstatSync,
  mkdirSync,
  readdirSync,
  readFileSync,
  writeFileSync,
} from "node:fs";
import { basename, dirname, relative, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

const SCRIPT_DIR = dirname(fileURLToPath(import.meta.url));
const PACKAGE_ROOT = resolve(SCRIPT_DIR, "..", "template");
const MANIFEST_PATH = resolve(PACKAGE_ROOT, "scaffold-manifest.json");
const TEMPLATE_PACKAGE_PATH = resolve(PACKAGE_ROOT, "scaffold-template-package.json");
const TEMPLATE_GITIGNORE_PATH = resolve(PACKAGE_ROOT, "scaffold-template-gitignore");
const DEFAULT_TARGET_DIRNAME = "vibe-motion-3d-app";
const DEFAULT_REGISTRY = "https://registry.npmmirror.com";

const args = process.argv.slice(2);
const positional = [];
let registryFromArg = null;

for (let index = 0; index < args.length; index += 1) {
  const arg = args[index];

  if (arg === "--registry") {
    const nextValue = args[index + 1];
    if (!nextValue || nextValue.startsWith("-")) {
      throw new Error("[create-vibe-motion-3d] missing value for --registry.");
    }
    registryFromArg = nextValue;
    index += 1;
    continue;
  }

  if (arg.startsWith("--registry=")) {
    const value = arg.slice("--registry=".length);
    if (value.trim().length === 0) {
      throw new Error("[create-vibe-motion-3d] missing value for --registry.");
    }
    registryFromArg = value;
    continue;
  }

  if (arg.startsWith("-")) {
    continue;
  }

  positional.push(arg);
}

const force = args.includes("--force") || args.includes("-f");
const skipInstall = args.includes("--skip-install");
const targetArg = positional[0] ?? DEFAULT_TARGET_DIRNAME;
const targetDir = resolve(process.cwd(), targetArg);

const ensureTargetDir = () => {
  if (!existsSync(targetDir)) {
    mkdirSync(targetDir, { recursive: true });
    return;
  }

  if (!lstatSync(targetDir).isDirectory()) {
    throw new Error(`[create-vibe-motion-3d] target exists and is not a directory: ${targetDir}`);
  }

  const files = readdirSync(targetDir);
  if (files.length > 0 && !force) {
    throw new Error(
      `[create-vibe-motion-3d] target directory is not empty: ${targetDir}\n` +
        "Re-run with --force to overwrite matching files."
    );
  }
};

const copyEntry = (entryPath) => {
  const sourcePath = resolve(PACKAGE_ROOT, entryPath);
  const destinationPath = resolve(targetDir, entryPath);
  mkdirSync(dirname(destinationPath), { recursive: true });
  cpSync(sourcePath, destinationPath, { recursive: true, force: true });
};

const sanitizePackageName = (name) =>
  name
    .trim()
    .toLowerCase()
    .replace(/[^a-z0-9-._~]/g, "-")
    .replace(/^[._-]+/, "")
    .replace(/[._-]+$/, "") || "vibe-motion-3d-app";

const writePackageJson = () => {
  const template = JSON.parse(readFileSync(TEMPLATE_PACKAGE_PATH, "utf8"));
  template.name = sanitizePackageName(basename(targetDir));
  writeFileSync(resolve(targetDir, "package.json"), `${JSON.stringify(template, null, 2)}\n`, "utf8");
};

const writeGitignore = () => {
  const content = readFileSync(TEMPLATE_GITIGNORE_PATH, "utf8");
  writeFileSync(resolve(targetDir, ".gitignore"), content, "utf8");
};

const readManifest = () => {
  const content = readFileSync(MANIFEST_PATH, "utf8");
  const parsed = JSON.parse(content);
  if (!Array.isArray(parsed) || parsed.some((entry) => typeof entry !== "string")) {
    throw new Error("[create-vibe-motion-3d] scaffold-manifest.json must be a string array.");
  }
  return parsed;
};

const normalizeRegistry = (value) => {
  if (typeof value !== "string") {
    return null;
  }

  const trimmed = value.trim();
  if (trimmed.length === 0) {
    return null;
  }

  return trimmed.replace(/\/+$/, "");
};

const resolveRegistry = () =>
  normalizeRegistry(registryFromArg) ??
  normalizeRegistry(process.env.CREATE_VIBE_MOTION_3D_REGISTRY) ??
  normalizeRegistry(process.env.npm_config_registry) ??
  normalizeRegistry(process.env.NPM_CONFIG_REGISTRY) ??
  DEFAULT_REGISTRY;

const resolveRequiredPnpmSpec = () => {
  try {
    const template = JSON.parse(readFileSync(TEMPLATE_PACKAGE_PATH, "utf8"));
    const packageManager = typeof template.packageManager === "string" ? template.packageManager.trim() : "";
    if (packageManager.startsWith("pnpm@")) {
      return packageManager;
    }
  } catch {
    // fall through
  }

  return "pnpm";
};

const buildInstallEnv = (registry) => ({
  ...process.env,
  npm_config_registry: registry,
  NPM_CONFIG_REGISTRY: registry,
});

const commandCandidates = (command) => {
  if (process.platform !== "win32") {
    return [command];
  }

  return [`${command}.cmd`, `${command}.exe`, command];
};

const runCommand = (command, commandArgs, options) => {
  if (process.platform === "win32" && !command.endsWith(".cmd") && !command.endsWith(".exe")) {
    return spawnSync(process.env.ComSpec || process.env.COMSPEC || "cmd.exe", ["/d", "/c", command, ...commandArgs], options);
  }

  return spawnSync(command, commandArgs, options);
};

const findAvailableCommand = (command) => {
  for (const candidate of commandCandidates(command)) {
    const result = runCommand(candidate, ["--version"], { stdio: "ignore" });
    if (!result.error && result.status === 0) {
      return candidate;
    }
  }

  return null;
};

const installPnpmWithNpm = (registry) => {
  const npmCommand = findAvailableCommand("npm");
  if (!npmCommand) {
    return null;
  }

  const pnpmSpec = resolveRequiredPnpmSpec();
  console.log(`\nDetected npm but pnpm is missing. Installing ${pnpmSpec} globally...`);
  const result = runCommand(
    npmCommand,
    ["install", "--global", pnpmSpec, "--registry", registry],
    {
      stdio: "inherit",
      env: buildInstallEnv(registry),
    }
  );

  if (result.error || (typeof result.status === "number" && result.status !== 0)) {
    console.error(`\nFailed to install ${pnpmSpec}. Run \`npm install -g ${pnpmSpec}\` and retry.`);
    return null;
  }

  return findAvailableCommand("pnpm");
};

const formatInstallCommand = (registry) => `pnpm install --registry=${registry}`;
const formatDevCommand = () => "pnpm dev";

const runInstall = (registry) => {
  console.log(`\nUsing registry: ${registry}`);

  let pnpmCommand = findAvailableCommand("pnpm");
  if (!pnpmCommand) {
    pnpmCommand = installPnpmWithNpm(registry);
  }

  if (!pnpmCommand) {
    console.log("\nCould not find pnpm or install it via npm. Please install pnpm and run `pnpm install` manually.");
    return false;
  }

  console.log("\nInstalling dependencies with pnpm...");
  const result = runCommand(pnpmCommand, ["install", "--registry", registry], {
    cwd: targetDir,
    stdio: "inherit",
    env: buildInstallEnv(registry),
  });

  if (result.error || (typeof result.status === "number" && result.status !== 0)) {
    console.error("\nInstall failed. Run `pnpm install` manually in the project directory.");
    return false;
  }

  return true;
};

const run = () => {
  const registry = resolveRegistry();
  ensureTargetDir();

  for (const entry of readManifest()) {
    copyEntry(entry);
  }

  writePackageJson();
  writeGitignore();

  const displayPath = relative(process.cwd(), targetDir) || ".";
  console.log(`\nScaffold created at ${displayPath}`);

  if (!skipInstall) {
    runInstall(registry);
  }

  console.log("\nNext steps:");
  if (targetArg !== ".") {
    console.log(`  cd ${displayPath}`);
  }
  if (skipInstall) {
    console.log(`  ${formatInstallCommand(registry)}`);
  }
  console.log(`  ${formatDevCommand()}`);
};

try {
  run();
} catch (error) {
  const message = error instanceof Error ? error.message : String(error);
  console.error(message);
  process.exit(1);
}
