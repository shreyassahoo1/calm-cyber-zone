#!/bin/bash

# SafeGuard ML Service - Startup Script

echo "========================================="
echo "SafeGuard ML Service - Starting..."
echo "========================================="
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Start the service
echo "Starting ML service..."
echo "Service will be available at http://localhost:8000"
echo ""
python main.py

