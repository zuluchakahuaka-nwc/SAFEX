@echo off
REM ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
setlocal enabledelayedexpansion

REM Цвета
set "RED=[91m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "BLUE=[94m"
set "CYAN=[96m"
set "NC=[0m"

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║                                                          ║
echo ║     🐳 SAFEX + ТЕСТОВЫЙ СЕРВЕР            ║
echo ║     SAFEX будет сканировать уязвимости ║
echo ║                                                          ║
echo ╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
echo ╚════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
echo.

if "%1"=="" goto help
if "%1"=="up" goto up
if "%1"=="down" goto down
if "%1"=="start" goto start
if "%1"=="scan" goto scan
if "%1"=="status" goto status
if "%1"=="logs" goto logs
if "%1"=="test-target" goto test_target
if "%1"=="safex" goto safex
if "%1"=="help" goto help
goto unknown

:help
echo.
echo ═════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
echo Команды:
echo   up          - Запустить оба контейнера
echo   down        - Остановить оба контейнера
echo   start       - Запустить контейнеры и открыть тестовую страницу
echo   scan        - Запустить SAFEX сканирование
echo   status      - Показать статус контейнеров
echo   logs        - Показать логи
echo   test-target - Открыть файл с уязвимостями
echo   safex       - Показать команды SAFEX
echo   help        - Показать эту справку
echo.

:up
echo.
echo ══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
echo ║                                                          ║
echo ║        🚀 Запуск контейнеров                       ║
echo ║                                                          ║
echo ╚═════════════════════════════════════════════════════════════════╝
echo.

echo %BLUE%🔴 Запуск тестового сервера...%NC%
docker run -d --name test-vulnerable-server ^
    -p 8081:80 ^
    -v D:\Projects\SAFEXerver\test-targets:/usr/share/nginx/html:ro ^
    nginx:alpine

if %ERRORLEVEL% NEQ 0 (
    echo %GREEN%✅ Тестовый сервер запущен!%NC%
    echo.
    echo %CYAN%🌐 Доступные URL:%NC%
    echo    🔴 Тестовая страница: http://localhost:8081/
    echo    🔍 SAFEX API: http://localhost:8001/
    echo.
    echo %YELLOW%📄 Уязвимости для теста:%NC%
    echo    1. Открой: http://localhost:8081/
    echo    2. Попробуй пароль: SuperSecretPassword123
    echo    3. Нажми "Test XSS" (XSS!)
    echo    4. Проверь консоль браузера (F12)
    echo.
    echo %BLUE%📋 Что SAFEX найдет:%NC%
    echo    1. 🔴 3 уязвимости CRITICAL (hardcoded password, exposed API key)
    echo    2. 🟠 3 уязвимости HIGH (SQL injection, XSS, weak crypto)
    echo    3. 🟡 2 уязвимости MEDIUM (insecure deserialization, file permissions)
) else (
    echo %RED%❌ Ошибка запуска тестового сервера!%NC%
    echo.
    echo Проверьте порт 8081:
    netstat -ano | findstr ":8081"
)
)

goto end

:down
echo.
echo ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
echo ║                                                          ║
echo ║        🏹 Остановка контейнеров                     ║
echo ║                                                          ║
echo ╚═════════════════════════════════════════════════════════════╝
echo.

echo %BLUE%🔴 Остановка тестового сервера...%NC%
docker stop test-vulnerable-server 2>nul

if %ERRORLEVEL% EQU 0 (
    echo %GREEN%✅ Тестовый сервер остановлен!%NC%
) else (
    echo %RED%❌ Ошибка остановки%NC%
)

goto end

:start
echo.
echo ══════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
echo ║                                                          ║
echo ║        🚀 Запуск и открытие теста               ║
echo ║                                                          ║
echo ╚═════════════════════════════════════════════════════════╝
echo.

echo %BLUE%1️⃣ Запуск контейнеров...%NC%
docker run -d --name test-vulnerable-server ^
    -p 8081:80 ^
    -v D:\Projects\SAFEXerver\test-targets:/usr/share/nginx/html:ro ^
    nginx:alpine

timeout /t 3 /nobreak >nul

if %ERRORLEVEL% EQU 0 (
    echo %GREEN%✅ Контейнеры запущены!%NC%
    echo.
    echo %CYAN%🌐 Доступные URL:%NC%
    echo.
    echo 🔴 Тестовая страница: http://localhost:8081/
    echo 🔍 SAFEX API: http://localhost:8001/
    echo.
    echo %YELLOW%📄 Открыть тестовую страницу?%NC%
    echo   - Да: Открой в браузере
    echo   - Нет: Нажми Enter
    echo.
    set /p "open_page="
    set /p "choice="
    set /p "open_choice="
    
    if /i "%open_page%"=="yes" (
        echo %BLUE%🌐 Открываю тестовую страницу...%NC%
        start "" http://localhost:8081/
    ) else (
        echo %YELLOW%📋 Пропускаю...%NC%
    )
    
    echo.
    echo %GREEN%✅ Тестовый сервер готов!%NC%
    echo.
    echo %CYAN%📊 SAFEX готов к сканированию!%NC%
    echo.
    echo %YELLOW%💡 Команда для сканирования:%NC%
    echo   .\start.bat scan
    echo.
    echo %CYAN%📊 Открыть SAFEX CLI:%NC%
    echo   .\start.bat safex
    echo.
    echo %CYAN%💡 Показать справку SAFEX:%NC%
    echo   .\start.bat safex help
    echo.
    echo %RED%⚠️  ВАЖНО: Не используйте тестовую среду в продакшене!%NC%
    echo.
    echo %YELLOW%💾 Установить пакеты Python:%NC%
    echo   pip install -r requirements.txt
) else (
    echo %RED%❌ Ошибка запуска контейнеров!%NC%
    echo.
    docker ps -a | findstr "test-vulnerable-server"
)

goto end

:scan
echo.
echo ══════════════════════════════════════════════════════════════════════════════════════╗
echo ║                                                          ║
echo ║        🔍 Сканирование тестового сервера SAFEX            ║
echo ║                                                          ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

echo %BLUE%🔴 Запуск SAFEX сканирования...%NC%
docker run -it --rm ^
    -v D:\Projects\SAFEXerver\test-targets:/app ^
    python safex.py scan test-targets/index.html ^
    --safety-level safe ^
    --language ru

echo.
echo %GREEN%✅ Сканирование завершено!%NC%
echo.
echo %CYAN%📊 Результаты сохранены в: D:\Projects\SAFEXerver\test-reports\%NC%

goto end

:status
echo.
echo ════════════════════════════════════════════════════════╗
echo ║                                                          ║
echo ║          📊 Статус контейнеров                      ║
echo ║                                                          ║
echo ╚═══════════════════════════════════════════════════════╝
echo.

echo %BLUE%🔴 Проверка контейнеров...%NC%
echo.
echo Контейнеры Docker:
docker ps -a | findstr "safex\|test-vulnerable"
echo.

echo.
echo %CYAN%📊 Статус портов:%NC%
echo.
echo Тестовый сервер (порт 8081):
netstat -ano | findstr ":8081"

echo.
echo SAFEX API (порт 8001):
netstat -ano | findstr ":8001"

goto end

:logs
echo.
echo ══════════════════════════════════════════════════════════════════════════════════════════════╗
echo ║                                                          ║
echo ║          📝 Логи контейнеров                           ║
echo ║                                                          ║
echo ╚═══════════════════════════════════════════════════════════════╝
echo.

echo %BLUE%📋 Логи тестового сервера:%NC%
docker logs test-vulnerable-server --tail 50
echo.
echo.
echo %CYAN%📋 Логи SAFEX:%NC%
docker logs test-safex-scanner --tail 50

goto end

:test_target
echo.
echo ══════════════════════════════════════════════════════╗
echo ║                                                          ║
echo ║          🎯 Открыть тестовый файл с уязвимостями      ║
echo ║                                                          ║
echo ╚═══════════════════════════════════════════════╝
echo.

echo %YELLOW%📂 Тестовый файл: D:\Projects\SAFEXerver\test-targets\index.html%NC%
echo.
echo %CYAN%🔴 Python файл: D:\Projects\SAFEXerver\test-targets\vulnerable_app.py%NC%
echo.
echo.
echo %BLUE%🚀 Запуск тестовой страницы...%NC%
start "" http://localhost:8081

echo.
echo %YELLOW%📝 Что проверить:%NC%
echo.
echo 🔴 Попробуй пароль: SuperSecretPassword123
echo 🟠 Нажми "Test XSS"
echo 🟠 Проверь консоль браузера (F12)
echo 🔴 Попробуй SQL Injection: 1; DROP TABLE users;--
echo 🟠 Проверь API key в консоли (F12)
echo.

echo.
echo %GREEN%✅ Тестовая страница открыта в браузере!%NC%
echo.

goto end

:safex
echo.
echo ══════════════════════════════════════════════════════════════════════╗
echo ║                                                          ║
echo ║          🔍 SAFEX команды                        ║
echo ║                                                          ║
echo ╚═══════════════════════════════════════════╝
echo.

echo %CYAN%📋 Доступные команды SAFEX:%NC%
echo.
echo ╔═══════════════════════════════════════════════════════════════════════╗
echo.
echo  📄 Команды валидации:
echo    python safex.py validate <path> [--method <method>] [--language <ru>]
echo.
echo.
echo 🔍 Команды сканирования:
echo    python safex.py scan <path> [--scanner <scanner>] [--safety-level <level>] [--language <ru>]
echo.
echo.
echo 📊 Команды отчетов:
echo    python safex.py report --format <json|html|markdown|csv> [--output <path>]
echo.
echo.
echo 📈 Команды статуса:
echo    python safex.py status
echo.
echo.
echo 📋 Команды списков:
echo    python safex.py list scanners
echo    python safex list tools
echo.
echo.
echo ══════════════════════════════════════════════════════════════════╝
echo.
echo 🔒 Safety Levels:
echo    🔍 discovery - Read-only (без изменений)
echo    🛡 safe - Безопасные изменения
echo    🟠 moderate - С предупреждениями
echo    🔴 aggressive - Все изменения
echo.
echo.
echo ════════════════════════════════════════════════════════════╝
echo.
echo 🌍 Поддерживаемые языки:
echo    🇬🇷 English, 🇪🇪, 🇫🇫, 🇩🇪, 🇨🇨🇦, 🇯🇵, 🇸🇸, 🇹🇹, 🇮🇮, 🇹🇰, 🇧🇷
echo.
echo.
echo ╔═════════════════════════════════════════════════════════╝
echo.
echo 💡 Быстрый старт:
echo    python safex.py --help
echo.

echo.
goto end

:unknown
echo %RED%❌ Неизвестная команда: %1%NC%
echo.
echo.
goto help

:end
echo.
echo ══════════════════════════════════════════════╗
echo ║                                                          ║
echo ║                                                          ║
echo ║                                                          ║
echo ╚═════════════════════════════════╝
echo.
endlocal
