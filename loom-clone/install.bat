@echo off
echo ==========================================
echo   Installation de Loom Clone
echo ==========================================
echo.

REM Vérifier que Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python n'est pas installe!
    echo Veuillez installer Python 3.7 ou superieur.
    pause
    exit /b 1
)

echo [OK] Python trouve
python --version
echo.

REM Créer un environnement virtuel
echo [*] Creation de l'environnement virtuel...
python -m venv venv

if errorlevel 1 (
    echo X Erreur lors de la creation de l'environnement virtuel
    pause
    exit /b 1
)

echo [OK] Environnement virtuel cree
echo.

REM Activer l'environnement virtuel
echo [*] Activation de l'environnement virtuel...
call venv\Scripts\activate.bat

REM Mettre à jour pip
echo.
echo [*] Mise a jour de pip...
python -m pip install --upgrade pip

REM Installer les dépendances
echo.
echo [*] Installation des dependances...
pip install -r requirements.txt

if errorlevel 1 (
    echo X Erreur lors de l'installation des dependances
    pause
    exit /b 1
)

echo.
echo ==========================================
echo [OK] Installation terminee avec succes!
echo ==========================================
echo.
echo Pour demarrer l'application:
echo 1. Activez l'environnement virtuel: venv\Scripts\activate.bat
echo 2. Lancez l'application: python loom_recorder.py
echo.
pause
