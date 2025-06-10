#!/bin/bash

# FastAPI Server Startup Script
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "Virtual environment activated"
fi

# Start the server in background
echo "Starting FastAPI server..."
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > server.log 2>&1 &

# Get the process ID
SERVER_PID=$!
echo "Server started with PID: $SERVER_PID"
echo $SERVER_PID > server.pid

echo "Server is running in background"
echo "Logs: tail -f server.log"
echo "To stop: kill \$(cat server.pid) or ./stop_server.sh" 