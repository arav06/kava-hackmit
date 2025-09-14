#!/bin/sh

# Start EigenCloud TEE service in background
echo "Starting EigenCloud TEE service on port 9000..."
node dist/index.js &

# Start FastAPI backend in background
echo "Starting FastAPI backend on port 8000..."
cd backend && /app/venv/bin/python -m uvicorn main:app --host 0.0.0.0 --port 8000 &

# Start Next.js frontend
echo "Starting Next.js frontend on port 3000..."
cd frontend && npm start -- --port 3000 --hostname 0.0.0.0
