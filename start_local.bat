@echo off
echo Setting up AI Twin Local Development Environment...

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH!
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo Python found! Creating virtual environment...

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    python -m venv venv
    echo Virtual environment created.
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
    echo Creating .env file template...
    copy .env.example .env >nul 2>&1
    echo.
    echo IMPORTANT: Edit .env file and add your Google API key!
    echo You can get a key from: https://makersuite.google.com/app/apikey
    echo.
    pause
)

REM Start the application
echo.
echo Starting AI Twin application...
echo The app will be available at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.
python api/index.py

pause
