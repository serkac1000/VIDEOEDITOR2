@echo off
echo Video Editor GUI - Windows Launcher
echo ===================================

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Run setup if needed
if not exist "setup_complete.flag" (
    echo Running first-time setup...
    python setup.py
    if errorlevel 1 (
        echo Setup failed
        pause
        exit /b 1
    )
    echo. > setup_complete.flag
)

REM Start the application
echo Starting Video Editor GUI...
python main.py

pause