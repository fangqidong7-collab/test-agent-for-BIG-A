#!/bin/bash
set -Eeuo pipefail

PORT=5000
COZE_WORKSPACE_PATH="${COZE_WORKSPACE_PATH:-$(pwd)}"
DEPLOY_RUN_PORT=5000

cd "${COZE_WORKSPACE_PATH}"

kill_port_if_listening() {
    local pids
    pids=$(ss -H -lntp 2>/dev/null | awk -v port="${DEPLOY_RUN_PORT}" '$4 ~ ":"port"$"' | grep -o 'pid=[0-9]*' | cut -d= -f2 | paste -sd' ' - || true)
    if [[ -z "${pids}" ]]; then
      echo "Port ${DEPLOY_RUN_PORT} is free."
      return
    fi
    echo "Port ${DEPLOY_RUN_PORT} in use by PIDs: ${pids} (SIGKILL)"
    echo "${pids}" | xargs -I {} kill -9 {}
    sleep 1
}

kill_backend_port() {
    local pids
    pids=$(ss -H -lntp 2>/dev/null | awk '$4 ~ ":8000$"' | grep -o 'pid=[0-9]*' | cut -d= -f2 | paste -sd' ' - || true)
    if [[ -n "${pids}" ]]; then
      echo "Port 8000 in use by PIDs: ${pids} (SIGKILL)"
      echo "${pids}" | xargs -I {} kill -9 {}
      sleep 1
    fi
}

echo "Clearing ports before start."
kill_port_if_listening
kill_backend_port

# ====== 启动后端 ======
echo "Installing backend dependencies..."
cd "${COZE_WORKSPACE_PATH}/backend"
pip install -r requirements.txt -q 2>&1 | tail -5 || echo "Warning: some backend deps failed"

echo "Starting backend server on port 8000..."
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
echo "Backend starting (PID: $BACKEND_PID)..."

# 等待后端就绪
for i in $(seq 1 15); do
  if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "Backend is ready!"
    break
  fi
  if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "Warning: Backend process died. Check backend logs."
    break
  fi
  echo "Waiting for backend... ($i/15)"
  sleep 2
done

cd "${COZE_WORKSPACE_PATH}"

# ====== 启动前端 ======
echo "Starting frontend on port ${PORT}..."
PORT=$PORT pnpm tsx watch src/server.ts
