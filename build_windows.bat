@echo off
set APP_NAME=HD_RAM_CPU_Alarm
set VERSION=1.1
echo ==================================================
echo %APP_NAME% v%VERSION% - Windows Build Tool
echo ==================================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not added to PATH!
    pause
    exit /b
)

echo [INFO] Updating dependencies...
pip install PyQt5 psutil pyinstaller --upgrade

echo [INFO] Building standalone executable...
pyinstaller --noconfirm --onefile --windowed --name "%APP_NAME%_v%VERSION%" --icon="NONE" main.py

echo [SUCCESS] Build finished! 
echo --------------------------------------------------
echo The executable is in the "dist" folder.
echo To create a professional installer (MSI/EXE), 
echo it is recommended to use "Inno Setup" or "NSIS" 
echo with the generated .exe file.
echo --------------------------------------------------
pause
