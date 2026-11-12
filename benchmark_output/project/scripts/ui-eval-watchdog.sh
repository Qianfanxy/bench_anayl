#!/usr/bin/env bash
set -u

PROJECT="/mnt/afs/panzhengyuan/llm_training/project/rate_website_figma-sft-cc-tap"
NODE_BIN="/root/.nvm/versions/node/v22.22.2/bin/node"
NODE_PATH="/root/.nvm/versions/node/v22.22.2/bin"
SESSION="ui_eval_platform"
HEALTH_URL="http://127.0.0.1:4173/api/health"
LOG="$PROJECT/storage/watchdog.log"

mkdir -p "$PROJECT/storage"

timestamp() {
  date "+%Y-%m-%d %H:%M:%S %z"
}

if curl --connect-timeout 3 --max-time 8 --fail --silent "$HEALTH_URL" >/dev/null; then
  printf "[%s] healthy\n" "$(timestamp)" >>"$LOG"
  exit 0
fi

# 服务收尾质检时事件循环会被同步的 python 审计卡住最长 120s，一次 8s 超时不能当死：再等 30s 复查一次
sleep 30
if curl --connect-timeout 3 --max-time 20 --fail --silent "$HEALTH_URL" >/dev/null; then
  printf "[%s] slow but healthy on recheck\n" "$(timestamp)" >>"$LOG"
  exit 0
fi

printf "[%s] unhealthy; restarting service\n" "$(timestamp)" >>"$LOG"
tmux kill-session -t "$SESSION" 2>/dev/null || true
# 端口没释放就起新实例会 EADDRINUSE 立即退出，会话跟着消失——2026-08-26 15:18 就是这样宕了 28 分钟
for _ in $(seq 1 30); do
  ss -ltn 2>/dev/null | grep -q ':4173 ' || break
  sleep 1
done
tmux new-session -d -s "$SESSION" \
  "cd '$PROJECT' && export PATH='$NODE_PATH':\"\$PATH\" && exec '$NODE_BIN' server/index.mjs >> storage/server.log 2>&1"

# 冷启动要回填历史数据，实测一分多钟才有 health；以前只等 60s，服务明明起来了却每次报 restart failed
for _ in $(seq 1 60); do
  sleep 2
  if curl --connect-timeout 3 --max-time 8 --fail --silent "$HEALTH_URL" >/dev/null; then
    printf "[%s] restart succeeded\n" "$(timestamp)" >>"$LOG"
    exit 0
  fi
done

printf "[%s] restart failed; retrying once\n" "$(timestamp)" >>"$LOG"
tmux kill-session -t "$SESSION" 2>/dev/null || true
sleep 5
tmux new-session -d -s "$SESSION" \
  "cd '$PROJECT' && export PATH='$NODE_PATH':\"\$PATH\" && exec '$NODE_BIN' server/index.mjs >> storage/server.log 2>&1"
for _ in $(seq 1 60); do
  sleep 2
  if curl --connect-timeout 3 --max-time 8 --fail --silent "$HEALTH_URL" >/dev/null; then
    printf "[%s] restart succeeded on retry\n" "$(timestamp)" >>"$LOG"
    exit 0
  fi
done
printf "[%s] restart failed twice; leaving it\n" "$(timestamp)" >>"$LOG"
exit 1
