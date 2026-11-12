#!/usr/bin/env python3
"""Import fresh inputs and the previous model/criteria configuration into an unused benchmark DB."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parents[1]
TAG = "benchmark-design-fresh-20261026"
PREVIOUS = ROOT.parent / "rate_website_figma-sft-cc-tap/storage/standalone-original-20261025"


def import_inputs(args):
    manifest = json.loads(args.manifest.read_text())
    assert manifest["fresh_targets"] is True and manifest["query_modified"] is False
    assert len(manifest["groups"]) == 7 and all(len(g["tests"]) == 3 for g in manifest["groups"])
    args.database.parent.mkdir(parents=True, exist_ok=True)
    source = sqlite3.connect(f"file:{args.model_db.resolve()}?mode=ro", uri=True)
    source.row_factory = sqlite3.Row
    target = sqlite3.connect(args.database)
    target.row_factory = sqlite3.Row
    target.execute("PRAGMA foreign_keys=ON")
    if not target.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='tests'").fetchone():
        for row in source.execute("SELECT sql FROM sqlite_master WHERE sql IS NOT NULL AND type IN ('table','index') AND name NOT LIKE 'sqlite_%' ORDER BY type DESC"):
            target.execute(row[0])
    existing = target.execute("SELECT * FROM tests WHERE title LIKE ?", (TAG + "/%",)).fetchall()
    if existing:
        by_title = {r["title"]: r for r in existing}
        assert len(existing) == 21, "Partial import: inspect before continuing"
        for group in manifest["groups"]:
            for item in group["tests"]:
                row = by_title[f"{TAG}/{group['task']}/{item['question']}"]
                assert (row["query"], row["model_id"], row["base_figma_url"]) == (item["query"], group["model_id"], item["figma_url"])
        print("Existing 21 fresh inputs verified; no records changed")
        return
    assert target.execute("SELECT COUNT(*) FROM runs").fetchone()[0] == 0, "Benchmark DB already has runs"
    assert target.execute("SELECT COUNT(*) FROM eval_batches").fetchone()[0] == 0, "Benchmark DB already has batches"
    assert all(row[0] == "系统示例" for row in target.execute("SELECT created_by FROM tests")), "Non-demo inputs exist"
    backup = args.database.with_name("ui-eval-before-fresh-import.sqlite3")
    if not backup.exists():
        with sqlite3.connect(backup) as destination:
            target.backup(destination)
        backup.chmod(0o600)
    timestamp = datetime.now(timezone.utc).isoformat()

    def insert(table, record):
        columns = list(record)
        target.execute(f"INSERT INTO {table} ({','.join(columns)}) VALUES ({','.join('?' for _ in columns)})",
                       [record[key] for key in columns])

    with target:
        target.execute("DELETE FROM criteria")
        target.execute("DELETE FROM tests")
        target.execute("DELETE FROM models")
        for group in manifest["groups"]:
            model = dict(source.execute("SELECT * FROM models WHERE id=?", (group["model_id"],)).fetchone())
            model["api_key_env"] = "ANTHROPIC_AUTH_TOKEN"
            model["is_default"] = int(group["task"] == "task2")
            if group["task"] == "task7":
                model.update(base_url="http://127.0.0.1:18185", host="127.0.0.1", port=18185)
            insert("models", model)
            for item in group["tests"]:
                assert item["query"] == item["original_query"], "Query was rewritten"
                previous_title = f"standalone-original-20261025/{group['task']}/{item['question']}"
                previous = dict(source.execute("SELECT * FROM tests WHERE title=?", (previous_title,)).fetchone())
                test_id = f"test_bd_fresh_20261026_{group['task']}_{item['question']}"
                previous_id = previous["id"]
                previous.update(id=test_id, code=f"BD-{group['task']}-{item['question']}",
                    title=f"{TAG}/{group['task']}/{item['question']}", query=item["query"],
                    base_figma_url=item["figma_url"], model_id=group["model_id"], status="等待生成",
                    figma_url="", preview_files="[]", run_dir="", criteria_version=1, created_by="gyy",
                    created_at=timestamp, updated_at=timestamp, clarification_questions="[]", clarifications="[]",
                    annotation="", plan_options="[]", plan_selection="")
                insert("tests", previous)
                criteria = source.execute("SELECT * FROM criteria WHERE test_id=? ORDER BY position", (previous_id,)).fetchall()
                assert len(criteria) == 20, "Previous evaluation configuration changed"
                for index, row in enumerate(criteria):
                    criterion = dict(row)
                    criterion.update(id=f"criterion_{test_id}_{index}", test_id=test_id, created_at=timestamp)
                    insert("criteria", criterion)
    args.database.chmod(0o600)
    print(json.dumps({"tag": TAG, "models": 7, "tests": 21, "criteria_per_test": 20,
                      "query_modified": False, "runs_submitted": 0, "source_db_modified": False}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=ROOT / "storage/benchmark-design/inputs.json")
    parser.add_argument("--database", type=Path, default=ROOT / "storage/benchmark-design/ui-eval.sqlite3")
    parser.add_argument("--model-db", type=Path, default=PREVIOUS / "state/ui-eval.sqlite3")
    import_inputs(parser.parse_args())
