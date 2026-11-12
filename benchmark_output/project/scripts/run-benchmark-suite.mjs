import fs from "node:fs";
import path from "node:path";
import { createBenchmarkClient, loadSuite, assertBackend, suiteStep, SuiteResources } from "../server/benchmark_suite.mjs";
import { saveJson } from "../server/benchmark_copies.mjs";
import { isBenchmarkTransportError } from "../server/benchmark_api_resources.mjs";

const argument = (name) => process.argv[process.argv.indexOf(name) + 1];
if (!process.argv.includes("--dir") || !process.argv.includes("--api")) throw new Error("Provide --dir and --api");
const directory = path.resolve(argument("--dir")); const lock = path.join(directory, "supervisor.pid");
if (fs.existsSync(lock)) {
  const pid = Number(fs.readFileSync(lock));
  try { process.kill(pid, 0); throw new Error(`Supervisor already running: ${pid}`); }
  catch (error) { if (error.code !== "ESRCH") throw error; fs.unlinkSync(lock); }
}
fs.writeFileSync(lock, String(process.pid), { flag: "wx", mode: 0o600 });
const memory = { frameTasks: new Map(), frameAttempted: new Map(), evidenceErrors: {} };
const cleanup = () => { if (fs.existsSync(lock) && Number(fs.readFileSync(lock)) === process.pid) fs.unlinkSync(lock); };
process.on("exit", cleanup);
process.on("SIGTERM", () => process.exit(0));
try {
  const suite = loadSuite(directory); const call = createBenchmarkClient(argument("--api"));
  await assertBackend(suite, call); const resources = new SuiteResources(suite, call);
  for (;;) {
    try {
      const progress = await suiteStep(suite, call, resources, memory);
      saveJson(path.join(directory, "progress.json"), progress);
      fs.rmSync(path.join(directory, "supervisor-error.json"), { force: true });
      console.log(JSON.stringify({ at: progress.updated_at, scored: progress.scored, total: progress.total, active: progress.active, phase: progress.phase }));
      if (progress.finished) { saveJson(path.join(directory, "complete.json"), progress); break; }
      if (process.argv.includes("--once")) { await Promise.allSettled([...memory.frameTasks.values()]); break; }
    } catch (error) {
      saveJson(path.join(directory, "supervisor-error.json"), { at: new Date().toISOString(), message: error.message, retryable: isBenchmarkTransportError(error) || error.status >= 500 });
      if (!isBenchmarkTransportError(error) && !(error.status >= 500)) throw error;
      // Reconcile committed batches from the API; never blindly replay a POST.
    }
    await new Promise((resolve) => setTimeout(resolve, 15000));
  }
} catch (error) { console.error(error.message); process.exitCode = 1; }
