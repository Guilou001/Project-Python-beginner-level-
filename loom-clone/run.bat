@echo off
echo [*] Lancement de Loom Clone...
echo.

REM Vérifier si l'environnement virtuel existe
if not exist "venv\" (
    echo X Environnement virtuel non trouve!
    echo Veuillez d'abord executer: install.bat
    pause
    exit /b 1
)

REM Activer l'environnement virtuel
call venv\Scripts\activate.bat

REM Lancer l'application
echo [OK] Demarrage de l'application...
python loom_recorder.py

pause
