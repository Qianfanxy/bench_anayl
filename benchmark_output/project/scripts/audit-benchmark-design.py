#!/usr/bin/env python3
"""Offline evidence: separate model requests, failed tools and actual design artifacts."""
import collections
import json
from pathlib import Path
import re
import sqlite3

ROOT = Path(__file__).resolve().parents[1] / "storage/benchmark-design"
QUOTA = re.compile(r"you.ve reached the Figma MCP tool call limit|too many requests|rate limit exceeded", re.I)


def records(directory):
    trace = directory / "task-000001/trace.sqlite3"
    if not trace.exists():
        return
    connection = sqlite3.connect(f"file:{trace.resolve()}?mode=ro", uri=True)
    if not connection.execute("SELECT 1 FROM sqlite_master WHERE name='records'").fetchone():
        return
    for payload, in connection.execute("SELECT payload_json FROM records ORDER BY record_index"):
        stored = json.loads(payload)
        record = stored.get("record", stored)
        for ref in stored.get("__claude_tap_compact_record__", {}).get("refs", []):
            if not ref["path"].startswith("/request/body/messages"):
                continue
            blob = connection.execute("SELECT payload_json FROM record_blobs WHERE hash=?", (ref["hash"],)).fetchone()
            if not blob:
                continue
            parts = ref["path"].strip("/").split("/")
            node = record
            for part in parts[:-1]:
                node = node[int(part)] if isinstance(node, list) else node[part]
            node[int(parts[-1]) if isinstance(node, list) else parts[-1]] = json.loads(blob[0])
        yield record


def tool_messages(record):
    for message in record.get("request", {}).get("body", {}).get("messages", []):
        for part in message.get("content", []) if isinstance(message.get("content"), list) else []:
            if part.get("type") == "tool_result":
                content = part.get("content", "")
                text = content if isinstance(content, str) else "\n".join(p.get("text", "") for p in content)
                yield part["tool_use_id"], {"content": text, "success": not part.get("is_error", False)}


def main():
    db = sqlite3.connect(f"file:{(ROOT/'ui-eval.sqlite3').resolve()}?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    snapshots_file = ROOT / "artifact-audit-20261026.json"
    snapshots = json.loads(snapshots_file.read_text())["files"] if snapshots_file.exists() else []
    by_key = {r["file_key"]: r.get("snapshot") for r in snapshots}
    report = []
    for row in db.execute("SELECT r.*,t.title,t.base_figma_url target_url FROM runs r JOIN tests t ON t.id=r.test_id ORDER BY r.started_at"):
        item = {key: row[key] for key in ["id", "test_id", "model_id", "title", "status", "error", "frames_error"]}
        key = re.search(r"/design/([A-Za-z0-9]+)", row["target_url"])[1]
        item["file_key"] = key
        item["artifact"] = by_key.get(key)
        item["model_started"] = bool(row["run_dir"])
        results = {}
        statuses = collections.Counter()
        last_usage = {}
        if row["run_dir"]:
            directory = Path(row["run_dir"])
            trajectory = directory / "task-000001/trajectory.jsonl"
            if trajectory.exists():
                messages = json.loads(trajectory.open().readline()).get("messages", [])
                for index, message in enumerate(messages):
                    if message.get("role") == "tool":
                        results[message.get("tool_call_id", str(index))] = message
                final = [m.get("content", "") for m in messages if m.get("role") == "assistant" and m.get("content")]
                item["final_response"] = final[-1] if final else ""
            else:
                for record in records(directory):
                    results.update(tool_messages(record))
            for record in records(directory):
                response = record.get("response", {})
                statuses[str(response.get("status", "unknown"))] += 1
                body = response.get("body", {})
                if isinstance(body, dict) and isinstance(body.get("usage"), dict):
                    last_usage = body["usage"]
            quota = [r for r in results.values() if QUOTA.search(str(r.get("content", "")))]
            errors = [r for r in results.values() if r.get("success") is False]
            item.update(tool_results=len(results), quota_errors=len(quota), tool_errors=len(errors),
                quota_examples=[str(r["content"])[:350] for r in quota[:2]],
                api_statuses=dict(statuses), last_request_usage=last_usage,
                saved_images=len(list((directory / "task-000001/media").glob("*.png"))))
        report.append(item)
    output = ROOT / "failure-attribution-20261026.json"
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    output.chmod(0o600)
    for item in report:
        workspace = (item.get("artifact") or {}).get("workspace") or {}
        frames = [n for n in workspace.get("children", []) if n["type"] == "FRAME"]
        print(item["title"], "started=" + str(item["model_started"]), "frames=" + str(len(frames)),
              "quota_errors=" + str(item.get("quota_errors", 0)), "api=" + str(item.get("api_statuses", {})))


if __name__ == "__main__":
    main()
