@echo off
REM SafeGuard ML Service - Installation Script (Windows)

echo =========================================
echo SafeGuard ML Service - Installation
echo =========================================
echo.

REM Check Python version
echo Checking Python version...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.9 or higher from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo.
echo =========================================
echo Creating virtual environment...
echo =========================================
python -m venv venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo.
echo =========================================
echo Activating virtual environment...
echo =========================================
call venv\Scripts\activate.bat

echo.
echo =========================================
echo Upgrading pip...
echo =========================================
python -m pip install --upgrade pip

echo.
echo =========================================
echo Installing dependencies...
echo =========================================
echo This may take 10-15 minutes (downloading large packages)...
echo Please be patient, especially for PyTorch and Transformers
echo.
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo WARNING: Some packages may not have installed correctly
    echo Try installing manually: pip install -r requirements.txt
    pause
    exit /b 1
)

echo.
echo =========================================
echo Verifying installation...
echo =========================================
python verify_installation.py
if errorlevel 1 (
    echo.
    echo WARNING: Installation verification failed
    echo Please check the errors above
    pause
    exit /b 1
)

echo.
echo =========================================
echo Installation completed successfully!
echo =========================================
echo.
echo Next steps:
echo 1. Activate virtual environment:
echo    venv\Scripts\activate
echo.
echo 2. Run the ML service:
echo    python main.py
echo.
pause

