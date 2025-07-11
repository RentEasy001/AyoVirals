#!/bin/bash

# AyoVirals - Start script for Replit deployment
# This script handles the complete startup process

echo "🔥 Starting AyoVirals on Replit..."

# Set environment variables
export PYTHONPATH="/app"
export NODE_ENV="production"
export PORT="3000"
export BACKEND_PORT="8001"
export MONGO_URL="mongodb://localhost:27017"
export DB_NAME="ayovirals_db"

# Get Replit environment variables
if [ -n "$REPL_SLUG" ] && [ -n "$REPL_OWNER" ]; then
    export REACT_APP_BACKEND_URL="https://$REPL_SLUG.$REPL_OWNER.repl.co"
else
    export REACT_APP_BACKEND_URL="http://localhost:8001"
fi

echo "Environment variables set:"
echo "  REACT_APP_BACKEND_URL: $REACT_APP_BACKEND_URL"
echo "  MONGO_URL: $MONGO_URL"

# Create necessary directories
mkdir -p /tmp/mongodb_data
mkdir -p /tmp/logs

# Function to cleanup processes
cleanup() {
    echo "🛑 Stopping services..."
    kill $MONGODB_PID 2>/dev/null
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set trap for cleanup
trap cleanup SIGINT SIGTERM

# Start MongoDB
echo "📦 Starting MongoDB..."
mongod --dbpath /tmp/mongodb_data --port 27017 --bind_ip 127.0.0.1 --nojournal --noprealloc --smallfiles --quiet &
MONGODB_PID=$!
sleep 3

# Install Python dependencies
echo "📦 Installing Python dependencies..."
cd /app
python -m pip install -r backend/requirements.txt --quiet

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
cd /app/frontend
yarn install --silent

# Build frontend
echo "🔨 Building React frontend..."
yarn build

# Start backend
echo "🚀 Starting FastAPI backend..."
cd /app/backend
python -m uvicorn server:app --host 0.0.0.0 --port 8001 --reload > /tmp/logs/backend.log 2>&1 &
BACKEND_PID=$!
sleep 2

# Start frontend
echo "🚀 Starting React frontend..."
cd /app/frontend
PORT=3000 BROWSER=none yarn start > /tmp/logs/frontend.log 2>&1 &
FRONTEND_PID=$!

# Wait a bit for services to start
sleep 5

echo "✅ AyoVirals is running!"
echo "   Frontend: http://localhost:3000"
echo "   Backend: http://localhost:8001"
echo "   Press Ctrl+C to stop"

# Keep the script running
wait