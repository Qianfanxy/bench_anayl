"""Read-only: dump full text of the 00 (task) and 01 (foundations) pages of each source template.

usage: PYTHONPATH=<vendor> <venv python> extract_briefs.py <mcp-config> <out-dir> [file_key ...]
Without file keys, takes every source template from ../manifest.json. Existing outputs are skipped.
"""
import asyncio, json, os, sys
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

CODE = ("const out=[];for(const p of figma.root.children){if(!/^0[01]\\s*[·.\\-—]/.test(p.name))continue;await p.loadAsync();"
        "const texts=p.findAll(n=>n.type==='TEXT').map(n=>({id:n.id,name:n.name,x:Math.round(n.absoluteTransform[0][2]),y:Math.round(n.absoluteTransform[1][2]),text:n.characters}));"
        "texts.sort((a,b)=>a.y-b.y||a.x-b.x);out.push({page_id:p.id,page_name:p.name,texts});}"
        "return JSON.stringify({file_key:%s,file_name:figma.root.name,pages:out});")


async def main(cfg, out, keys):
    c = json.loads(Path(cfg).read_text())
    srv = c["mcpServers"][next(iter(c["mcpServers"]))] if "mcpServers" in c else c
    params = StdioServerParameters(command=srv["command"], args=srv.get("args", []), env={**os.environ, **srv.get("env", {}), "FIGMA_MCP_ALLOWED_TOOLS": "use_figma", "FIGMA_MCP_PIN_PAGE": "", "FIGMA_MCP_USAGE_PHASE": "source_check"})
    async with stdio_client(params) as (r, w):
        async with ClientSession(r, w) as s:
            await s.initialize()
            for k in keys:
                dest = out / f"{k}.json"
                if dest.exists(): continue
                res = await s.call_tool("use_figma", {"fileKey": k, "code": CODE % json.dumps(k), "skillNames": "resource:figma-use",
                                                      "description": "Read-only: read text of 00/01 reference pages; no edits"})
                txt = "\n".join(b.text for b in res.content if b.type == "text")
                try:
                    v = json.loads(txt); v = json.loads(v) if isinstance(v, str) else v
                    assert v["file_key"] == k and v["pages"]
                except Exception:
                    print("FAIL", k, txt[:300]); continue
                dest.write_text(json.dumps(v, ensure_ascii=False, indent=1))
                print("ok", k, v["file_name"], [(p["page_name"], len(p["texts"])) for p in v["pages"]])
                await asyncio.sleep(4)


if __name__ == "__main__":
    out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    keys = sys.argv[3:] or sorted({c["source_file_key"] for c in json.loads((Path(__file__).parent.parent / "manifest.json").read_text())["meta"]["cases"]})
    asyncio.run(main(sys.argv[1], out, keys))
