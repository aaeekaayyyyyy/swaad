#!/bin/bash

# Kill any existing backend process
echo "Stopping existing backend..."
pkill -f "python.*main.py" || echo "No existing backend process found"

# Wait a moment
sleep 2

# Start the backend
echo "Starting backend server..."
cd "$(dirname "$0")"
source venv/bin/activate
python main.py

