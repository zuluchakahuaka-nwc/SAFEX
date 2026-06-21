# 🐳 Docker Scan: SAFEX + Тестовый сервер

## 📋 Обзор

Запускаем 2 контейнера:
1. **🔍 SAFEX** - Утилита для сканирования
2. **🎯 Тестовый сервер** - Приложение с 8 намеренными уязвимостями

---

## 🚀 Быстрый старт

### Linux/macOS

```bash
# Запустить контейнеры
./docker/scan.sh up

# Запустить сканирование
./docker/scan.sh scan

# Показать отчеты
./docker/scan.sh reports

# Показать логи
./docker/scan.sh logs

# Остановить
./docker/scan.sh stop

# Удалить всё
./docker/scan.sh clean
```

### Windows

```cmd
REM Запустить контейнеры
docker\scan.bat up

REM Запустить сканирование
docker\scan.bat scan

REM Показать отчеты
docker\scan.bat reports

REM Показать логи
docker\scan.bat logs

REM Остановить
docker\scan.bat stop

REM Удалить всё
docker\scan.bat clean
```

---

## 🌐 Доступные сервисы

| Сервис | URL | Описание |
|--------|-----|-----------|
| **Тестовая страница** | http://localhost:8081 | Страница с 8 уязвимостями |
| **SAFEX API** | http://localhost:8001 | API SAFEX |
| **SAFEX Docs** | http://localhost:8001/docs | API документация |
| **База данных** | localhost:5433 | PostgreSQL для тестов |
| **Redis** | localhost:6381 | Redis для тестов |

---

## 🎯 Тестовые уязвимости

Тестовый сервер содержит **8 намеренных уязвимостей**:

### 1. 🔴 Hardcoded Password (CRITICAL)
- **CWE:** CWE-798
- **Файл:** `test-targets/index.html`
- **Описание:** Пароль хранится в JavaScript коде
- **Демо:** Попробуй пароль `SuperSecretPassword123!`

### 2. 🔴 Exposed API Key (CRITICAL)
- **CWE:** CWE-798
- **Файл:** `test-targets/index.html`, `test-targets/vulnerable_app.py`
- **Описание:** API ключ OpenAI виден в коде
- **Демо:** Открой консоль браузера (F12)

### 3. 🟠 SQL Injection (HIGH)
- **CWE:** CWE-89
- **Файл:** `test-targets/index.html`, `test-targets/vulnerable_app.py`
- **Описание:** SQL запрос через конкатенацию строк
- **Демо:** Ввод: `1; DROP TABLE users;--`

### 4. 🟠 Cross-Site Scripting (XSS) (HIGH)
- **CWE:** CWE-79
- **Файл:** `test-targets/index.html`
- **Описание:** Вставка пользовательского ввода в DOM
- **Демо:** Нажми кнопку "Test XSS"

### 5. 🟠 Insecure Deserialization (HIGH)
- **CWE:** CWE-502
- **Файл:** `test-targets/index.html`, `test-targets/vulnerable_app.py`
- **Описание:** Небезопасная десериализация JSON

### 6. 🟡 Weak Cryptographic Algorithm (MEDIUM)
- **CWE:** CWE-327
- **Файл:** `test-targets/index.html`, `test-targets/vulnerable_app.py`
- **Описание:** MD5 хеширование (слабый алгоритм)

### 7. 🔴 Command Injection (CRITICAL)
- **CWE:** CWE-77
- **Файл:** `test-targets/index.html`, `test-targets/vulnerable_app.py`
- **Описание:** Выполнение команд через `eval()`

### 8. 🟡 Insecure File Permissions (MEDIUM)
- **CWE:** CWE-732
- **Файл:** `test-targets/index.html`, `test-targets/vulnerable_app.py`
- **Описание:** Файлы с правами 777 (world-writable)

---

## 📊 Ожидаемые результаты SAFEX

SAFEX должен обнаружить **все 8 уязвимостей**:

```
🎯 Общее количество найденных уязвимостей: 8+

Распределение по критичности:
🔴 CRITICAL: 3
   - Hardcoded password
   - Exposed API key
   - Command injection

🟠 HIGH: 3
   - SQL injection
   - XSS
   - Insecure deserialization

🟡 MEDIUM: 2
   - Weak cryptographic algorithm
   - Insecure file permissions
```

---

## 🔍 Процесс сканирования

```bash
# 1. Запустить контейнеры
./docker/scan.sh up

# 2. Дождаться запуска (~30-60 секунд)
./docker/scan.sh status

# 3. Открыть тестовую страницу в браузере
# http://localhost:8081

# 4. Запустить сканирование
./docker/scan.sh scan

# 5. Посмотреть отчеты
./docker/scan.sh reports
```

---

## 📝 Логи и отчеты

### Логи контейнеров:

```bash
# Все логи
docker-compose -f docker-compose.scan.yml logs

# Логи SAFEX
docker logs safex-scanner

# Логи тестового сервера
docker logs test-vulnerable-server
```

### Отчеты сканирования:

Отчеты сохраняются в `./test-reports/`

```
test-reports/
├── scan_vulnerable_app_20250217_123456.json
├── scan_index_20250217_123457.json
└── ...
```

---

## 🗑️ Очистка

### Остановить (сохранить данные):

```bash
# Linux/macOS
./docker/scan.sh stop

# Windows
docker\scan.bat stop
```

### Удалить всё (⚠️ без возврата):

```bash
# Linux/macOS
./docker/scan.sh clean

# Windows
docker\scan.bat clean
```

**Что удалится:**
- ❌ Все контейнеры
- ❌ Все volumes с данными
- ❌ Все отчеты сканирования
- ❌ Сеть test-network

---

## ✅ Проверка работоспособности

### 1. Проверить контейнеры:

```bash
docker-compose -f docker-compose.scan.yml ps
```

**Должно быть:**
```
NAME                     STATUS
safex-scanner          Up
test-vulnerable-server  Up
safex-test-db           Up (healthy)
safex-test-redis        Up (healthy)
```

### 2. Проверить доступность:

```bash
# Тестовая страница
curl http://localhost:8081

# SAFEX API
curl http://localhost:8001/health
```

### 3. Открыть в браузере:

```
🌐 http://localhost:8081
```

---

## 🔒 Безопасность

### ⚠️ Тестовые уязвимости:

**Эти уязвимости - ДЕМОНСТРАЦИОННЫЕ и НЕ используются в продакшене:**
- ❌ Hardcoded passwords (только тесты)
- ❌ Exposed API keys (тестовые ключи)
- ❌ SQL injection (только демонстрация)
- ❌ XSS (только демонстрация)

**Никогда не используйте эти файлы в реальном продакшене!**

---

## 🎯 Задачи тестового сканирования

1. ✅ Обнаружить все 8 уязвимостей
2. ✅ Определить критичность (CRITICAL/HIGH/MEDIUM/LOW)
3. ✅ Предоставить рекомендации по исправлению
4. ✅ Создать отчеты (JSON, HTML, Markdown)
5. ✅ Проверить работу всех сканнеров:
   - Config Scanner
   - Code Scanner
   - System Scanner
6. ✅ Проверить безопасность уровней:
   - Discovery mode (read-only)
   - Safe mode (non-destructive)
   - Moderate mode (с предупреждениями)
   - Aggressive mode (все изменения)

---

## 🆘 Решение проблем

### Контейнеры не запускаются:

```bash
# Проверить логи
docker-compose -f docker-compose.scan.yml logs

# Проверить статус
./docker/scan.sh status

# Пересоздать
./docker/scan.sh stop
./docker/scan.sh up
```

### SAFEX не видит уязвимости:

```bash
# Проверить логи SAFEX
./docker/scan.sh logs

# Проверить что файлы существуют
docker exec safex-scanner ls -la test-targets/

# Попробовать ручное сканирование
docker exec -it safex-scanner bash
python safex.py scan test-targets/vulnerable_app.py
```

---

## 📦 Структура контейнеров

```
┌─────────────────────────────────────────────────────┐
│              DOCKER ENGINE                         │
│                                                     │
│  ┌───────────────────────────────────────────┐    │
│  │  🔒 test-network                       │    │
│  │                                        │    │
│  │  ┌────────────┐                      │    │
│  │  │  🔍 SAFEX   │ safex-scanner    │    │
│  │  │             │ (порт 8001)     │    │
│  │  │  └────────────┘                      │    │
│  │                                        │    │
│  │  ┌────────────┐                      │    │
│  │  │  🎯 Test     │ test-vulnerable │    │
│  │  │  │            │ -server (8081) │    │
│  │  │  └────────────┘                      │    │
│  │                                        │    │
│  │  ┌────────────┐                      │    │
│  │  │  🐘 Postgres │ safex-test-db    │    │
│  │  │             │ (порт 5433)    │    │
│  │  │  └────────────┘                      │    │
│  │                                        │    │
│  │  ┌────────────┐                      │    │
│  │  │  🔴 Redis     │ safex-test-redis  │    │
│  │  │             │ (порт 6381)    │    │
│  │  │  └────────────┘                      │    │
│  │                                        │    │
│  │  └───────────────────────────────────┘    │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 🚀 Готово к тестированию!

```bash
# Запустить
docker\scan.bat up          # Windows
./docker/scan.sh up         # Linux/macOS

# Просмотреть уязвимости
# http://localhost:8081

# Запустить сканирование
docker\scan.bat scan        # Windows
./docker/scan.sh scan       # Linux/macOS

# Посмотреть результаты
docker\scan.bat reports    # Windows
./docker/scan.sh reports    # Linux/macOS

# Удалить всё
docker\scan.bat clean      # Windows
./docker/scan.sh clean       # Linux/macOS
```

---

**🎯 SAFEX найдет все 8 уязвимостей!** 🔍🔒
