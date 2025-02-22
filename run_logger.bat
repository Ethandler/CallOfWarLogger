@echo off
:: Check for admin privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running with administrator privileges...
) else (
    echo Please run this script as administrator
    echo Right-click the batch file and select "Run as administrator"
    pause
    exit
)

:: Run the Python script
python game_logger.py
pause
