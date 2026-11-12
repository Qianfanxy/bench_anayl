#!/usr/bin/env node
// 固定量表的题项分析：拿一套量表（默认 fixed_v3pool）的基准分，回答「哪些题该留、哪些该合、哪些该删」。
//
//   node scripts/scale-item-analysis.mjs --method fixed_v3pool [--models "Opus 5,Fable 5,Fable 5.1"]
//                                        [--tests TEST-056,TEST-062] [--out /path/report.md] [--csv /path/items.csv]
//
// 输出（markdown 到 stdout，--out 另存）：
//   1. 每题：均分 / 标准差 / 满分率（天花板）/ 零分率（地板）/ 题总相关（r_it）
//   2. 三模型逐题均分与极差（区分度）——极差 ≥ 0.5 的题才拉得开
//   3. 题间相关 |r| ≥ 0.7 的冗余对
//   4. 证据质量：有多少题的证据指到了「第 N 屏」
//   5. 按模型的总分对照（含 v1 fixed20 同 run 的分，看差距是否被放大）
// 只读打开 sqlite（WAL，mode=ro）；不写库。
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { DatabaseSync } from "node:sqlite";

const here = path.dirname(fileURLToPath(import.meta.url));
const args = Object.fromEntries(
  process.argv.slice(2).map((arg, index, all) => arg.startsWith("--")
    ? [arg.slice(2), all[index + 1] && !all[index + 1].startsWith("--") ? all[index + 1] : "1"]
    : []).filter((pair) => pair.length)
);
const method = args.method || "fixed_v3pool";
const dbPath = args.db || path.join(here, "..", "storage", "ui-eval.sqlite3");
const db = new DatabaseSync(dbPath, { readOnly: true });

const { getScaleMethod } = await import("../server/fixed_scales/index.mjs");
const def = getScaleMethod(method);
if (!def) { console.error(`未知量表 ${method}`); process.exit(2); }
const questions = def.questions;
const keys = questions.map((question) => question.key);

const modelFilter = args.models ? args.models.split(",").map((s) => s.trim()) : null;
const testFilter = args.tests ? args.tests.split(",").map((s) => s.trim()) : null;

const rows = db.prepare(`
  SELECT s.run_id, s.cc_values, s.human_values, s.evidence, s.total, s.cc_total, s.g0_pass, s.parse_error,
         m.name AS model, t.code AS test_code, t.title AS test_title, s.eval_model_id
  FROM scale_scores s
  LEFT JOIN models m ON m.id = s.model_id
  LEFT JOIN tests t ON t.id = s.test_id
  WHERE s.method = ? AND s.is_baseline = 1 AND s.status = '已完成'
`).all(method)
  .filter((row) => !modelFilter || modelFilter.includes(row.model))
  .filter((row) => !testFilter || testFilter.includes(row.test_code));
if (rows.length < 3) { console.error(`${method} 只有 ${rows.length} 条基准分，不够分析`); process.exit(1); }

const parse = (text, fallback) => { try { return JSON.parse(text || ""); } catch { return fallback; } };
const samples = rows.map((row) => {
  const cc = parse(row.cc_values, {});
  const human = parse(row.human_values, {});
  const values = {};
  for (const key of keys) values[key] = Number.isFinite(Number(human[key])) ? Number(human[key]) : Number(cc[key] ?? NaN);
  return { ...row, values, evidence: parse(row.evidence, {}) };
});

const mean = (xs) => xs.reduce((a, b) => a + b, 0) / (xs.length || 1);
const sd = (xs) => { const m = mean(xs); return Math.sqrt(mean(xs.map((x) => (x - m) ** 2))); };
const pearson = (xs, ys) => {
  const mx = mean(xs), my = mean(ys);
  const num = xs.reduce((sum, x, i) => sum + (x - mx) * (ys[i] - my), 0);
  const den = Math.sqrt(xs.reduce((s, x) => s + (x - mx) ** 2, 0) * ys.reduce((s, y) => s + (y - my) ** 2, 0));
  return den ? num / den : 0;
};
const fmt = (x, digits = 2) => Number.isFinite(x) ? x.toFixed(digits) : "—";

const totals = samples.map((sample) => keys.reduce((sum, key) => sum + (sample.values[key] || 0), 0));
const models = [...new Set(samples.map((sample) => sample.model))];
const lines = [];
lines.push(`# 题项分析 · ${def.name}（${method}）`);
lines.push("");
lines.push(`样本：${samples.length} 条基准分 · 模型 ${models.join(" / ")} · 测试 ${[...new Set(samples.map((s) => s.test_code))].join(", ")}`);
lines.push(`评分模型：${[...new Set(samples.map((s) => s.eval_model_id))].join(", ")} · 漏题记录 ${samples.filter((s) => s.parse_error).length} 条`);
lines.push("");

// 1. 每题统计
lines.push("## 1. 每题：均分 / sd / 满分率 / 零分率 / 题总相关");
lines.push("");
lines.push("| 题 | 维度 | 层 | 均分 | sd | 满分率 | 零分率 | r_it | 判定 |");
lines.push("|---|---|---|---|---|---|---|---|---|");
const itemStats = {};
for (const question of questions) {
  const xs = samples.map((s) => s.values[question.key]).filter(Number.isFinite);
  const m = mean(xs), s = sd(xs);
  // 满分档按题各自的满分算（v4 的信息组织、布局质量是 0-3）
  const ceiling = xs.filter((x) => x === (question.max ?? 2)).length / xs.length;
  const floor = xs.filter((x) => x === 0).length / xs.length;
  const rest = samples.map((sample) => totals[samples.indexOf(sample)] - (sample.values[question.key] || 0));
  const rit = pearson(xs, rest);
  itemStats[question.key] = { mean: m, sd: s, ceiling, floor, rit };
  const flags = [];
  if (ceiling >= 0.85) flags.push("天花板");
  if (floor >= 0.85) flags.push("地板");
  if (s < 0.3) flags.push("无变异");
  if (rit < 0.1 && s >= 0.3) flags.push("与总分无关");
  lines.push(`| ${question.key} | ${question.dimension} | ${question.layer || ""} | ${fmt(m)} | ${fmt(s)} | ${Math.round(ceiling * 100)}% | ${Math.round(floor * 100)}% | ${fmt(rit)} | ${flags.join("、")} |`);
}
lines.push("");

// 2. 按模型逐题
lines.push("## 2. 各模型逐题均分与极差（区分度）");
lines.push("");
lines.push(`| 题 | ${models.join(" | ")} | 极差 | 判定 |`);
lines.push(`|---|${models.map(() => "---").join("|")}|---|---|`);
const gapOf = {};
for (const question of questions) {
  const means = models.map((model) => mean(samples.filter((s) => s.model === model).map((s) => s.values[question.key]).filter(Number.isFinite)));
  const gap = Math.max(...means) - Math.min(...means);
  gapOf[question.key] = gap;
  lines.push(`| ${question.key} | ${means.map((x) => fmt(x)).join(" | ")} | ${fmt(gap)} | ${gap >= 0.5 ? "**拉得开**" : gap >= 0.25 ? "一般" : "拉不开"} |`);
}
lines.push("");
lines.push("### 各模型总分");
lines.push("");
lines.push(`| 模型 | n | 均分 / ${def.max} | 归一化 % | v1 同 run 均分 / 40 | v1 归一化 % |`);
lines.push("|---|---|---|---|---|---|");
const v1 = db.prepare(`SELECT run_id, total FROM scale_scores WHERE method = 'fixed20' AND is_baseline = 1 AND status = '已完成'`).all();
const v1Of = Object.fromEntries(v1.map((row) => [row.run_id, row.total]));
for (const model of models) {
  const mine = samples.filter((s) => s.model === model);
  const t = mine.map((s) => totals[samples.indexOf(s)]);
  const old = mine.map((s) => v1Of[s.run_id]).filter(Number.isFinite);
  lines.push(`| ${model} | ${mine.length} | ${fmt(mean(t), 1)} ± ${fmt(sd(t), 1)} | ${fmt(mean(t) / def.max * 100, 1)}% | ${old.length ? fmt(mean(old), 1) : "—"} | ${old.length ? fmt(mean(old) / 40 * 100, 1) + "%" : "—"} |`);
}
lines.push("");

// 3. 题间相关
lines.push("## 3. 题间相关 |r| ≥ 0.7（疑似重复）");
lines.push("");
const pairs = [];
for (let i = 0; i < keys.length; i += 1) {
  for (let j = i + 1; j < keys.length; j += 1) {
    const xs = samples.map((s) => s.values[keys[i]]);
    const ys = samples.map((s) => s.values[keys[j]]);
    if (sd(xs) < 1e-9 || sd(ys) < 1e-9) continue;
    const r = pearson(xs, ys);
    if (Math.abs(r) >= 0.7) pairs.push({ a: keys[i], b: keys[j], r });
  }
}
pairs.sort((l, r) => Math.abs(r.r) - Math.abs(l.r));
if (!pairs.length) lines.push("（无）");
else {
  lines.push("| 题 A | 题 B | r | A 题干 | B 题干 |");
  lines.push("|---|---|---|---|---|");
  for (const pair of pairs) {
    const qa = questions.find((q) => q.key === pair.a), qb = questions.find((q) => q.key === pair.b);
    lines.push(`| ${pair.a} | ${pair.b} | ${fmt(pair.r)} | ${qa.text.slice(0, 28)}… | ${qb.text.slice(0, 28)}… |`);
  }
}
lines.push("");

// 4. 证据质量
lines.push("## 4. 证据质量（证据里指到「第 N 屏」的比例）");
lines.push("");
const located = {};
for (const question of questions) {
  const ev = samples.map((s) => String(s.evidence[question.key] || ""));
  located[question.key] = ev.filter((text) => /第\s*\d+\s*屏/.test(text)).length / ev.length;
}
const weak = questions.filter((q) => located[q.key] < 0.6).map((q) => `${q.key}（${Math.round(located[q.key] * 100)}%）`);
lines.push(`整体：${Math.round(mean(Object.values(located)) * 100)}% 的题证据指到了屏；低于 60% 的题：${weak.length ? weak.join("、") : "无"}`);
lines.push("");

// 5. 综合建议
lines.push("## 5. 综合建议（机械规则，最终取舍仍要人看）");
lines.push("");
const keep = [], merge = [], drop = [];
for (const question of questions) {
  const st = itemStats[question.key];
  const dup = pairs.find((p) => p.a === question.key || p.b === question.key);
  if (st.ceiling >= 0.85 || st.floor >= 0.85 || st.sd < 0.3) drop.push(`${question.key}（${st.ceiling >= 0.85 ? "天花板" : st.floor >= 0.85 ? "地板" : "无变异"}）`);
  else if (dup) merge.push(`${question.key}↔${dup.a === question.key ? dup.b : dup.a}（r=${fmt(dup.r)}）`);
  else if (gapOf[question.key] >= 0.5) keep.push(`${question.key}（极差 ${fmt(gapOf[question.key])}）`);
}
lines.push(`- **优先保留（拉得开）**：${keep.join("、") || "无"}`);
lines.push(`- **考虑合并**：${merge.join("、") || "无"}`);
lines.push(`- **考虑删除**：${drop.join("、") || "无"}`);
lines.push("");

const report = lines.join("\n");
console.log(report);
if (args.out) fs.writeFileSync(args.out, report);
if (args.csv) {
  const header = ["key", "dimension", "layer", "mean", "sd", "ceiling", "floor", "r_it", "gap", "located", ...models.map((m) => `mean_${m}`)];
  const csv = [header.join(",")];
  for (const question of questions) {
    const st = itemStats[question.key];
    csv.push([
      question.key, question.dimension, question.layer || "", fmt(st.mean), fmt(st.sd), fmt(st.ceiling), fmt(st.floor), fmt(st.rit),
      fmt(gapOf[question.key]), fmt(located[question.key]),
      ...models.map((model) => fmt(mean(samples.filter((s) => s.model === model).map((s) => s.values[question.key]).filter(Number.isFinite))))
    ].map((v) => `"${String(v).replaceAll('"', '""')}"`).join(","));
  }
  fs.writeFileSync(args.csv, `﻿${csv.join("\n")}`);
}
