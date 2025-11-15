@echo off
REM SafeGuard ML Service - Startup Script (Windows)

echo =========================================
echo SafeGuard ML Service - Starting...
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

REM Start the service
echo Starting ML service...
echo Service will be available at http://localhost:8000
echo.
python main.py

