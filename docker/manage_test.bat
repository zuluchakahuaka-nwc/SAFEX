@echo off
REM ═════════════════════════════════════════════════════════════
REM 🐳 УПРАВЛЕНИЕ ТЕСТОВОЙ СРЕДОЙ DOCKER (Windows)
REM ═════════════════════════════════════════════════════════════

setlocal enabledelayedexpansion

REM Цвета
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "NC=[0m"

echo.
echo ╔══════════════════════════════════════════════════════════╗
echo ║                                                          ║
echo ║           🐳 SAFEX TEST DOCKER MANAGER                  ║
echo ║                                                          ║
echo ╚══════════════════════════════════════════════════════════╝
echo.

if "%1"=="" goto help
if "%1"=="up" goto up
if "%1"=="down" goto down
if "%1"=="restart" goto restart
if "%1"=="status" goto status
if "%1"=="logs" goto logs
if "%1"=="logs-api" goto logs_api
if "%1"=="logs-db" goto logs_db
if "%1"=="clean" goto clean
if "%1"=="reset" goto reset
if "%1"=="backup" goto backup
if "%1"=="restore" goto restore
if "%1"=="help" goto help
goto unknown

:help
echo Использование: %0 [команда]
echo.
echo Команды:
echo   up          - Запустить тестовую среду
echo   down        - Остановить тестовую среду
echo   restart     - Перезапустить тестовую среду
echo   status      - Показать статус контейнеров
echo   logs        - Показать логи всех контейнеров
echo   logs-api    - Показать логи API
echo   logs-db     - Показать логи базы данных
echo   clean       - ⚠️  УДАЛИТЬ ВСЕ контейнеры и данные!
echo   reset       - ⚠️  ОСТОРОЖНО: Полный сброс (удаление + пересоздание)
echo   backup      - Создать бэкап тестовых данных
echo   restore     - Восстановить бэкап
echo   help        - Показать эту справку
echo.
echo Примеры:
echo   %0 up              # Запустить тестовую среду
echo   %0 logs            # Просмотреть логи
echo   %0 clean           # Удалить все контейнеры и данные
echo.
goto end

:up
echo %BLUE%ℹ️  Запуск тестовой среды...%NC%
docker-compose -f docker-compose.test.yml up -d
if %ERRORLEVEL% EQU 0 (
    echo %GREEN%✅ Тестовая среда запущена!%NC%
    echo.
    echo 🌐 Доступные сервисы:
    echo    - API: http://localhost:8001
    echo    - API Docs: http://localhost:8001/docs
    echo    - База данных: localhost:5433
    echo    - Redis: localhost:6380
    echo    - Prometheus: http://localhost:9091
    echo    - Grafana: http://localhost:3001 (admin/admin_test123)
    echo.
    echo 📝 Логи:
    echo    %0 logs         # Все логи
    echo    %0 logs-api     # Логи API
    echo    %0 logs-db      # Логи БД
    echo.
) else (
    echo %RED%❌ Ошибка запуска тестовой среды%NC%
    exit /b 1
)
goto end

:down
echo %BLUE%ℹ️  Остановка тестовой среды...%NC%
docker-compose -f docker-compose.test.yml down
if %ERRORLEVEL% EQU 0 (
    echo %GREEN%✅ Тестовая среда остановлена%NC%
    echo.
) else (
    echo %RED%❌ Ошибка остановки тестовой среды%NC%
    exit /b 1
)
goto end

:restart
echo %BLUE%ℹ️  Перезапуск тестовой среды...%NC%
docker-compose -f docker-compose.test.yml restart
if %ERRORLEVEL% EQU 0 (
    echo %GREEN%✅ Тестовая среда перезапущена%NC%
    echo.
) else (
    echo %RED%❌ Ошибка перезапуска тестовой среды%NC%
    exit /b 1
)
goto end

:status
echo %BLUE%ℹ️  Статус контейнеров:%NC%
echo.
docker-compose -f docker-compose.test.yml ps
echo.
echo %BLUE%ℹ️  Использование ресурсов:%NC%
echo.
docker stats --no-stream
goto end

:logs
echo %BLUE%ℹ️  Логи всех контейнеров:%NC%
echo.
docker-compose -f docker-compose.test.yml logs -f
goto end

:logs_api
echo %BLUE%ℹ️  Логи API контейнера:%NC%
echo.
docker-compose -f docker-compose.test.yml logs -f safex-api
goto end

:logs_db
echo %BLUE%ℹ️  Логи базы данных:%NC%
echo.
docker-compose -f docker-compose.test.yml logs -f test-db
goto end

:clean
echo %YELLOW%⚠️  ВНИМАНИЕ! Это удалит ВСЕ тестовые контейнеры и данные!%NC%
echo.
set /p confirm="Вы уверены? (yes/no): "
if /i "%confirm%"=="yes" (
    echo %BLUE%ℹ️  Удаление контейнеров и данных...%NC%
    docker-compose -f docker-compose.test.yml down -v

    REM Удалить volumes
    docker volume rm safex-test-db-data 2>nul
    docker volume rm safex-test-redis-data 2>nul
    docker volume rm safex-test-data 2>nul
    docker volume rm safex-test-reports 2>nul
    docker volume rm safex-test-logs 2>nul
    docker volume rm safex-test-nginx-logs 2>nul
    docker volume rm safex-test-prometheus-data 2>nul
    docker volume rm safex-test-grafana-data 2>nul

    REM Удалить сеть
    docker network rm safex-test-network 2>nul

    echo %GREEN%✅ Все контейнеры и данные удалены!%NC%
    echo.
) else (
    echo %BLUE%ℹ️  Отменено%NC%
    echo.
)
goto end

:reset
echo %YELLOW%⚠️  ОСТОРОЖНО! Полный сброс тестовой среды!%NC%
echo %YELLOW%⚠️  Это УДАЛИТ все контейнеры, данные и пересоздаст заново!%NC%
echo.
set /p confirm="Вы уверены? (yes/no): "
if /i "%confirm%"=="yes" (
    REM Сначала очистить
    call :clean

    REM Подождать
    timeout /t 2 /nobreak >nul

    REM Пересоздать
    echo %BLUE%ℹ️  Пересоздание тестовой среды...%NC%
    docker-compose -f docker-compose.test.yml up -d --force-recreate
    if %ERRORLEVEL% EQU 0 (
        echo %GREEN%✅ Тестовая среда сброшена и пересоздана!%NC%
        echo.
    ) else (
        echo %RED%❌ Ошибка сброса тестовой среды%NC%
        exit /b 1
    )
) else (
    echo %BLUE%ℹ️  Отменено%NC%
    echo.
)
goto end

:backup
echo %BLUE%ℹ️  Создание бэкапа тестовых данных...%NC%
echo.

set BACKUP_DIR=docker\backups\test
set BACKUP_NAME=test_backup_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%%time:~6,2%
set BACKUP_NAME=%BACKUP_NAME: =0%

if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

REM Бэкап volumes
echo %BLUE%ℹ️  Бэкап volumes...%NC%
docker run --rm -v safex-test-db-data:/db-data -v "%BACKUP_DIR%":/backup alpine tar czf "/backup/%BACKUP_NAME%_db.tar.gz" -C /db-data .
docker run --rm -v safex-test-redis-data:/redis-data -v "%BACKUP_DIR%":/backup alpine tar czf "/backup/%BACKUP_NAME%_redis.tar.gz" -C /redis-data .

echo %GREEN%✅ Бэкап создан: %BACKUP_DIR%\%BACKUP_NAME%%NC%
echo.
goto end

:restore
echo %BLUE%ℹ️  Восстановление бэкапа...%NC%
echo.

set BACKUP_DIR=docker\backups\test

if not exist "%BACKUP_DIR%" (
    echo %RED%❌ Директория бэкапов не найдена: %BACKUP_DIR%%NC%
    exit /b 1
)

echo Доступные бэкапы:
dir /B "%BACKUP_DIR%\*.tar.gz"

set /p backup_name="Введите имя бэкапа для восстановления: "

if exist "%BACKUP_DIR%\%backup_name%" (
    echo %BLUE%ℹ️  Восстановление из: %backup_name%%NC%

    REM Остановить контейнеры
    docker-compose -f docker-compose.test.yml down

    REM Восстановить volumes
    echo %backup_name% | findstr /C:"_db.tar.gz" >nul
    if !ERRORLEVEL! EQU 0 (
        docker run --rm -v safex-test-db-data:/db-data -v "%BACKUP_DIR%":/backup alpine tar xzf "/backup/%backup_name%" -C /db-data
    )

    echo %backup_name% | findstr /C:"_redis.tar.gz" >nul
    if !ERRORLEVEL! EQU 0 (
        docker run --rm -v safex-test-redis-data:/redis-data -v "%BACKUP_DIR%":/backup alpine tar xzf "/backup/%backup_name%" -C /redis-data
    )

    REM Запустить контейнеры
    docker-compose -f docker-compose.test.yml up -d

    echo %GREEN%✅ Бэкап восстановлен!%NC%
    echo.
) else (
    echo %RED%❌ Бэкап не найден: %backup_name%%NC%
    exit /b 1
)
goto end

:unknown
echo %RED%❌ Неизвестная команда: %1%NC%
echo.
goto help

:end
endlocal
