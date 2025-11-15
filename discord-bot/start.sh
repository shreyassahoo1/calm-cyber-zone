#!/bin/bash

# SafeGuard Discord Bot - Startup Script

echo "========================================="
echo "SafeGuard Discord Bot - Starting..."
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

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo ""
    echo "WARNING: .env file not found!"
    echo "Please create .env file from env.example"
    echo ""
    exit 1
fi

# Start the bot
echo "Starting Discord bot..."
echo ""
python bot.py

