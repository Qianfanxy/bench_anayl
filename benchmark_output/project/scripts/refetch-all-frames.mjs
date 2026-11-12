#!/usr/bin/env node
// 把评测端所有带 Figma 链接的 run 重新补一遍图 —— 全部走 REST（零 MCP 配额、零模型）。
//
// 老的 figma-frames 内容直接覆盖：那些图要么是模型顺手截的、要么是整画布切出来的，
// 质量参差；REST 取的是每个画板的原生 2 倍图，统一换掉。
//
// ⚠ Figma 的文件权限按账号隔离：PAT 是 xinya-old 的，读别的账号建的文件会 403/404，
//    这类只记录、不算失败（生成端迁入的稿子就属于这种）。
// 用法：node scripts/refetch-all-frames.mjs [--concurrency 50] [--limit N] [--dry-run]
import fs from "node:fs";
import path from "node:path";
import { DatabaseSync } from "node:sqlite";
import { fetchFramesAnyAccount, readFigmaPats } from "../server/figma_rest_frames.mjs";

const here = path.dirname(new URL(import.meta.url).pathname);
const appRoot = path.resolve(here, "..");
const args = process.argv.slice(2);
const flag = (name, fallback) => {
  const at = args.indexOf(`--${name}`);
  return at >= 0 && args[at + 1] && !args[at + 1].startsWith("--") ? args[at + 1] : fallback;
};
const concurrency = Math.max(1, Number(flag("concurrency", 50)));
const limit = Number(flag("limit", 0));
const dryRun = args.includes("--dry-run");

const storageRoot = process.env.UI_EVAL_STORAGE_PATH
  ? path.resolve(process.env.UI_EVAL_STORAGE_PATH)
  : path.join(appRoot, "storage");
const privateDir = path.join(storageRoot, "private");
const tokens = readFigmaPats(privateDir);
if (!tokens.length) {
  console.error("没有配置 Figma PAT（storage/private/figma-pat.json / figma-pats.json）");
  process.exit(2);
}
console.log(`可用账号 ${tokens.length} 个：${tokens.map((t) => t.account).join("、")}`);
const db = new DatabaseSync(path.join(storageRoot, "ui-eval.sqlite3"));
const parseFileKey = (url) => (String(url).match(/\/(?:file|design|board)\/([A-Za-z0-9]+)/) || [])[1] || "";

let rows = db.prepare("SELECT id, figma_url, run_dir FROM runs WHERE figma_url != '' AND run_dir != '' ORDER BY started_at DESC").all()
  .filter((row) => parseFileKey(row.figma_url) && fs.existsSync(row.run_dir));
// --only-failed：只补上一轮报告里失败的那些，别把已经取好的再取一遍（省 API 调用）
if (args.includes("--only-failed")) {
  const reportPath = path.join(storageRoot, "private", "refetch-frames-report.json");
  let failed = new Set();
  try {
    failed = new Set((JSON.parse(fs.readFileSync(reportPath, "utf8")).failures || []).map((f) => f.id));
  } catch { /* 没报告就当全量 */ }
  if (failed.size) {
    rows = rows.filter((row) => failed.has(row.id));
    console.log(`只补上一轮失败的 ${rows.length} 条`);
  }
}
// --ids-file：只补指定的那些 run（收尾时把"还没补到图"的挑出来单独跑，不必全量重来）
const idsFile = flag("ids-file", "");
if (idsFile) {
  const wanted = new Set(JSON.parse(fs.readFileSync(idsFile, "utf8")));
  rows = rows.filter((row) => wanted.has(row.id));
  console.log(`只补指定的 ${rows.length} 条`);
}
if (limit) rows = rows.slice(0, limit);
console.log(`共 ${rows.length} 条待补图，并发 ${concurrency}${dryRun ? "（试跑，不写盘）" : ""}`);

const stats = { ok: 0, frames: 0, noAccess: 0, failed: 0, empty: 0 };
const failures = [];
let cursor = 0;
let done = 0;

async function worker() {
  while (cursor < rows.length) {
    const row = rows[cursor++];
    const fileKey = parseFileKey(row.figma_url);
    const dir = path.join(row.run_dir, "figma-frames");
    if (dryRun) { stats.ok += 1; continue; }
    // ⚠ 先取到临时目录、成功了再换 —— 之前是"先删后取"，撞上 429 的那批直接变成一张图都没有
    const staging = path.join(row.run_dir, ".figma-frames-new");
    try {
      fs.rmSync(staging, { recursive: true, force: true });
      const result = await fetchFramesAnyAccount(row.run_dir, fileKey, {
        privateDir, tokens, dir: staging,
        onWait: ({ status, attempt, delay }) =>
          console.log(`  ⏳ ${row.id} 被限流（HTTP ${status}，第 ${attempt} 次），等 ${Math.round(delay / 1000)}s`),
      });
      if (result.files.length) {
        fs.mkdirSync(dir, { recursive: true });
        for (const name of fs.readdirSync(dir)) {
          if (name.endsWith(".png") || name === "frames.json") {
            try { fs.rmSync(path.join(dir, name)); } catch { /* 覆盖即可 */ }
          }
        }
        for (const name of fs.readdirSync(staging)) {
          fs.renameSync(path.join(staging, name), path.join(dir, name));
        }
      }
      fs.rmSync(staging, { recursive: true, force: true });
      if (!result.files.length) { stats.empty += 1; failures.push({ id: row.id, reason: result.reason || "没有画板" }); }
      else { stats.ok += 1; stats.frames += result.files.length; }
    } catch (error) {
      const message = String(error.message || "");
      // 403/404 = 这个文件不属于 PAT 那个账号（生成端迁入的稿子），不算故障
      if (/都读不到这个文件/.test(message)) { stats.noAccess += 1; failures.push({ id: row.id, reason: "所有账号都无权限" }); }
      else { stats.failed += 1; failures.push({ id: row.id, reason: message.slice(0, 120) }); }
    }
    done += 1;
    if (done % 25 === 0) console.log(`  ...${done}/${rows.length} | 成功 ${stats.ok}（${stats.frames} 张）无权限 ${stats.noAccess} 失败 ${stats.failed}`);
  }
}

const started = Date.now();
await Promise.all(Array.from({ length: Math.min(concurrency, rows.length) }, worker));
console.log(`\n完成：成功 ${stats.ok} 条 / ${stats.frames} 张图；无权限 ${stats.noAccess}；空文件 ${stats.empty}；失败 ${stats.failed}`);
console.log(`用时 ${((Date.now() - started) / 1000).toFixed(0)}s`);
const report = path.join(storageRoot, "private", "refetch-frames-report.json");
if (fs.existsSync(report)) fs.copyFileSync(report, `${report}.prev`);
fs.writeFileSync(report, JSON.stringify({ stats, failures }, null, 2));
console.log(`明细写在 ${report}`);
