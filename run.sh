#!/usr/bin/env bash

# Function to handle cleanup on exit
cleanup() {
    echo "Stopping backend and frontend..."
    kill $(jobs -p)
    exit
}

# Trap SIGINT and SIGTERM
trap cleanup SIGINT SIGTERM

echo "Starting Skill Gap Analyzer..."

# Check if venv exists and activate it if it does
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/Scripts/activate || source venv/bin/activate
fi

echo "Starting Backend (FastAPI)..."
python -m uvicorn app.main:app --reload &

echo "Waiting for backend to initialize..."
sleep 5

echo "Starting Frontend (React)..."
cd client && npm run dev &

# Wait for all background processes
wait
