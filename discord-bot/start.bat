@echo off
REM SafeGuard Discord Bot - Startup Script (Windows)

echo =========================================
echo SafeGuard Discord Bot - Starting...
echo =========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

REM Check if .env file exists
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Please create .env file from env.example
    echo.
    pause
    exit
)

REM Start the bot
echo Starting Discord bot...
echo.
python bot.py

