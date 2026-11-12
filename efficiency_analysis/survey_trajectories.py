"""Exploratory survey of trajectory files: schema variants, metadata fields, tool names, error shapes.

Usage: python3 -I survey_trajectories.py <batch_dir>
"""
import collections
import glob
import json
import os
import sys

root = sys.argv[1]
top_keys = collections.Counter()
msg_keys = collections.Counter()
meta_keys = collections.Counter()
tool_names = collections.Counter()
status = collections.Counter()
lines_per_file = collections.Counter()
success_vals = collections.Counter()
reasoning = collections.Counter()
sources = collections.Counter()
err_prefix = collections.Counter()
attempt_files = collections.Counter()
usage_keys = collections.Counter()
examples = {}

for d in sorted(glob.glob(os.path.join(root, "*", "task-*"))):
    files = sorted(glob.glob(os.path.join(d, "trajectory*.jsonl")))
    attempt_files[len(files)] += 1
    for f in files:
        with open(f) as fh:
            lines = [l for l in fh if l.strip()]
        lines_per_file[len(lines)] += 1
        for l in lines:
            try:
                r = json.loads(l)
            except Exception as e:
                status["<json error>"] += 1
                continue
            top_keys[tuple(sorted(r.keys()))] += 1
            status[r.get("status")] += 1
            md = r.get("metadata") or {}
            meta_keys[tuple(sorted(md.keys()))] += 1
            sources[(md.get("source"), md.get("client"), md.get("generation_mode"))] += 1
            rc = md.get("reasoning_control") or {}
            reasoning[(md.get("model"), rc.get("requested_effort"), r.get("enable_thinking"))] += 1
            usage_keys[tuple(sorted((md.get("usage") or {}).keys()))] += 1
            for m in r.get("messages", []):
                msg_keys[(m.get("role"), tuple(sorted(m.keys())))] += 1
                if m.get("role") == "assistant":
                    for tc in m.get("tool_calls") or []:
                        tool_names[(tc.get("function") or {}).get("name")] += 1
                if m.get("role") == "tool":
                    success_vals[(m.get("name"), repr(m.get("success")))] += 1
                    c = m.get("content")
                    c = c if isinstance(c, str) else json.dumps(c, ensure_ascii=False)
                    if m.get("success") is False or c.lstrip().lower().startswith("error"):
                        key = (repr(m.get("success")), c.strip()[:60].replace("\n", " "))
                        err_prefix[key] += 1
                        examples.setdefault(key, f)

def show(title, counter, n=40):
    print(f"\n== {title} ==")
    for k, v in counter.most_common(n):
        print(v, k)

show("trajectory files per task dir", attempt_files)
show("lines per file", lines_per_file)
show("top-level keys", top_keys)
show("status", status)
show("metadata keys", meta_keys)
show("source/client/mode", sources)
show("model / requested_effort / enable_thinking", reasoning, 60)
show("usage keys", usage_keys)
show("message keys by role", msg_keys)
show("tool names", tool_names, 60)
show("tool success values", success_vals, 60)
show("error prefixes", err_prefix, 80)
