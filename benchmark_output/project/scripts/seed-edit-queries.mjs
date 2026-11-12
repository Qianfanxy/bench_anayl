#!/usr/bin/env node
// 把一份「第二轮编辑 query」表格导入平台。
//
// 表格形态（0_query_fix_example.md）：
//   | # | 类型标签 | L | 编辑向query | 要作用的figma url |
// 每行一条独立需求，各自对着一个事先复制好的 Figma 文件，互不干扰。
//
// 导入成 tests，并把「要作用的 figma url」写进 tests.base_figma_url —— 有这个字段
// 的测试起 run 时会走编辑模式（禁止 create_new_file，先 get_metadata 读结构）。
//
// 检查点用通用模板，不调模型生成：这批任务的目的是把修改落到文件里，不是打分。
//
// 用法：
//   node scripts/seed-edit-queries.mjs [markdown 路径] [--base http://127.0.0.1:4176] [--dry-run]
import fs from "node:fs";
import path from "node:path";

const args = process.argv.slice(2);
const flag = (name, fallback) => {
  const index = args.indexOf(name);
  return index >= 0 ? args[index + 1] : fallback;
};
const dryRun = args.includes("--dry-run");
const baseUrl = (flag("--base", "http://127.0.0.1:4176")).replace(/\/$/, "");
const markdownPath = path.resolve(
  args.find((value) => !value.startsWith("--") && value !== flag("--base", "")) || "0_query_fix_example.md"
);
const createdBy = flag("--created-by", "编辑向批次导入");
// 先跑一条确认链路时用：--only B-01（可写多条，逗号分隔）
const only = new Set(
  String(flag("--only", "")).split(",").map((value) => value.trim().toUpperCase()).filter(Boolean)
);

function parseRows(markdown) {
  const rows = [];
  for (const line of markdown.split("\n")) {
    if (!line.trim().startsWith("|")) continue;
    const cells = line.split("|").slice(1, -1).map((cell) => cell.trim());
    if (cells.length < 5) continue;
    const [code, kind, level, query, url] = cells;
    // 表头与分隔行没有 B-xx 编号
    if (!/^B-?\d+$/i.test(code)) continue;
    if (!/figma\.com\/(?:design|file|board)\/[A-Za-z0-9]+/.test(url)) {
      throw new Error(`${code} 那一行的 Figma 链接无法识别：${url}`);
    }
    rows.push({ code: code.toUpperCase(), kind, level, query, url });
  }
  return rows;
}

async function api(pathname, init) {
  const response = await fetch(`${baseUrl}/api${pathname}`, init);
  const text = await response.text();
  let payload = null;
  try { payload = JSON.parse(text); } catch { /* 非 JSON 一律当失败 */ }
  if (!response.ok || payload?.ok === false) {
    throw new Error(`${pathname} ${response.status}: ${payload?.message || text.slice(0, 200)}`);
  }
  return payload;
}

const allRows = parseRows(fs.readFileSync(markdownPath, "utf8"));
const rows = only.size ? allRows.filter((row) => only.has(row.code)) : allRows;
if (!allRows.length) throw new Error(`${markdownPath} 里没解析出任何 B-xx 行`);
if (!rows.length) throw new Error(`--only ${[...only].join(",")} 在表格里没有对应行`);
console.log(`解析到 ${rows.length} 条编辑需求（来源：${markdownPath}）`);

const existing = dryRun ? { tests: [] } : await api("/bootstrap");
const byTitle = new Map((existing.tests || []).map((test) => [test.title, test]));

let created = 0;
let skipped = 0;
for (const row of rows) {
  const title = `${row.code} ${row.kind}`;
  const known = byTitle.get(title);
  if (known) {
    console.log(`跳过 ${title}：平台里已有（${known.code}）`);
    skipped += 1;
    continue;
  }
  if (dryRun) {
    console.log(`[dry-run] ${title} -> ${row.url.slice(0, 72)}…`);
    created += 1;
    continue;
  }
  const result = await api("/tests", {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({
      title,
      query: row.query,
      base_figma_url: row.url,
      criteria_mode: "template",
      created_by: createdBy,
    }),
  });
  console.log(`已创建 ${title} -> ${result.code || result.id}`);
  created += 1;
}
console.log(`完成：新建 ${created} 条，跳过 ${skipped} 条`);
