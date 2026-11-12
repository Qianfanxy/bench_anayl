#!/usr/bin/env python3
"""Launch the isolated benchmark services and supervisor in the background."""
import argparse
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
STORAGE = ROOT / "storage/benchmark-design"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime-config", required=True, type=Path)
    parser.add_argument("--services-only", action="store_true", help="Start dependencies without submitting tasks")
    parser.add_argument("--recovery", action="store_true", help="Resume only verified empty files; preserve prior attempts and designs")
    args = parser.parse_args()
    if (STORAGE / "complete.json").exists():
        raise SystemExit("This benchmark is complete; existing files will not be reused")
    if not os.environ.get("ANTHROPIC_AUTH_TOKEN"):
        raise SystemExit("Provide the existing model credential through ANTHROPIC_AUTH_TOKEN")
    services = [
        ("responses-adapter", ["node", "scripts/benchmark-responses-adapter.mjs"]),
        ("forward", ["node", "scripts/benchmark-model-forward.mjs"]),
        ("server", ["node", "scripts/start-benchmark-design.mjs", "--runtime-config", str(args.runtime_config.resolve())]),
        ("supervisor", ["node", "scripts/run-benchmark-design.mjs"]),
    ]
    if args.recovery:
        services[-1] = ("recovery", ["node", "scripts/recover-benchmark-design.mjs"])
    if args.services_only:
        services = services[:-1]
    for name, command in services:
        pid_file = STORAGE / f"{name}.pid"
        try:
            pid = int(pid_file.read_text())
            os.kill(pid, 0)
            cmdline = Path(f"/proc/{pid}/cmdline").read_bytes().decode().split("\0")
            if str(ROOT) not in Path(f"/proc/{pid}/cwd").resolve().as_posix() or command[1] not in cmdline:
                raise SystemExit(f"{name}: PID belongs to another process; inspect before resuming")
            print(f"{name}: already running ({pid})")
            continue
        except (OSError, ValueError):
            pass
        if name in ["supervisor", "recovery"]:
            # Wait for server readiness before putting any task into the queue.
            import time
            import urllib.request
            for attempt in range(30):
                try:
                    with urllib.request.urlopen("http://127.0.0.1:18174/api/health", timeout=2) as response:
                        if response.status == 200:
                            break
                except OSError:
                    time.sleep(1)
            else:
                raise SystemExit("Benchmark server did not become ready; supervisor not started")
        with (STORAGE / f"{name}.log").open("ab", buffering=0) as log:
            child = subprocess.Popen(command, cwd=ROOT, stdin=subprocess.DEVNULL,
                stdout=log, stderr=subprocess.STDOUT, start_new_session=True,
                env={**os.environ, **({"UI_EVAL_BENCHMARK_RECOVERY": "1"} if args.recovery else {})})
        pid_file.write_text(str(child.pid) + "\n")
        print(f"{name}: started ({child.pid})")
