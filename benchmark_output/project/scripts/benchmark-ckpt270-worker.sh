#!/usr/bin/env bash
set -euo pipefail

PROJECT=/mnt/afs/gaoyongyong/code/rate_website_figma-sft-cc-tap-benchmark-design
GPU_STATE="$PROJECT/storage/benchmark-design/gpu"
PREVIOUS=/mnt/afs/gaoyongyong/code/rate_website_figma-sft-cc-tap/storage/standalone-original-20261025/gpu
CHECKPOINT=/mnt/afs/panzhengyuan/llm_training/project/rate_website_figma-sft-cc-tap/storage/local-runtime/model-local-a282d9c9a73446c8/ckpt-270-shadow

if [[ $(id -u) == 0 ]]; then
  if ! getent passwd 10704 >/dev/null; then
    useradd --uid 10704 --no-create-home --home-dir /mnt/afs/gaoyongyong gaoyongyong
  fi
  exec runuser -u "$(getent passwd 10704 | cut -d: -f1)" -- bash "$0"
fi

mkdir -p "$GPU_STATE"
exec >>"$GPU_STATE/worker.log" 2>&1
printf 'Starting fresh benchmark checkpoint worker at %s\n' "$(date -Is)"
nvidia-smi --query-gpu=name,memory.total --format=csv,noheader

# Reuse the pinned inference packages read-only. Install the CuDNN compatibility
# fix into this branch's overlay; never change the previous environment.
export PIP_CONFIG_FILE=/dev/null
export PIP_EXTRA_INDEX_URL=
if [[ ! -d "$GPU_STATE/overlay/nvidia_cudnn_cu12-9.16.0.29.dist-info" ]]; then
  "$PREVIOUS/venv/bin/python" -m pip install --index-url https://pypi.org/simple \
    --no-deps --target "$GPU_STATE/overlay" 'nvidia-cudnn-cu12==9.16.0.29'
fi
export PYTHONPATH="$GPU_STATE/overlay:$PREVIOUS/vendor${PYTHONPATH:+:$PYTHONPATH}"
export LD_LIBRARY_PATH="$GPU_STATE/overlay/nvidia/cudnn/lib${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
export CUDA_VISIBLE_DEVICES=0
"$PREVIOUS/venv/bin/python" - "$GPU_STATE" <<'PY'
import json,socket,sys
from pathlib import Path
from importlib.metadata import version
import torch
assert torch.cuda.is_available(), 'No CUDA device'
assert torch.backends.cudnn.version() >= 91500, 'CuDNN fix did not load'
info={'host':socket.gethostname(),'ip':socket.gethostbyname(socket.gethostname()),'port':18013,
      'cudnn_version':torch.backends.cudnn.version(),
      'versions':{k:version(k) for k in ('sglang','torch','sgl-kernel','flashinfer-python')}}
(Path(sys.argv[1])/'worker-info.json').write_text(json.dumps(info)+'\n')
PY

"$PREVIOUS/venv/bin/python" -m sglang.launch_server \
  --model-path "$CHECKPOINT" --host 0.0.0.0 --port 18013 --tp-size 1 \
  --max-running-requests 1 --tool-call-parser qwen3_coder --trust-remote-code \
  >>"$GPU_STATE/sglang.log" 2>&1 &
inference_pid=$!
cleanup() {
  kill -TERM "$inference_pid" 2>/dev/null || true
  wait "$inference_pid" 2>/dev/null || true
}
trap cleanup EXIT INT TERM
while kill -0 "$inference_pid" 2>/dev/null; do
  if [[ -f "$GPU_STATE/release.json" ]]; then
    printf 'Checkpoint tasks finished; releasing GPU at %s\n' "$(date -Is)"
    exit 0
  fi
  sleep 10
done
wait "$inference_pid"
