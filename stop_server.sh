#!/bin/bash

# FastAPI Server Stop Script
cd "$(dirname "$0")"

if [ -f "server.pid" ]; then
    PID=$(cat server.pid)
    if kill -0 $PID > /dev/null 2>&1; then
        echo "Stopping FastAPI server (PID: $PID)..."
        kill $PID
        rm server.pid
        echo "Server stopped successfully"
    else
        echo "Server is not running"
        rm server.pid
    fi
else
    echo "No server.pid file found. Attempting to find and kill uvicorn processes..."
    pkill -f "uvicorn app.main:app"
    echo "Done"
fi 