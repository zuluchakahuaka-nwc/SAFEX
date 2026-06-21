# 📋 SAFEX - Quick Start Manual

Быстрый запуск и использование SAFEX Security Framework

---

## 🚀 Быстрый запуск (Python)

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Запуск CLI

```bash
# Показать справку
python safex.py --help

# Валидация владения
python safex.py validate /path/to/target

# Сканирование с предупреждениями
python safex.py scan /path/to/target --safety-level safe

# С русской версией
python safex.py validate /path/to/target --language ru
```

### 3. Запуск TUI (интерактивный режим)

```bash
python src/tui/main.py
```

### 4. Запуск API (опционально)

```bash
python src/api/app.py
```

---

## 🌍 Выбор языка

```bash
python safex.py --help --language ru
python safex.py --help --language en
python safex.py --help --language es
```

---

## 🔧 Safety Levels

```bash
# Discovery mode (read-only)
python safex.py scan /path --safety-level discovery

# Safe mode (non-destructive)
python safex.py scan /path --safety-level safe

# Moderate mode (с предупреждениями)
python safex.py scan /path --safety-level moderate

# Aggressive mode (все изменения)
python safex.py scan /path --safety-level aggressive
```

---

## 📊 Генерация отчетов

```bash
# JSON формат
python safex.py report --format json --output report.json

# HTML формат
python safex.py report --format html --output report.html

# Markdown формат
python safex.py report --format markdown --output report.md

# CSV формат
python safex.py report --format csv --output report.csv
```

---

## 🌐 API Server

```bash
# Запуск на порту 8000
python src/api/app.py

# API документация
http://localhost:8000/docs
```

---

## 🔍 Команды CLI

### Основные:

```
validate    - Валидация владения
scan        - Сканирование
report      - Генерация отчетов
status      - Статус системы
list        - Список ресурсов
```

### Bot Security (безопасность ботов):

```
bot-scan    - Сканирование проекта бота на уязвимости
bot-audit   - Генерация чеклиста безопасности
bot-deploy  - Генерация Podman-шаблонов для деплоя
```

### Опции:

```
--language ru          - Русский интерфейс
--safety-level safe    - Безопасный режим
--help               - Справка
--verbose            - Подробные логи
```

---

## 🤖 Bot Security

### Сканирование проекта бота:

```bash
# Telegram бот
python safex.py bot-scan /path/to/bot --platform telegram

# Discord бот
python safex.py bot-scan /path/to/bot --platform discord

# Через универсальный scan
python safex.py scan /path/to/bot --scanner bot
```

### Аудит безопасности:

```bash
# Текстовый чеклист
python safex.py bot-audit --platform telegram --text

# JSON чеклист в файл
python safex.py bot-audit --platform telegram --output audit.json
```

### Генерация деплой-шаблонов (Podman):

```bash
# Генерация в папку
python safex.py bot-deploy --platform telegram --domain mybot.example.com --output-dir ./deploy

# Затем:
cd deploy
cp .env.example .env  # Заполнить реальные значения
# Добавить TLS сертификаты в nginx/certs/
podman-compose up -d
```

### Что проверяет bot-scan:
- Утечки токенов (Telegram, Discord, Slack, VK)
- eval() / exec() в коде
- Command injection (shell=True)
- Небезопасная десериализация (pickle, yaml.load)
- Захардкоженные секреты (пароли, ключи)
- Webhook без HTTPS
- Webhook без проверки секрета
- Отсутствие rate limiting
- Утечки в логах

---

## 🧪 Тестирование

```bash
# Запуск всех тестов
pytest tests/ -v

# С покрытием
pytest tests/ --cov=src --cov-report=html

# Конкретный модуль
pytest tests/test_basic.py -v
```

---

## 🗂️ Knowledge Base

```bash
# Проверить уязвимости
python src/knowledge_base/knowledge_base.py

# Поиск по CWE
python -c "from src.knowledge_base.knowledge_base import KnowledgeBase; kb = KnowledgeBase(); vuln = kb.get_vulnerability('VULN-001'); print(vuln)"
```

---

## 🛠️ Автофикс

```bash
python src/autofix/autofix_engine.py
```

---

## 🔒 Безопасность

```bash
# Создать бэкап
python src/safety/backup.py

# Мониторинг
python src/safety/monitor.py
```

---

## 📈 Режимы работы

### CLI режим
```bash
python safex.py
```

### TUI режим
```bash
python src/tui/main.py
```

### API режим
```bash
uvicorn src.api.app:app --host 0.0.0.0 --port 8000
```

---

## 🎯 Рекомендации

1. ⚠️ Сначала используйте `--safety-level safe`
2. 📝 Всегда проверяйте что вы владете файлами
3. 🔄 Обновляйтесь из GitHub:
   ```bash
   git pull origin main
   pip install -r requirements.txt --upgrade
   ```
4. 📊 Читайте логи в `logs/`
5. 🔒 Делайте бэкапы перед критическими операциями

---

## 🐛 Устрановка

```bash
# Удаление
pip uninstall safex

# Очистка кэша
pip cache purge
```

---

## 📚 Поддержка

```
📖 README.md          - Полная документация
📄 PROJECT_STRUCTURE.md - Структура проекта
📁 docs/*.md       - Дополнительные документы
```

---

## 🚀 Быстрый тест

```bash
# Проверка
python safex.py --help

# Валидация тестового файла
python safex.py validate test-targets/index.html

# Сканирование с отчетом
python safex.py scan test-targets/index.html --language ru --safety-level safe
python safex.py report --format json
```

---

**Готово к использованию!** 🚀
