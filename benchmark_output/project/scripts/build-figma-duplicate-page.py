#!/usr/local/bin/python3
"""生成「逐个复制 Figma 文件」的静态页(public/ 与 dist/ 各一份,express.static 按请求读盘,不用重启)。

Figma 没有可编程的"复制文件"入口(MCP 无此工具、REST 无此端点、服务器访问 figma.com/design/* 被 CloudFront 拦),
只能靠网页端的 /duplicate 链接:在**已登录 Figma 的浏览器**里打开就会在该账号草稿里建一份副本。
本脚本只读库、不调 Figma、不占配额。重跑即刷新清单。
"""
import html, json, re, sqlite3, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
db = sqlite3.connect(f"file:{ROOT/'storage/ui-eval.sqlite3'}?mode=ro", uri=True)
rows = db.execute("""
  SELECT r.id, t.code, t.title, COALESCE(m.name, r.model_id), r.status, r.figma_url, r.started_at, r.young_mode
  FROM runs r LEFT JOIN tests t ON t.id = r.test_id LEFT JOIN models m ON m.id = r.model_id
  WHERE r.figma_url != '' AND r.status IN ('等待评分','结果不完整')
    AND COALESCE(r.command_preview,'') NOT LIKE '%生产端%'
  ORDER BY r.started_at DESC""").fetchall()

seen, items = set(), []
for rid, code, title, model, status, url, started, young in rows:
    m = re.search(r"figma\.com/(?:design|file)/([A-Za-z0-9]+)", url or "")
    if not m or m.group(1) in seen:
        continue
    seen.add(m.group(1))
    items.append({"run": rid, "code": code or "", "title": title or "", "model": model or "",
                  "status": status, "key": m.group(1), "at": (started or "")[:16].replace("T", " "),
                  "young": bool(young)})

page = """<!doctype html><html lang="zh"><head><meta charset="utf-8"><title>逐个复制 Figma 文件</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{font:14px/1.6 -apple-system,"PingFang SC",sans-serif;margin:0;background:#f6f7f9;color:#1f2329}
main{max-width:1100px;margin:0 auto;padding:24px 16px}
h1{font-size:20px;margin:0 0 8px}.tip{background:#fff;border:1px solid #e5e6eb;border-radius:8px;padding:12px 16px;margin-bottom:16px}
.tip b{color:#d4380d}.bar{display:flex;gap:8px;flex-wrap:wrap;align-items:center;margin-bottom:12px}
input,select,button{font:inherit;padding:6px 10px;border:1px solid #c9cdd4;border-radius:6px;background:#fff}
button{cursor:pointer}button.primary{background:#3370ff;color:#fff;border-color:#3370ff}
table{width:100%;border-collapse:collapse;background:#fff;border-radius:8px;overflow:hidden}
th,td{padding:8px 10px;border-bottom:1px solid #eff0f1;text-align:left;vertical-align:middle}
th{background:#fafafa;font-weight:600}tr.done{opacity:.45}tr.next{background:#f0f5ff}
.young{color:#722ed1;font-size:12px;margin-left:4px}td.url input{width:260px}a{color:#3370ff}
</style></head><body><main>
<h1>逐个复制 Figma 文件</h1>
<div class="tip">
① 先在这个浏览器里登录 Figma,而且必须是<b>评测端在用的那个账号(Xinya Liu / xinya-old)</b>——
源文件是它建的,别的账号打不开;副本也要落在它名下,平台之后才改得动。<br>
② 点「复制」会新开一个标签页,Figma 在草稿里建好副本后地址栏就是新文件的 URL。浏览器一次点击只放行一个弹窗,所以只能一条一条点;
「复制下一条」(或按 <b>N</b> 键)会自动找到下一条没点过的。<br>
③ 需要让平台认这份副本时,把新 URL 贴到右边的框里(只存在本浏览器里),最后点「导出对照表」交给我。
</div>
<div class="bar">
<button class="primary" id="next">复制下一条 (N)</button>
<input id="q" placeholder="筛选:测试编号 / 标题 / 模型" size="28">
<label><input type="checkbox" id="hide"> 隐藏已点过的</label>
<span id="stat"></span><span style="flex:1"></span>
<button id="export">导出对照表</button><button id="reset">清空记录</button>
</div>
<table><thead><tr><th>测试</th><th>模型</th><th>状态</th><th>时间</th><th>原文件</th><th>操作</th><th>副本 URL</th></tr></thead><tbody id="tb"></tbody></table>
</main><script>
const ITEMS = __ITEMS__;
const KEY = "figma-duplicate-state-v1";
let state = {}; try { state = JSON.parse(localStorage.getItem(KEY) || "{}"); } catch {}
const save = () => { try { localStorage.setItem(KEY, JSON.stringify(state)); } catch {} };
const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
const dupUrl = (k) => "https://www.figma.com/file/" + k + "/duplicate";
function visible() {
  const q = document.getElementById("q").value.trim().toLowerCase();
  const hide = document.getElementById("hide").checked;
  return ITEMS.filter((it) => (!q || (it.code + it.title + it.model).toLowerCase().includes(q)) && !(hide && state[it.key]?.opened));
}
function render() {
  const list = visible();
  const nextKey = list.find((it) => !state[it.key]?.opened)?.key;
  document.getElementById("tb").innerHTML = list.map((it) => {
    const st = state[it.key] || {};
    return `<tr class="${st.opened ? "done" : ""} ${it.key === nextKey ? "next" : ""}">
      <td><b>${esc(it.code)}</b> ${esc(it.title)}${it.young ? '<span class="young">young</span>' : ""}</td>
      <td>${esc(it.model)}</td><td>${esc(it.status)}</td><td>${esc(it.at)}</td>
      <td><a href="https://www.figma.com/design/${it.key}" target="_blank" rel="noopener">${it.key.slice(0, 8)}…</a></td>
      <td><button data-dup="${it.key}">${st.opened ? "再复制一次" : "复制"}</button></td>
      <td class="url"><input data-url="${it.key}" value="${esc(st.copy || "")}" placeholder="贴副本的 URL"></td></tr>`;
  }).join("");
  const opened = ITEMS.filter((it) => state[it.key]?.opened).length;
  document.getElementById("stat").textContent = `共 ${ITEMS.length} 个文件,已点 ${opened},已填副本 ${ITEMS.filter((it) => state[it.key]?.copy).length}`;
}
function dup(key) {
  window.open(dupUrl(key), "_blank", "noopener");
  state[key] = { ...(state[key] || {}), opened: Date.now() }; save(); render();
}
document.getElementById("tb").addEventListener("click", (e) => { const k = e.target.dataset?.dup; if (k) dup(k); });
document.getElementById("tb").addEventListener("change", (e) => {
  const k = e.target.dataset?.url; if (!k) return;
  state[k] = { ...(state[k] || {}), copy: e.target.value.trim() }; save(); render();
});
const next = () => { const it = visible().find((x) => !state[x.key]?.opened); if (it) dup(it.key); };
document.getElementById("next").onclick = next;
document.addEventListener("keydown", (e) => { if ((e.key === "n" || e.key === "N") && e.target.tagName !== "INPUT") next(); });
document.getElementById("q").oninput = render; document.getElementById("hide").onchange = render;
document.getElementById("reset").onclick = () => { if (confirm("清空本浏览器里的点击与副本记录?")) { state = {}; save(); render(); } };
document.getElementById("export").onclick = () => {
  const rows = ITEMS.filter((it) => state[it.key]?.copy).map((it) => ({ run: it.run, code: it.code, source: it.key, copy: state[it.key].copy }));
  const a = document.createElement("a");
  a.href = URL.createObjectURL(new Blob([JSON.stringify(rows, null, 2)], { type: "application/json" }));
  a.download = "figma-copies.json"; a.click();
};
render();
</script></body></html>"""
out = page.replace("__ITEMS__", json.dumps(items, ensure_ascii=False).replace("</", "<\\/"))
for d in ("public", "dist"):
    p = ROOT / d / "figma-duplicate.html"
    p.parent.mkdir(exist_ok=True)
    p.write_text(out, encoding="utf-8")
print(f"{len(items)} 个文件(去重前 {len(rows)} 条 run) → /figma-duplicate.html")
