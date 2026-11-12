#!/usr/bin/env node
// 在一台新 clone 的机器上，把「服务器 Opus 5」和「Gemini 3.5 Flash」两个评分模型
// 种进 storage/ui-eval.sqlite3，让 CC 评分按钮有可选的评分模型。
//
// 用法（在仓库根目录）：
//   1) 先 npm install && npm run build，并启动一次 node server/index.mjs 让它建好库表（有了库表就能 Ctrl-C）
//   2) node scripts/seed-eval-models.mjs
//   3) 把两把 API Key 放进 storage/private/model_api_keys.json（走安全通道拷过来，git 不带 key）
//   4) 重新启动 server
//
// 只插模型「配置行」，不含任何 Key —— Key 在 storage/private/model_api_keys.json（0600），单独传。
import { DatabaseSync } from "node:sqlite";
import path from "node:path";
import fs from "node:fs";

const dbPath = process.env.UI_EVAL_DB
  || path.join(process.cwd(), "storage", "ui-eval.sqlite3");
if (!fs.existsSync(dbPath)) {
  console.error(`找不到 ${dbPath} —— 先启动一次 server 让它建好库表，再跑本脚本。`);
  process.exit(1);
}
const db = new DatabaseSync(dbPath);
const hasModels = db.prepare(
  "SELECT name FROM sqlite_master WHERE type='table' AND name='models'"
).get();
if (!hasModels) {
  console.error("库里还没有 models 表 —— 先启动一次 server（node server/index.mjs）让它建表。");
  process.exit(1);
}

// 两个评分模型的配置（与源机一致；不含 Key）
const MODELS = [
  {
    id: "model_claude_opus5", name: "服务器 Opus 5", provider: "Claude Code",
    connection_mode: "direct", host: "127.0.0.1", port: 0,
    base_url: "https://tokenhub.sensetime.com", model_id: "claude-opus-5",
    auth_mode: "api-key", api_key_env: "ANTHROPIC_API_KEY", reasoning_mode: "summary",
    is_default: 1, api_format: "", is_deleted: 0, can_evaluate: 1, buffered_stream: 0,
  },
  {
    id: "model_gemini_31_pro_cc", name: "Gemini 3.5 Flash", provider: "TokenHub / Gemini",
    connection_mode: "cc-switch", host: "tokenhub.sensetime.com", port: 443,
    base_url: "https://tokenhub.sensetime.com", model_id: "gemini-3.5-flash",
    auth_mode: "api-key", api_key_env: "ANTHROPIC_API_KEY", reasoning_mode: "summary",
    is_default: 0, api_format: "", is_deleted: 0, can_evaluate: 1, buffered_stream: 1,
  },
];

// 显式列名（这个仓库的红线：禁止位置式 INSERT），有则更新、无则插入
const upsert = db.prepare(`
  INSERT INTO models (
    id, name, provider, connection_mode, host, port, base_url, model_id,
    auth_mode, api_key_env, reasoning_mode, is_default, api_format,
    is_deleted, can_evaluate, buffered_stream, created_at
  ) VALUES (
    @id, @name, @provider, @connection_mode, @host, @port, @base_url, @model_id,
    @auth_mode, @api_key_env, @reasoning_mode, @is_default, @api_format,
    @is_deleted, @can_evaluate, @buffered_stream, @created_at
  )
  ON CONFLICT(id) DO UPDATE SET
    name=excluded.name, provider=excluded.provider, connection_mode=excluded.connection_mode,
    host=excluded.host, port=excluded.port, base_url=excluded.base_url, model_id=excluded.model_id,
    auth_mode=excluded.auth_mode, api_key_env=excluded.api_key_env, reasoning_mode=excluded.reasoning_mode,
    is_default=excluded.is_default, api_format=excluded.api_format, is_deleted=0,
    can_evaluate=excluded.can_evaluate, buffered_stream=excluded.buffered_stream
`);

const now = new Date().toISOString();
for (const m of MODELS) {
  upsert.run({ ...m, created_at: now });
  console.log(`已种入评分模型：${m.name}（${m.model_id}）`);
}

// 有了 key 才真能评分；这里只检查是否已放好 key，不打印 key 内容
const keyFile = path.join(path.dirname(dbPath), "private", "model_api_keys.json");
let haveKeys = {};
try { haveKeys = JSON.parse(fs.readFileSync(keyFile, "utf8")); } catch { /* 还没放 */ }
for (const m of MODELS) {
  const ok = typeof haveKeys[m.id] === "string" && haveKeys[m.id].trim();
  console.log(`  ${m.name} 的 API Key：${ok ? "已就位" : "⚠ 缺失 —— 需把 key 放进 storage/private/model_api_keys.json"}`);
}
console.log("完成。重启 server 后，CC 评分的「评分模型」下拉里就有这两个了。");
