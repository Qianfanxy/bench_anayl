#!/usr/bin/env node
// 给评测页截图的小工具（用 Chrome DevTools Protocol）。
//
// Chrome 自带的 --screenshot 只能拍首屏静态渲染，对这个页面不够用：
//   1. 开局就被「填写评测姓名」弹窗挡住，姓名存在 localStorage 里，必须先注入；
//   2. 要看某条 run 的生成结果/轨迹，得先点开它，静态截图点不了。
// 所以这里连上 CDP，注入 localStorage、执行任意点击脚本，再截图。
//
// 用法：
//   node scripts/ui-shot.mjs --out /tmp/a.png [--url ...] [--reviewer 姓名]
//                            [--eval "<在页面里执行的 JS>"] [--wait 8000]
//                            [--width 1600] [--height 1000] [--full-page]
import { spawn } from "node:child_process";
import fs from "node:fs";

const CHROME = process.env.UI_SHOT_CHROME
  || ["/root/.cache/ms-playwright", "/mnt/afs/panzhengyuan/.cache/ms-playwright"]
    .map((root) => `${root}/chromium-1228/chrome-linux64/chrome`).find((file) => fs.existsSync(file))
  || "/mnt/afs/panzhengyuan/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome"; // 容器重置会清掉 /root，afs 上那份是持久的

function parseArgs(argv) {
  const out = { flags: new Set() };
  for (let i = 0; i < argv.length; i += 1) {
    const token = argv[i];
    if (!token.startsWith("--")) continue;
    const name = token.slice(2);
    const next = argv[i + 1];
    if (next === undefined || next.startsWith("--")) {
      out.flags.add(name);
    } else {
      out[name] = next;
      i += 1;
    }
  }
  return out;
}

const args = parseArgs(process.argv.slice(2));
const url = args.url || "http://127.0.0.1:4173/";
const outFile = args.out;
const reviewer = args.reviewer || "系统验证";
const waitMs = Number(args.wait || 8000);
const width = Number(args.width || 1600);
const height = Number(args.height || 1000);
const fullPage = args.flags.has("full-page");
const debugPort = Number(args.port || 9333);

if (!outFile) {
  console.error("必须给 --out <png 路径>");
  process.exit(2);
}

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function waitForDevtools(port, timeoutMs = 20000) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    try {
      const response = await fetch(`http://127.0.0.1:${port}/json/version`);
      if (response.ok) return await response.json();
    } catch { /* Chrome 还没起来 */ }
    await sleep(200);
  }
  throw new Error("Chrome 的调试端口一直没起来");
}

class Cdp {
  constructor(socket) {
    this.socket = socket;
    this.nextId = 1;
    this.pending = new Map();
    this.events = [];
    socket.addEventListener("message", (event) => {
      const message = JSON.parse(event.data);
      if (message.id && this.pending.has(message.id)) {
        const { resolve, reject } = this.pending.get(message.id);
        this.pending.delete(message.id);
        if (message.error) reject(new Error(JSON.stringify(message.error)));
        else resolve(message.result);
        return;
      }
      if (message.method) this.events.push(message.method);
    });
  }

  send(method, params = {}) {
    const id = this.nextId++;
    this.socket.send(JSON.stringify({ id, method, params }));
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      setTimeout(() => {
        if (this.pending.delete(id)) reject(new Error(`${method} 超时`));
      }, 60000);
    });
  }

  async evaluate(expression) {
    const result = await this.send("Runtime.evaluate", {
      expression,
      awaitPromise: true,
      returnByValue: true,
    });
    if (result.exceptionDetails) {
      throw new Error(`页面里执行 JS 出错：${result.exceptionDetails.text}`);
    }
    return result.result?.value;
  }
}

const chrome = spawn(CHROME, [
  "--headless=new",
  "--no-sandbox",
  "--disable-gpu",
  "--disable-dev-shm-usage",
  "--hide-scrollbars",
  `--remote-debugging-port=${debugPort}`,
  `--window-size=${width},${height}`,
  "--user-data-dir=/tmp/ui-shot-profile",
  "about:blank",
], { stdio: ["ignore", "ignore", "ignore"] });

let socket;
try {
  await waitForDevtools(debugPort);
  const target = await (await fetch(
    `http://127.0.0.1:${debugPort}/json/new?${encodeURIComponent(url)}`,
    { method: "PUT" }
  )).json();

  socket = new WebSocket(target.webSocketDebuggerUrl);
  await new Promise((resolve, reject) => {
    socket.addEventListener("open", resolve, { once: true });
    socket.addEventListener("error", () => reject(new Error("CDP 连接失败")), { once: true });
  });
  const cdp = new Cdp(socket);
  await cdp.send("Page.enable");
  await cdp.send("Runtime.enable");
  await cdp.send("Emulation.setDeviceMetricsOverride", {
    width, height, deviceScaleFactor: 1, mobile: false,
  });

  await cdp.send("Page.navigate", { url });
  await sleep(2500);
  // 姓名弹窗挡住整页，先把评测人身份塞进 localStorage 再刷新
  await cdp.evaluate(`
    localStorage.setItem("ui-eval-reviewer", ${JSON.stringify(reviewer)});
    if (!localStorage.getItem("ui-eval-reviewer-id")) {
      localStorage.setItem("ui-eval-reviewer-id", "ui-shot-" + Math.random().toString(16).slice(2));
    }
    true;
  `);
  await cdp.send("Page.reload");
  await sleep(waitMs);

  if (args.eval) {
    const value = await cdp.evaluate(args.eval);
    if (value !== undefined) console.error(`[eval] ${JSON.stringify(value)}`);
    await sleep(Number(args["eval-wait"] || 4000));
  }

  const shotParams = { format: "png" };
  if (fullPage) {
    const metrics = await cdp.send("Page.getLayoutMetrics");
    const size = metrics.cssContentSize || metrics.contentSize;
    shotParams.captureBeyondViewport = true;
    shotParams.clip = {
      x: 0, y: 0, width: size.width, height: size.height, scale: 1,
    };
  }
  const shot = await cdp.send("Page.captureScreenshot", shotParams);
  fs.writeFileSync(outFile, Buffer.from(shot.data, "base64"));
  console.log(`已截图 -> ${outFile}`);
} finally {
  try { socket?.close(); } catch { /* 已断开 */ }
  chrome.kill("SIGKILL");
}
