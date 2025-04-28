#!/bin/bash

# Create logs directory if it doesn't exist
mkdir -p logs

# Array to store PIDs
declare -a pids

# Function to cleanup processes
cleanup() {
    echo "Shutting down all services..."
    for pid in "${pids[@]}"; do
        if kill -0 "$pid" 2>/dev/null; then
            kill "$pid"
            wait "$pid" 2>/dev/null
        fi
    done
    exit 0
}

# Set up trap for cleanup on SIGINT (Ctrl+C)
trap cleanup SIGINT

# Start frontend
echo "Starting frontend..."
(cd frontend && BROWSER=none npm start) > logs/frontend.log 2>&1 &
pids+=($!)

# Start backend
echo "Starting backend..."
(cd backend && \
    export GOPROXY=https://goproxy.cn,direct && \
    go mod download && \
    go mod tidy && \
    go run .) > logs/backend.log 2>&1 &
pids+=($!)

# Start AI engine
echo "Starting AI engine..."
python3 run.py > logs/ai_engine.log 2>&1 &
pids+=($!)

# Start Caddy in foreground
echo "Starting Caddy..."
caddy start > logs/caddy.log 2>&1

# Wait for Caddy to exit (it will be in foreground)
wait

# Cleanup when Caddy exits
cleanup
