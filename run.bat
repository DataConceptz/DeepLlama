@echo off
REM Run script for DeepLlama (Windows)

echo Starting DeepLlama - AI Literature Review Tool
echo ==============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install/upgrade dependencies
echo Installing dependencies...
python -m pip install --upgrade pip --quiet
pip install -r requirements.txt --quiet

REM Check if Ollama is running
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo.
    echo Warning: Ollama does not appear to be running!
    echo    Please start Ollama before using AI features.
    echo    Visit https://ollama.ai for installation instructions.
    echo.
)

REM Run the application
echo.
echo Launching DeepLlama...
python main.py

pause
