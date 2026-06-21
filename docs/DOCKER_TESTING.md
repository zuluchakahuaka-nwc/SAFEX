# БЕЗОПАСНОЕ ТЕСТИРОВАНИЕ В DOCKER

## 🐋 Обзор

Полностью изолированная тестовая среда в Docker с возможностью быстрого удаления.

### 🎯 Преимущества:

- ✅ **Полная изоляция** - отдельные volumes, сети, порты
- ✅ **Быстрое удаление** - одна команда и все удалено
- ✅ **Бэкап данных** - можно сохранить тестовые данные
- ✅ **Мониторинг** - Prometheus + Grafana встроены
- ✅ **Отдельные порты** - не конфликтуют с продакшеном

---

## 📋 Порты для тестовой среды

| Сервис | Тестовый порт | Продакшен порт |
|--------|--------------|-----------------|
| API | 8001 | 8000 |
| База данных | 5433 | 5432 |
| Redis | 6380 | 6379 |
| Prometheus | 9091 | 9090 |
| Grafana | 3001 | 3000 |
| Nginx HTTP | 8081 | 8080 |
| Nginx HTTPS | 8443 | 8443 |

---

## 🚀 Быстрый старт

### Linux/macOS

```bash
# Запустить тестовую среду
./docker/manage_test.sh up

# Проверить статус
./docker/manage_test.sh status

# Посмотреть логи
./docker/manage_test.sh logs

# Остановить
./docker/manage_test.sh down

# ⚠️  Удалить ВСЕ!
./docker/manage_test.sh clean
```

### Windows

```cmd
REM Запустить тестовую среду
docker\manage_test.bat up

REM Проверить статус
docker\manage_test.bat status

REM Посмотреть логи
docker\manage_test.bat logs

REM Остановить
docker\manage_test.bat down

REM ⚠️  Удалить ВСЕ!
docker\manage_test.bat clean
```

---

## 🌐 Доступные сервисы

После запуска (`docker/manage_test.sh up`):

### API

- **URL:** http://localhost:8001
- **API Docs:** http://localhost:8001/docs
- **Health Check:** http://localhost:8001/health

### База данных

- **Host:** localhost
- **Port:** 5433
- **Database:** safex_test
- **User:** safex_test
- **Password:** test_password123

**Подключение:**
```bash
psql -h localhost -p 5433 -U safex_test -d safex_test
```

### Redis

- **Host:** localhost
- **Port:** 6380
- **Password:** test_redis_pass

**Подключение:**
```bash
redis-cli -h localhost -p 6380 -a test_redis_pass
```

### Grafana (Мониторинг)

- **URL:** http://localhost:3001
- **Login:** admin
- **Password:** admin_test123

---

## 📊 Мониторинг

### Prometheus

- **URL:** http://localhost:9091
- Данные метрик API, БД, Redis

### Grafana

- **URL:** http://localhost:3001
- Дашборды:
  - API Performance
  - Database Performance
  - Redis Performance
  - System Resources

---

## 💾 Бэкап и восстановление

### Создать бэкап

**Linux/macOS:**
```bash
./docker/manage_test.sh backup
```

**Windows:**
```cmd
docker\manage_test.bat backup
```

Бэкапи сохраняются в `docker/backups/test/`

### Восстановить бэкап

**Linux/macOS:**
```bash
./docker/manage_test.sh restore
```

**Windows:**
```cmd
docker\manage_test.bat restore
```

---

## 🗑️ Удаление

### Остановить (сохранить данные)

```bash
# Linux/macOS
./docker/manage_test.sh down

# Windows
docker\manage_test.bat down
```

### Удалить все (⚠️ БЕЗ ВОЗВРАТА!)

```bash
# Linux/macOS
./docker/manage_test.sh clean

# Windows
docker\manage_test.bat clean
```

**Что удалится:**
- ❌ Все контейнеры
- ❌ Все volumes (БД, Redis, данные)
- ❌ Все данные в тестовой среде
- ❌ Сеть test-network

**Что НЕ удалится:**
- ✅ Исходный код проекта
- ✅ Конфигурационные файлы
- ✅ Бэкапи (если созданы)

---

## 🔄 Полный сброс

Если что-то пошло не так - полный сброс:

```bash
# Linux/macOS
./docker/manage_test.sh reset

# Windows
docker\manage_test.bat reset
```

Это:
1. Удалит все контейнеры и данные
2. Подождет 2 секунды
3. Пересоздаст все заново

---

## 🔍 Отладка

### Проверить логи

**Все логи:**
```bash
# Linux/macOS
./docker/manage_test.sh logs

# Windows
docker\manage_test.bat logs
```

**Логи API:**
```bash
# Linux/macOS
./docker/manage_test.sh logs-api

# Windows
docker\manage_test.bat logs-api
```

**Логи базы данных:**
```bash
# Linux/macOS
./docker/manage_test.sh logs-db

# Windows
docker\manage_test.bat logs-db
```

### Проверить контейнеры

```bash
# Показать все контейнеры
docker ps -a | grep safex-test

# Показать volumes
docker volume ls | grep safex-test

# Показать сети
docker network ls | grep safex-test
```

### Войти в контейнер

```bash
# Войти в API контейнер
docker exec -it safex-test-api bash

# Войти в БД контейнер
docker exec -it safex-test-db psql -U safex_test -d safex_test

# Войти в Redis контейнер
docker exec -it safex-test-redis redis-cli -a test_redis_pass
```

---

## 📊 Изоляция

### Volumes (изолированные!)

```
safex-test-db-data         - Только тестовая БД
safex-test-redis-data      - Только тестовый Redis
safex-test-data            - Данные приложения (тест)
safex-test-reports          - Отчеты (тест)
safex-test-logs            - Логи (тест)
safex-test-nginx-logs      - Nginx логи (тест)
safex-test-prometheus-data  - Prometheus (тест)
safex-test-grafana-data     - Grafana (тест)
```

### Network (изолированная!)

```
safex-test-network - Тестовая сеть
```

### Порты (изолированные!)

```
API:         8001 (не 8000)
БД:          5433 (не 5432)
Redis:       6380 (не 6379)
Prometheus:  9091 (не 9090)
Grafana:     3001 (не 3000)
```

---

## 🧪 Тестирование

### Пример теста

```bash
# 1. Запустить тестовую среду
./docker/manage_test.sh up

# 2. Подождать пока контейнеры запустятся (30-60 сек)
./docker/manage_test.sh status

# 3. Проверить API
curl http://localhost:8001/health

# 4. Запустить тесты
pytest tests/ -v

# 5. Если все хорошо - остановить
./docker/manage_test.sh down

# 6. Если что-то пошло не так - сбросить
./docker/manage_test.sh reset
```

### Если что-то пошло не так:

```bash
# 1. Проверить логи
./docker/manage_test.sh logs

# 2. Проверить статус контейнеров
./docker/manage_test.sh status

# 3. Если ошибка - полный сброс
./docker/manage_test.sh reset

# 4. Если совсем все плохо - удалить все
./docker/manage_test.sh clean
```

---

## 🔒 Безопасность

### Тестовые данные (не используются в продакшене!)

```
База данных:
  - User: safex_test
  - Password: test_password123
  - Database: safex_test

Redis:
  - Password: test_redis_pass

Grafana:
  - User: admin
  - Password: admin_test123
```

**⚠️ ВАЖНО:**
- Никогда не используйте эти данные в продакшене!
- Это только для тестов!
- Никогда не открывайте порты тестовой среды в интернет!

---

## ✅ Проверка после запуска

```bash
# Проверить что все контейнеры запущены
docker-compose -f docker-compose.test.yml ps

# Должно быть:
# NAME                STATUS
# safex-test-api      Up
# safex-test-db       Up (healthy)
# safex-test-redis    Up (healthy)
# safex-test-nginx    Up
# safex-test-prometheus Up
# safex-test-grafana   Up
```

---

## 🆘 Решение проблем

### Контейнеры не запускаются

```bash
# Проверить логи
./docker/manage_test.sh logs

# Проверить статус
./docker/manage_test.sh status

# Сбросить
./docker/manage_test.sh reset
```

### Порты уже заняты

```bash
# Посмотреть что занимает порт
netstat -ano | findstr :8001

# Остановить тестовую среду
./docker/manage_test.sh down

# Использовать другие порты в docker-compose.test.yml
```

### Данные не удаляются

```bash
# Принудительное удаление
docker-compose -f docker-compose.test.yml down -v

# Удалить volumes вручную
docker volume rm safex-test-db-data
docker volume rm safex-test-redis-data
docker volume rm safex-test-data

# Удалить сеть
docker network rm safex-test-network
```

---

## 📦 Что создается

### Контейнеры (7 штук)

```
safex-test-api        - SAFEX API
safex-test-db         - PostgreSQL
safex-test-redis      - Redis
safex-test-nginx      - Nginx
safex-test-prometheus - Prometheus
safex-test-grafana    - Grafana
```

### Volumes (8 штук)

```
safex-test-db-data
safex-test-redis-data
safex-test-data
safex-test-reports
safex-test-logs
safex-test-nginx-logs
safex-test-prometheus-data
safex-test-grafana-data
```

### Network (1)

```
safex-test-network
```

---

## ✅ Удалить все (если что-то не так)

```bash
# ОДНА КОМАНДА!
./docker/manage_test.sh clean
```

Это удалит ВСЕ:
- ❌ Все контейнеры
- ❌ Все volumes
- ❌ Все данные
- ❌ Сеть

Без возврата! Будь осторожен!

---

**Готово к безопасному тестированию!** 🚀🔒
