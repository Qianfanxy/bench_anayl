#!/usr/bin/env bash
set -u

PROJECT="/mnt/afs/panzhengyuan/llm_training/project/rate_website_figma-sft-cc-tap"

while true; do
  "$PROJECT/scripts/ui-eval-watchdog.sh" || true
  sleep 7200
done
