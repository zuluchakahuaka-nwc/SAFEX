@echo off
chcp 65001 >nul
REM ═══════════════════════════════════════════════════════════
REM Запуск SAFEX + Тестовый сервер (Windows)
REM ═══════════════════════════════════════════════════════════

setlocal enabledelayedexpansion

REM Цвета
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "CYAN=[96m"
set "NC=[0m"

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║                                                          ║
echo ║ SAFEX + ТЕСТОВЫЙ СЕРВЕР ║
echo ║                                                          ║
echo ╚════════════════════════════════════════════════════════╝
echo.

if "%1"=="" goto help
if "%1"=="up" goto up
if "%1"=="scan" goto scan
if "%1"=="reports" goto reports
if "%1"=="logs" goto logs
if "%1"=="status" goto status
if "%1"=="stop" goto stop
if "%1"=="clean" goto clean
if "%1"=="help" goto help
goto unknown

:help
echo Использование: %0 [команда]
echo.
echo Команды:
echo   up        - Запустить контейнеры
echo   scan      - Запустить SAFEX и сканировать тестовый сервер
echo   reports   - Показать отчеты сканирования
echo   logs      - Показать логи SAFEX
echo   status    - Показать статус контейнеров
echo   stop      - Остановить контейнеры
echo clean - Удалить все контейнеры и данные
echo   help      - Показать эту справку
echo.
echo Примеры:
echo   %0 up              # Запустить контейнеры
echo   %0 scan            # Запустить сканирование
echo   %0 reports         # Показать отчеты
echo   %0 clean           # Удалить всё
echo.
goto end

:up
echo %BLUE% Запуск контейнеров...%NC%
echo.
docker-compose -f docker-compose.scan.yml up -d
if %ERRORLEVEL% EQU 0 (
    echo.
    echo %GREEN%[OK] Контейнеры запущены!%NC%
    echo.
    echo Контейнеры:
    echo [X] safex-scanner - SAFEX (порт 8001)
    echo test-vulnerable-server - Тестовый сервер (порт 8081)
    echo safex-test-db - PostgreSQL (порт 5433)
    echo [X] safex-test-redis - Redis (порт 6381)
    echo.
    echo Доступные URL:
    echo Тестовая страница: http://localhost:8081
    echo SAFEX API: http://localhost:8001
    echo Отчеты: .\test-reports\
    echo.
) else (
    echo %RED%[FAIL] Ошибка запуска контейнеров%NC%
    exit /b 1
)
goto end

:scan
echo %CYAN% Запуск сканирования...%NC%
echo.
echo %BLUE%1. Запуск контейнеров...%NC%
docker-compose -f docker-compose.scan.yml up -d
timeout /t 3 /nobreak >nul
echo.
echo %CYAN%2. Сканирование Python файла...%NC%
docker exec safex-scanner python safex.py scan test-targets/vulnerable_app.py --language ru
timeout /t 5 /nobreak >nul
echo.
echo %CYAN%3. Сканирование HTML файла...%NC%
docker exec safex-scanner python safex.py scan test-targets/index.html --language ru
timeout /t 5 /nobreak >nul
echo.
echo %GREEN%[OK] Сканирование завершено!%NC%
echo.
goto end

:reports
echo %CYAN% Отчеты сканирования:%NC%
echo.
echo Поиск отчетов в test-reports\...
dir /B test-reports\*.json 2>nul
if errorlevel 1 (
    echo Отчеты не найдены.
) else (
    echo Найдены отчеты:
    dir /B test-reports\*.json
)
echo.
goto end

:logs
echo %CYAN% Логи SAFEX:%NC%
echo.
docker logs safex-scanner
goto end

:status
echo %CYAN% Статус контейнеров:%NC%
echo.
docker-compose -f docker-compose.scan.yml ps
echo.
goto end

:stop
echo %YELLOW%⏹  Остановка контейнеров...%NC%
echo.
docker-compose -f docker-compose.scan.yml down
if %ERRORLEVEL% EQU 0 (
    echo %GREEN%[OK] Контейнеры остановлены%NC%
    echo.
) else (
    echo %RED%[FAIL] Ошибка остановки%NC%
    exit /b 1
)
goto end

:clean
echo.
echo %RED% ОЧИСТКА ВСЕХ КОНТЕЙНЕРОВ И ДАННЫХ!%NC%
echo.
set /p confirm="Вы уверены? (yes/no): "
if /i "%confirm%"=="yes" (
    echo %BLUE%ℹ Удаление контейнеров и данных...%NC%
    docker-compose -f docker-compose.scan.yml down -v
    
    REM Удалить отчеты
    if exist test-reports rmdir /s /q test-reports
    
    if %ERRORLEVEL% EQU 0 (
        echo %GREEN%[OK] Все удалено!%NC%
        echo.
    ) else (
        echo %RED%[FAIL] Ошибка удаления%NC%
        exit /b 1
    )
) else (
    echo %BLUE%ℹ Отменено%NC%
    echo.
)
goto end

:unknown
echo %RED%[FAIL] Неизвестная команда: %1%NC%
echo.
goto help

:end
endlocal
