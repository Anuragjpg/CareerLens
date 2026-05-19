@echo off
cd /d "%~dp0"
echo ==========================================
echo  CareerLens - AI Resume Analyzer
echo ==========================================
echo.
echo Activating virtual environment...

if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
) else if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo [ERROR] No virtual environment found!
    echo Please create one: python -m venv .venv
    pause
    exit /b 1
)

echo Running app with Gemini AI support...
echo.
python app.py

echo.
pause
