import fs from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
function option(name, fallback) {
  const at = process.argv.indexOf(name);
  if (at < 0) return fallback;
  if (!process.argv[at + 1]) throw new Error(`${name} requires a value`);
  return process.argv[at + 1];
}
const configFlag = process.argv.indexOf("--runtime-config");
let dependencyRoot = "";
if (configFlag !== -1) {
  if (!process.argv[configFlag + 1]) throw new Error("--runtime-config requires a JSON file");
  const configFile = path.resolve(process.argv[configFlag + 1]);
  Object.assign(process.env, JSON.parse(fs.readFileSync(configFile, "utf8")));
  dependencyRoot = path.dirname(configFile);
}

// Always isolate writes even when borrowing dependency/account paths from a
// prepared runtime. Never inherit that runtime's database, runs or working cwd.
const storage = path.resolve(option("--storage-root", path.join(root, "storage/benchmark-design")));
const port = Number(option("--port", "18174"));
if (!Number.isInteger(port) || port < 1024 || port > 65535) throw new Error("Invalid benchmark port");
const workspace = path.join(storage, "workspace");
fs.mkdirSync(workspace, { recursive: true });
// Reuse the configured identity, while making every subprocess share this
// branch's rate scheduler. Do not edit the borrowed runtime or its OAuth file.
if (process.env.UI_EVAL_MCP_CONFIG_PATH) {
  const config = JSON.parse(fs.readFileSync(process.env.UI_EVAL_MCP_CONFIG_PATH, "utf8"));
  const figma = config.mcpServers.figma;
  figma.args = [path.join(root, "server/figma_mcp_stdio_proxy.py")];
  figma.env = { ...figma.env, FIGMA_MCP_BUDGET_FILE: option("--account-budget", path.join(root, "storage/benchmark-design/private/figma-budget.json")), FIGMA_MCP_MIN_INTERVAL: "4" };
  const file = path.join(storage, "private/figma-mcp.json");
  fs.mkdirSync(path.dirname(file), { recursive: true, mode: 0o700 });
  fs.writeFileSync(file, JSON.stringify(config, null, 2) + "\n", { mode: 0o600 });
  process.env.UI_EVAL_MCP_CONFIG_PATH = file;
  process.env.FIGMA_MCP_BUDGET_FILE = figma.env.FIGMA_MCP_BUDGET_FILE;
  process.env.FIGMA_MCP_MIN_INTERVAL = "4";
}
Object.assign(process.env, {
  UI_EVAL_BENCHMARK_DESIGN: "1",
  UI_EVAL_HOST: "127.0.0.1", UI_EVAL_PORT: String(port),
  UI_EVAL_STORAGE_PATH: storage, UI_EVAL_RUNS_ROOT: path.join(storage, "runs"),
  UI_EVAL_RUN_CWD: workspace,
});
const commandDirs = [process.env.UI_EVAL_PYTHON, process.env.CLAUDE_CODE_PATH, process.env.CLAUDE_TAP_PATH]
  .filter((file) => file && path.isAbsolute(file)).map((file) => path.dirname(file));
process.env.PATH = [...new Set(commandDirs), process.env.PATH].join(path.delimiter);
process.env.PYTHONPATH = [
  dependencyRoot && fs.existsSync(path.join(dependencyRoot, "vendor/claude_tap")) ? path.join(dependencyRoot, "vendor") : "",
  process.env.CTTAP_REPO_PATH, process.env.UI_EVAL_PRODUCTION_SERVER, process.env.PYTHONPATH,
].filter(Boolean).join(path.delimiter);
process.chdir(workspace);
console.log(`benchmark-design: http://127.0.0.1:${port}; storage=${storage}`);
await import(pathToFileURL(path.join(root, "server/index.mjs")));
