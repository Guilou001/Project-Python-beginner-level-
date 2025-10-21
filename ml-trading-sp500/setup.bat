@echo off
REM ML Trading Strategy - Setup Script for Windows

echo ========================================
echo ML Trading Strategy - Setup Script
echo ========================================
echo.

REM Check Python version
echo Checking Python version...
python --version
if errorlevel 1 (
    echo Error: Python not found
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)
echo.

REM Create virtual environment
echo Creating virtual environment...
if exist venv (
    echo Virtual environment already exists
    set /p REPLY="Do you want to recreate it? (y/n) "
    if /i "%REPLY%"=="y" (
        rmdir /s /q venv
        python -m venv venv
        echo Virtual environment recreated
    )
) else (
    python -m venv venv
    echo Virtual environment created
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet
echo pip upgraded
echo.

REM Install dependencies
echo Installing dependencies...
echo This may take a few minutes...
pip install -r requirements.txt --quiet
echo Dependencies installed
echo.

REM Create necessary directories
echo Creating project directories...
if not exist data mkdir data
if not exist models mkdir models
if not exist results mkdir results
echo Directories created
echo.

REM Test imports
echo Testing imports...
python test_imports.py
if errorlevel 1 (
    echo Import test failed
    echo Please check error messages above
    pause
    exit /b 1
)
echo All imports successful
echo.

echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo Next steps:
echo 1. Activate virtual environment:
echo    venv\Scripts\activate
echo.
echo 2. Run the pipeline:
echo    python main.py
echo.
echo 3. Or explore interactively:
echo    jupyter notebook notebooks\01_data_exploration.ipynb
echo.
echo For more information, see QUICKSTART.md
echo.
pause
