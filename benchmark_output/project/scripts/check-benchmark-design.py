#!/usr/bin/env python3
"""Save read-only page snapshots for every file in the fresh benchmark manifest."""
import argparse
import asyncio
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "server"))
from benchmark_fixture import inspect


async def check(args):
    raw = args.manifest.read_bytes()
    manifest = json.loads(raw)
    result = {"manifest_sha256": hashlib.sha256(raw).hexdigest(), "read_only": True, "files": []}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    for group in manifest["groups"]:
        for task in group["tests"]:
            record = {"task": group["task"], "question": task["question"], "file_key": task["file_key"],
                      "checked_at": datetime.now(timezone.utc).isoformat()}
            try:
                record["snapshot"] = await asyncio.wait_for(inspect(args.mcp_config, task["file_key"], args.artifacts), 120)
            except Exception as error:
                record["error_type"] = type(error).__name__
            result["files"].append(record)
            temporary = args.output.with_suffix(".tmp")
            temporary.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
            temporary.chmod(0o600)
            temporary.replace(args.output)
            print(json.dumps(record, ensure_ascii=False), flush=True)
            await asyncio.sleep(args.interval)
    if any("snapshot" not in record for record in result["files"]):
        raise SystemExit("Some files could not be inspected; see the saved report")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=ROOT / "storage/benchmark-design/inputs.json")
    parser.add_argument("--output", type=Path, default=ROOT / "storage/benchmark-design/fresh-preflight-20261026.json")
    parser.add_argument("--mcp-config", required=True)
    parser.add_argument("--interval", type=float, default=6)
    parser.add_argument("--artifacts", action="store_true", help="Also inspect existing Workspace frames and the task brief without writing")
    asyncio.run(check(parser.parse_args()))
