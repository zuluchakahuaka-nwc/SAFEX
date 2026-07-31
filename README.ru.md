# SAFEX

**Languages:** [English](README.md) | [Русский](README.ru.md) | [中文](README.zh-CN.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Português](README.pt-BR.md) | [العربية](README.ar.md) | [日本語](README.ja.md) | [हिन्दी](README.hi.md) | [한국어](README.ko.md)

**SAFEX (Security Audit Framework for Enhanced Protection) — модульный Python-инструмент безопасности, который проверяет владение целью, а затем сканирует конфигурации, исходный код, системы и чат-ботов на уязвимости и формирует отчёты с рекомендациями по исправлению.**

> Python 3.9+ · ориентирован на Linux/Ubuntu · инструмент кибербезопасности. Используйте SAFEX только для систем, кода и инфраструктуры, которыми вы владеете или на тестирование которых у вас есть явное разрешение.

## Возможности

- **Проверка владения** — двухфазная проверка авторизации перед любым сканированием с несколькими методами валидации.
- **Сканеры через плагины** — `config`, `code`, `system`, `vulnerability`, `network`, `web`, `bot` и сканер Linux-сервера, подключаемые через Factory/плагинную архитектуру.
- **Безопасность ботов** — обнаружение утечек токенов Telegram/Discord/Slack/VK, `eval`/`exec`, внедрения команд, небезопасной десериализации, захардкоженных секретов и небезопасных вебхуков; формирует чек-листы аудита и шаблоны развёртывания Podman.
- **Уровни безопасности** — `discovery` (только чтение), `safe`, `moderate` и `aggressive` контролируют каждую операцию.
- **Авто-исправление** — применяет исправления с резервным копированием и откатом.
- **Отчёты** — JSON, text, HTML, Markdown и CSV.
- **i18n** — интерфейс доступен на 10+ языках.
- **Интерфейсы** — CLI, Python API, REST API на FastAPI и TUI.
- **Контейнеры** — полная поддержка Podman (rootless).

## Установка (Ubuntu)

```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv python3-dev \
  build-essential libssl-dev libffi-dev nmap nikto sqlmap
git clone https://github.com/zuluchakahuaka-nwc/safex.git
cd safex
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
python safex.py --help
```

Также поддерживается образ контейнера Podman — см. руководство по установке ниже.

## Быстрый старт

```bash
python safex.py --help
python safex.py validate /path/to/target
python safex.py scan /path/to/target --safety-level safe
python safex.py scan /path/to/target --scanner code
python safex.py report --format json --output report.json
python safex.py status
python safex.py list scanners
```

## Использование

```bash
# Безопасность ботов
python safex.py bot-scan /path/to/bot --platform telegram
python safex.py bot-audit --platform telegram --text

# Другие интерфейсы
python src/tui/main.py                  # TUI
uvicorn src.api.app:app --port 8000     # REST API
```

Глобальные опции: `--language en|ru|es|fr|de|zh|ja|ar|pt|it`, `--safety-level discovery|safe|moderate|aggressive`, `--verbose`.

## Документация

- [MANUAL.md](MANUAL.md) — краткое руководство
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — архитектура, поток данных, точки расширения
- [docs/AI_AGENT_GUIDE.md](docs/AI_AGENT_GUIDE.md) — краткая справка для AI-агентов
- [docs/INSTALLATION_UBUNTU.md](docs/INSTALLATION_UBUNTU.md) — подробная установка на Ubuntu
- [docs/UBUNTU_INSTALL.md](docs/UBUNTU_INSTALL.md) — установка на Ubuntu с Podman
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) — структура проекта
- [CHANGELOG.md](CHANGELOG.md) — история версий

## Правовое / Ответственное использование

SAFEX — это инструмент тестирования безопасности. Запускайте его только против систем, сетей, приложений и исходного кода, которыми вы владеете или на тестирование которых у вас есть явное письменное разрешение. Несанкционированное сканирование сторонних систем может быть незаконным. Авторы не несут ответственности за неправомерное использование.

## Лицензия

Лицензия MIT — согласно проекту (см. LICENSE в репозитории).
