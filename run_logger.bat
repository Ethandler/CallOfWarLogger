@echo off
:: Check for admin privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running with administrator privileges...
) else (
    echo ==========================================
    echo Administrator privileges are required
    echo Please right-click this batch file and
    echo select "Run as administrator"
    echo ==========================================
    pause
    exit
)

:: Set up Python environment and run the logger
echo Starting Game Logger...
python game_logger.py
pause