# 🐋 Проверка Docker и запуск тестов

## ❌ Проблема: Docker не найден!

```
'docker-compose' is not recognized as an internal or external command
```

Это означает, что **Docker не установлен** или не добавлен в PATH.

---

## 🔍 Проверка Docker Desktop

### 1. Открыть Docker Desktop:

```cmd
# Проверь если запущен
```
Открой Docker Desktop и посмотри статус:
- Если стоит статус "Docker Desktop is running" - ✅ Docker работает
- Если "Docker Desktop is stopped" - ❌ Docker не запущен

### 2. Проверить через командную строку:

**PowerShell (Admin):**
```powershell
docker info
```

**CMD:**
```cmd
docker info
```

**Результат:**
- Если показана версия Docker - ✅ Docker установлен
- Если ошибка "docker is not recognized" - ❌ Docker не установлен

---

## 📥 Установка Docker Desktop

### Способ 1: Через официальный сайт

1. Перейди: https://www.docker.com/products/docker-desktop/
2. Скачай Docker Desktop для Windows
3. Запусти установку
4. После установки перезагрузи компьютер
5. Открой Docker Desktop

### Способ 2: Через winget (если включен)

```cmd
winget install Docker.Desktop
```

### Способ 3: Через Chocolatey

```cmd
choco install docker-desktop
```

---

## 🚀 После установки Docker

### 1. Проверка работы:

```cmd
# Проверить версию
docker --version

# Проверить статус контейнеров
docker ps
```

### 2. Запуск тестового сервера:

```cmd
cd D:\Projects\SAFEXerver\docker
docker-compose -f docker-compose.test-only.yml up -d
```

### 3. Проверка доступа:

```
Открой браузер: http://localhost:8081
```

Должна быть страница с кнопками и уязвимостями!

---

## 🔍 Диагностика

### Проверка порта:

**PowerShell:**
```powershell
Test-NetConnection -LocalPort 8081 -InformationLevel Detailed
```

**CMD:**
```cmd
netstat -ano | findstr :8081
```

**Результат:**
- `LISTENING` - ✅ Порт открыт
- `TIME_WAIT` - ❌ Порт занят
- `EMPTY` - ❌ Порт свободен

---

## 📋 Проверка файлов проекта

### 1. Проверь структуру:

```cmd
cd D:\Projects\SAFEXerver
dir /B /S test-targets
```

**Должно быть:**
```
index.html              - Тестовая страница
vulnerable_app.py        - Python файл с уязвимостями
```

### 2. Проверь Docker файлы:

```cmd
cd D:\Projects\SAFEXerver\docker
dir /B *.yml
```

**Должно быть:**
```
docker-compose.yml         - Основной compose файл
docker-compose.test-only.yml  - Тестовый compose (только сервер)
```

---

## 🆘 Решение проблем

### Проблема: "docker not found"

**Причина:** Docker Desktop не установлен

**Решение:**
1. Установите Docker Desktop
2. Запустите Docker Desktop
3. Проверьте работу через командную строку

### Проблема: "localhost refused connection"

**Причина:** Контейнер не запущен или порт закрыт

**Решение:**
1. Проверьте статус: `docker ps`
2. Проверьте логи: `docker logs test-vulnerable-server`
3. Перезапустите: `docker-compose down` затем `docker-compose up -d`

### Проблема: "Map keys must be unique"

**Причина:** Дубликаты в docker-compose.yml

**Решение:**
1. Откройте docker-compose.yml в редакторе
2. Найдите дублирующиеся ключи
3. Удалите дубликаты

---

## 🎯 Простой тест (без Docker)

Если Docker не работает - можешь протестировать файлы напрямую:

### 1. Открыть HTML файл:

```
Дв браузере: file:///D:/Projects/SAFEXerver/test-targets/index.html
```

### 2. Запустить Python сервер:

```cmd
cd D:\Projects\SAFEXerver\test-targets
python vulnerable_app.py
```

### 3. Открыть в браузере:

```
http://localhost:8081
```

(тебе нужен простой HTTP сервер, например Python http.server)
```

**Простой HTTP сервер:**
```cmd
cd D:\Projects\SAFEXerver\test-targets
python -m http.server 8081
```

---

## 📋 Что должно работать

### После запуска контейнера:

```
🌐 http://localhost:8081

Страница с:
- 🔴 Hardcoded Password (CRITICAL)
- 🔴 SQL Injection (HIGH)
- 🟠 XSS (HIGH)
- 🟡 Weak Crypto (MEDIUM)
- 🔴 Insecure Deserialization (HIGH)
- 🔴 Exposed API Key (CRITICAL)
- 🔴 Command Injection (CRITICAL)
- 🟡 Insecure File Permissions (MEDIUM)
```

### SAFEX должен найти:

```
🔍 Всего уязвимостей: 8
🔴 КРИТИЧЕСКИЕ: 3
🟠 HIGH: 3
🟡 MEDIUM: 2
```

---

## 🔧 Восстановление

Если что-то не так:

### 1. Удалить контейнеры:

```cmd
docker-compose -f docker-compose.test-only.yml down -v
```

### 2. Удалить volumes:

```cmd
docker volume rm safex-test-db-data
docker volume rm safex-test-redis-data
docker network rm safex-test-network
```

### 3. Начать заново:

```cmd
docker-compose -f docker-compose.test-only.yml up -d
```

---

## 🆘 Если Docker не хотите устанавливать

### Вариант 1: Использовать Python HTTP сервер

```cmd
cd D:\Projects\SAFEXerver\test-targets
python -m http.server 8081
```

### Вариант 2: Использовать VS Code Live Server

1. Открой `test-targets/index.html` в VS Code
2. Нажми "Go Live" (кнопка справа внизу)
3. Страница откроется в браузере

### Вариант: IIS (Windows)

1. Открой IIS Manager
2. Добавь новый сайт
3. Укажи путь к `D:\Projects\SAFEXerver\test-targets`
4. Порт: 8081
5. Запустите сайт

---

## ✅ Проверка работоспособности

### Тест 1: Docker проверка

```cmd
docker info
docker ps
```

**Успех:** ✅ Docker работает

### Тест 2: Запуск контейнера

```cmd
docker-compose -f docker-compose.test-only.yml up -d
docker ps
```

**Успех:** Контейнер `test-vulnerable-server` должен быть Up

### Тест 3: Проверка доступа

```cmd
curl http://localhost:8081
```

**Успех:** Должен вернуться HTML

### Тест 4: Открыть в браузере

```
http://localhost:8081
```

**Успех:** Страница с кнопками и уязвимостями

---

## 🚀 Быстрый старт (после установки Docker)

```cmd
# 1. Запустить контейнер
docker-compose -f docker-compose.test-only.yml up -d

# 2. Открыть браузер
start http://localhost:8081

# 3. Проверить что работает
# Кликните на кнопки, посмотрите уязвимости
```

---

## 📊 Мониторинг

### Посмотреть логи:

```cmd
docker logs test-vulnerable-server
```

### Стоп контейнера:

```cmd
docker-compose -f docker-compose.test-only.yml down
```

---

## 🔒 Важное!

### ⚠️  НЕ используйте в продакшене:

- ❌ Hardcoded passwords
- ❌ SQL injection
- ❌ XSS vulnerabilities
- ❌ Weak cryptographic algorithms
- ❌ Insecure deserialization
- ❌ Exposed API keys
- ❌ Command injection
- ❌ Insecure file permissions

### ✅ Это ТОЛЬКО для тестов SAFEX!

---

## 📝 Следующие шаги

1. ✅ Установить Docker Desktop
2. ✅ Запустить контейнер: `docker-compose -f docker-compose.test-only.yml up -d`
3. ✅ Открыть http://localhost:8081
4. ✅ Проверить что страница работает
5. ✅ Сканировать через SAFEX
6. ✅ Посмотреть результаты

---

## 🆘 Если НЕ хотите использовать Docker

### Быстрый способ без Docker:

```cmd
cd D:\Projects\SAFEXerver\test-targets
python -m http.server 8081
```

Затем открой в браузере:
```
http://localhost:8081
```

**Это самый простой способ протестировать!** 🎯
