#!/usr/bin/env python3
"""Recover screenshots of terminal runs' existing Workspace screens without changing Figma."""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import re

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "server"))
from benchmark_frames import benchmark_product_frame
STORAGE = ROOT / "storage/benchmark-design"
DEPENDENCIES = ROOT.parent / "rate_website_figma-sft-cc-tap/storage/standalone-original-20261025"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-id", help="Recover one terminal run without touching other attempts")
    args = parser.parse_args()
    config = json.loads((DEPENDENCIES / "runtime-config.json").read_text())
    mcp = json.loads(Path(config["UI_EVAL_MCP_CONFIG_PATH"]).read_text())
    auth_file = mcp["mcpServers"]["figma"]["env"]["FIGMA_MCP_AUTH_FILE"]
    db = sqlite3.connect(f"file:{(STORAGE/'ui-eval.sqlite3').resolve()}?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    env = {**os.environ, "FIGMA_MCP_BUDGET_FILE": str(STORAGE / "private/figma-budget.json"), "FIGMA_MCP_MIN_INTERVAL": "4"}
    report = STORAGE / "frames-recovery-20261026.json"
    results = json.loads(report.read_text()) if report.exists() else []
    query = "SELECT r.id,r.run_dir,t.base_figma_url FROM runs r JOIN tests t ON t.id=r.test_id WHERE r.run_dir!='' AND r.status NOT IN ('运行中','补图中','已暂停','停止中')"
    if args.run_id:
        query += " AND r.id=?"
    query += " ORDER BY r.started_at"
    for row in db.execute(query, (args.run_id,) if args.run_id else ()):
        directory = Path(row["run_dir"])
        inventory = directory / "benchmark-artifact.json"
        if not inventory.exists():
            continue
        snapshot = json.loads(inventory.read_text())
        assigned = re.search(r"/design/([A-Za-z0-9]+)", row["base_figma_url"] or "")
        if not assigned or assigned.group(1) != snapshot.get("file_key"):
            raise SystemExit("Artifact file does not match the assigned benchmark target")
        expected = [n for n in (snapshot.get("workspace") or {}).get("children", [])
                    if benchmark_product_frame(n)]
        if not expected:
            continue
        output = directory / "figma-frames"
        manifest = output / "frames.json"
        saved = json.loads(manifest.read_text()) if manifest.exists() else []
        if {n["node_id"] for n in saved} == {n["id"] for n in expected} and all((output/n["file"]).exists() for n in saved):
            result = {"run_id": row["id"], "ok": True, "frames": len(saved), "figma_calls": 0}
        else:
            process = subprocess.run([config["UI_EVAL_PYTHON"], str(ROOT / "server/figma_page_frames.py"),
                "--file-key", snapshot["file_key"], "--out-dir", str(output), "--auth-file", auth_file,
                "--auth-lib", config["UI_EVAL_PRODUCTION_SERVER"], "--workspace-only", "--inventory-file", str(inventory),
                "--max-frames", "80", "--max-dimension", "32768"], env=env, capture_output=True, text=True, timeout=360)
            try:
                result = {"run_id": row["id"], **json.loads(process.stdout)}
            except ValueError:
                result = {"run_id": row["id"], "ok": False, "error": "Screenshot recovery did not return JSON"}
        result["checked_at"] = datetime.now(timezone.utc).isoformat()
        receipt = directory / "benchmark-frame-recovery.json"
        receipt.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
        receipt.chmod(0o600)
        results = [r for r in results if r["run_id"] != row["id"]] + [result]
        report.write_text(json.dumps(results, ensure_ascii=False, indent=2) + "\n")
        report.chmod(0o600)
        print(json.dumps(result, ensure_ascii=False), flush=True)
