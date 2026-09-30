@echo off
chcp 65001 >nul
REM Простая проверка Docker (Windows)

echo Проверка Docker...

REM Проверить запущен ли Docker
docker info >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [FAIL] Docker не запущен!
    echo Запустите Docker Desktop и попробуйте снова.
    exit /b 1
)

echo [OK] Docker запущен
echo.

echo Версия Docker:
docker --version
echo.

echo Статус контейнеров:
docker ps -a
echo.

echo Проверка порта 8081...
echo.

REM Проверка через PowerShell
powershell -Command "if (Get-NetTCPConnection -LocalPort 8081 -ErrorAction SilentlyContinue) { Write-Host '[OK] Порт 8081 открыт и слушается' } else { Write-Host '[FAIL] Порт 8081 не слушается' }"

echo.
echo Попробуйте открыть в браузере: http://localhost:8081
echo.
pause
