@echo off
REM SAFEX Setup Script for Windows
REM Copyright 2024 SAFEX Project

setlocal enabledelayedexpansion

echo ========================================
echo SAFEX Windows Setup Script
echo ========================================
echo.

set /p "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo WARNING: Python 3 is not installed or not in PATH
    echo.
    echo Please install Python 3.11+ from https://python.org/downloads/
    echo.
    pause
    goto :end
)

echo Python 3 is installed: %python_version%

REM Create virtual environment
echo.
echo Creating virtual environment...
if not exist "venv\" (
    python -m venv venv
    echo Virtual environment created successfully
    echo.
) else (
    echo.
    echo Virtual environment already exists
    echo.
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing Python dependencies...
echo.
if exist "requirements.txt\" (
    python -m pip install --upgrade pip setuptools wheel pyinstaller
    python -m pip install -r requirements.txt
    echo Python dependencies installed successfully
    echo.
)

REM Create necessary directories
echo.
echo Creating directories...
if not exist "data\" mkdir data
if not exist "data\backups\" mkdir data\backups
if not exist "data\temp\" mkdir data\temp
if not exist "data\wordlists\" mkdir data\wordlists
if not exist "data\exploits\" mkdir data\exploits
if not exist "reports\" mkdir reports
if not exist "logs\" mkdir logs
echo Directories created successfully
echo.

REM Setup environment
echo.
echo Setting up environment...
if not exist ".env\" (
    if exist ".env.example\" (
        copy .env.example .env
        echo .env file created from .env.example
        echo.
        echo WARNING: Please edit .env file with your configuration
    goto :end
    ) else (
        echo.
        echo .env file already exists
        echo.
    )

REM Create empty placeholder data directories with .gitkeep
echo.
echo Creating placeholder files for data directories...
if not exist "data\backups\.gitkeep\" echo. >data\backups\.gitkeep
if not exist "data\temp\.gitkeep\" echo. >data\temp\.gitkeep
if not exist "data\wordlists\.gitkeep\" echo. >data\wordlists\.gitkeep
if not exist "data\exploits\.gitkeep\" echo. >data\exploits\.gitkeep"
if not exist "reports\.gitkeep\" echo >reports\.gitkeep
if not exist "logs\.gitkeep\" echo >logs\.gitkeep

REM Database setup
echo.
echo Database setup:
echo   1. Install PostgreSQL: https://www.postgresql.org/download/windows
echo   2. Create database: createdb safex_db
echo   3. Create user: create user safex with password safex_password
echo   4. Grant privileges: GRANT ALL PRIVILEGES ON DATABASE safex_db TO safex;
echo.
echo.
echo   5. Configure DATABASE_URL in .env file

REM Security tools setup
echo.
echo Security tools:
echo   1. Install Nmap: https://nmap.org/download
echo   2. Install Nikto: https://github.com/sullo/nikto
echo   3. Install OpenVAS: https://www.openvas.org
echo   4. Install OWASP ZAP: https://www.zaproxy.org/
echo.
echo.
echo Security tools setup skipped. Please install manually if needed.

:end
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo.
echo Next steps:
echo   1. Edit .env file with your configuration
echo.
echo   2. Activate environment: call venv\Scripts\activate.bat
echo   3. Run CLI: safex --help
echo.
echo   4. Validate domain: safex validate --domain example.com --target-email admin@example.com
echo   5. Start scan: safex scan --target 1.2.3.4 --token <token>
echo.
echo   6. Generate report: safex report --scan-id <uuid> --format json,html,pdf
echo.
echo.
echo.
echo For deployment:
echo   Local deployment: docker-compose up -d
echo   Cloud deployment: docker-compose -f docker-compose.yml up -d
echo.
echo.
echo Happy testing!

pause
