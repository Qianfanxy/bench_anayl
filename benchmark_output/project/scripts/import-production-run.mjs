#!/usr/bin/env node
// 把生产端批次里跑出来的设计搬进评测端，作为历史记录展示。
//
// 生产端产物和评测端的目录约定不一样：轨迹里的图片路径是相对**批次根目录**的
// （accounts/<账号>/runs/<run>/task-000001/media/…），直接复制过来，评测端按
// storage/runs 为基准去找就全都对不上，质检会报 "missing or invalid PNG"。
// 所以复制之后不手工改路径，而是让评测端自己的 reimport 从 trace.sqlite3 重新
// 导出一遍——导出时用的就是评测端的 media-prefix，路径天然是对的，
// 顺带还走了归一化、质检、figma_url 提取那一整套，状态由真实逻辑判定。
//
// 用法：node scripts/import-production-run.mjs <配置json>
// 配置格式：[{ "src": "生产端运行目录绝对路径", "code": "PROD-001", "title": "外卖点餐App s3l2v3" }]
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const here = path.dirname(fileURLToPath(import.meta.url));
const appRoot = path.resolve(here, "..");
const API = process.env.UI_EVAL_API || "http://127.0.0.1:4173/api";
const runRoot = path.join(appRoot, "storage", "runs");
// 复用测试时的身份标记：只认本脚本建的，别挂到同名的人工测试上
const IMPORTER = "生产端迁移";

const configPath = process.argv[2];
if (!configPath) {
  console.error("用法: node scripts/import-production-run.mjs <配置json>");
  process.exit(2);
}
const items = JSON.parse(fs.readFileSync(configPath, "utf8"));

async function api(route, options = {}) {
  const response = await fetch(`${API}${route}`, {
    headers: { "content-type": "application/json" },
    ...options,
  });
  const body = await response.json().catch(() => ({}));
  if (!response.ok || body.ok === false) {
    throw new Error(`${route} -> ${response.status} ${body.message || ""}`);
  }
  return body;
}

// prompt.txt 开头是流水线加的那句「请使用 Figma MCP，在 sensetime 团队…新建一个
// design 文件，名称为「…」。」。评测用不上它，留着还会让自动生成的检查点去考
// "有没有建文件"，而不是考设计本身。
function designQuery(promptFile) {
  const raw = fs.readFileSync(promptFile, "utf8").trim();
  const cut = raw.indexOf("\n\n");
  return (cut > 0 && raw.slice(0, cut).includes("Figma MCP") ? raw.slice(cut + 2) : raw).trim();
}

// 配置支持两种写法：
//   一条一个 test:  [{ "src": "...", "title": "..." }]
//   一个 test 挂多条: [{ "title": "极简天气App", "runs": [{ "src": "...", "label": "插画风·Bento v2" }] }]
function normalizeGroups(raw) {
  return raw.map((item) => (Array.isArray(item.runs)
    ? item
    : { title: item.title || path.basename(item.src), runs: [{ ...item, label: item.title }] }));
}

for (const group of normalizeGroups(items)) {
  const title = group.title;
  try {
    for (const entry of group.runs) {
      if (!fs.existsSync(path.join(entry.src, "task-000001", "trace.sqlite3"))) {
        throw new Error(`${entry.src} 里没有 trace.sqlite3`);
      }
    }
    const queries = group.runs.map((entry) =>
      designQuery(path.join(entry.src, "task-000001", "prompt.txt")));

    // 1) 建测试。同名已存在就复用——这个脚本要能重跑，不该每次堆一份新的 100 检查点。
    //    但只认**本脚本自己建的**：评测端可能早就有同名的人工测试（实测撞上了刘新雅
    //    7/31 建的「打卡App(员工端)」），挂上去等于拿她那份 query 生成的检查点来评
    //    这几条，还污染了她的测试。
    let test = (await api("/bootstrap")).tests
      .find((item) => item.title === title && item.created_by === IMPORTER);
    if (test) {
      console.log(`[${title}] 复用已存在的测试 ${test.code}`);
    } else {
      // 多个变体挂同一个 test 时，检查点必须照"共同要求"生成。直接用其中一条的 query，
      // 别的变体会因为"没用它要求的 Bento Grid"被白白扣分。
      let query = queries[0];
      if (queries.length > 1) {
        process.stdout.write(`[${title}] 合并 ${queries.length} 份 query…`);
        // 模型偶尔会只回一段散文而不是 JSON（实测第一次就撞上了），重试一次
        for (let attempt = 0; attempt < 2; attempt += 1) {
          try {
            query = (await api("/queries/merge", {
              method: "POST",
              body: JSON.stringify({ queries }),
            })).query;
            break;
          } catch (error) {
            if (attempt) throw error;
            process.stdout.write(" 没照做，重试…");
          }
        }
        process.stdout.write(` ${query.length} 字\n`);
      }
      process.stdout.write(`[${title}] 生成检查点…`);
      let generated;
      for (let attempt = 0; attempt < 2 && !generated; attempt += 1) {
        try {
          generated = await api("/criteria/generate", {
            method: "POST",
            body: JSON.stringify({ query }),
          });
        } catch (error) {
          if (attempt) throw error;
          process.stdout.write(" 超时，重试…");
        }
      }
      test = await api("/tests", {
        method: "POST",
        body: JSON.stringify({
          title,
          query,
          criteria_mode: "claude",
          criteria: generated.criteria,
          created_by: IMPORTER,
        }),
      });
      process.stdout.write(` ${generated.criteria.length} 条\n`);
      test = (await api("/bootstrap")).tests.find((item) => item.id === test.id) || test;
    }

    for (const [index, entry] of group.runs.entries()) {
      const label = entry.label || path.basename(entry.src);
      // 按 run_dir 判重，不能按 test——同一个 test 下本来就要挂好几条
      const already = (await api("/bootstrap")).runs
        .some((run) => run.reviewer_name === label && run.test_id === test.id);
      if (already) {
        console.log(`  [${label}] 已导入，跳过`);
        continue;
      }
      // 2) 复制运行目录（源目录只读不动——生产端产物是原始证据）
      const runDir = path.join(runRoot, `${test.code || test.id}_${Date.now()}_${index}`);
      fs.cpSync(entry.src, runDir, { recursive: true });

      // 3) 落一条 run，再交给 reimport 走真实的导出/归一化/质检
      const run = await api("/runs/import", {
        method: "POST",
        body: JSON.stringify({
          test_id: test.id,
          run_dir: runDir,
          model_id: entry.model_id || group.model_id || null,
          reviewer_id: entry.reviewer_id || "prod-import",
          // 历史卡片上显示的就是这个名字。一个 test 下并排三条都叫"生产端迁移"分不清谁是谁，
          // 写变体标签才认得出来。
          reviewer_name: label,
          query: queries[index],
        }),
      });
      const result = await api(`/runs/${run.run_id}/reimport`, { method: "POST" });
      console.log(`  [${label}] ${result.status}${result.error ? ` · ${result.error.slice(0, 70)}` : ""}`);
    }
  } catch (error) {
    console.error(`[${title}] 失败：${error.message}`);
  }
}
