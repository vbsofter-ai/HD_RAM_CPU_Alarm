@echo off
echo ==========================================
echo System Resource Alarm - Windows Build Tool
echo ==========================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not added to PATH!
    echo Please install Python 3 from python.org and check "Add Python to PATH".
    pause
    exit /b
)

echo [INFO] Installing required libraries...
pip install PyQt5 psutil pyinstaller

echo [INFO] Building the executable...
pyinstaller --noconfirm --onefile --windowed --name "HD_RAM_CPU_Alarm_Win" main.py

echo [SUCCESS] Build finished! 
echo Check the "dist" folder for HD_RAM_CPU_Alarm_Win.exe.
pause
