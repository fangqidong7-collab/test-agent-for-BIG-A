#!/bin/bash
set -Eeuo pipefail

COZE_WORKSPACE_PATH="${COZE_WORKSPACE_PATH:-$(pwd)}"
PORT=5000
DEPLOY_RUN_PORT="${DEPLOY_RUN_PORT:-$PORT}"

cd "${COZE_WORKSPACE_PATH}"

# ====== 启动后端 ======
echo "Starting backend server on port 8000..."
cd "${COZE_WORKSPACE_PATH}/backend"
pip install -r requirements.txt -q 2>&1 | tail -3 || true
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

for i in $(seq 1 10); do
  if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "Backend ready (PID: $BACKEND_PID)"
    break
  fi
  sleep 2
done

# ====== 启动前端 ======
cd "${COZE_WORKSPACE_PATH}"
echo "Starting frontend on port ${DEPLOY_RUN_PORT}..."
PORT=${DEPLOY_RUN_PORT} node dist/server.js
