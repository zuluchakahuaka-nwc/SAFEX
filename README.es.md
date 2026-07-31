# SAFEX

**Languages:** [English](README.md) | [Русский](README.ru.md) | [中文](README.zh-CN.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Português](README.pt-BR.md) | [العربية](README.ar.md) | [日本語](README.ja.md) | [हिन्दी](README.hi.md) | [한국어](README.ko.md)

**SAFEX (Security Audit Framework for Enhanced Protection) es un conjunto de herramientas de seguridad modular en Python que valida la propiedad de un objetivo y luego analiza configuraciones, código fuente, sistemas y bots de mensajería en busca de vulnerabilidades, generando informes orientados a la corrección.**

> Python 3.9+ · orientado a Linux/Ubuntu · herramienta de ciberseguridad. Usa SAFEX únicamente en sistemas, código e infraestructura que poseas o que estés autorizado explícitamente a probar.

## Características

- **Validación de propiedad** — una comprobación de autorización en dos fases se ejecuta antes de cualquier análisis, con varios métodos de validación.
- **Escáneres conectables** — `config`, `code`, `system`, `vulnerability`, `network`, `web`, `bot` y un escáner de servidores Linux, integrados mediante una arquitectura Factory/plugin.
- **Seguridad de bots** — detecta tokens filtrados de Telegram/Discord/Slack/VK, `eval`/`exec`, inyección de comandos, deserialización insegura, secretos codificados y webhooks inseguros; genera listas de auditoría y plantillas de despliegue Podman.
- **Niveles de seguridad** — `discovery` (solo lectura), `safe`, `moderate` y `aggressive` controlan cada operación.
- **Auto-fix** — aplica correcciones con copias de seguridad y reversión.
- **Informes** — JSON, text, HTML, Markdown y CSV.
- **i18n** — interfaz disponible en más de 10 idiomas.
- **Interfaces** — CLI, API de Python, API REST con FastAPI y TUI.
- **Contenedores** — soporte completo de Podman (rootless).

## Instalación (Ubuntu)

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

También se admite una imagen de contenedor Podman — consulta la guía de instalación a continuación.

## Inicio rápido

```bash
python safex.py --help
python safex.py validate /path/to/target
python safex.py scan /path/to/target --safety-level safe
python safex.py scan /path/to/target --scanner code
python safex.py report --format json --output report.json
python safex.py status
python safex.py list scanners
```

## Uso

```bash
# Seguridad de bots
python safex.py bot-scan /path/to/bot --platform telegram
python safex.py bot-audit --platform telegram --text

# Otras interfaces
python src/tui/main.py                  # TUI
uvicorn src.api.app:app --port 8000     # REST API
```

Opciones globales: `--language en|ru|es|fr|de|zh|ja|ar|pt|it`, `--safety-level discovery|safe|moderate|aggressive`, `--verbose`.

## Documentación

- [MANUAL.md](MANUAL.md) — manual de inicio rápido
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — arquitectura, flujo de datos, puntos de extensión
- [docs/AI_AGENT_GUIDE.md](docs/AI_AGENT_GUIDE.md) — referencia rápida para agentes de IA
- [docs/INSTALLATION_UBUNTU.md](docs/INSTALLATION_UBUNTU.md) — instalación detallada en Ubuntu
- [docs/UBUNTU_INSTALL.md](docs/UBUNTU_INSTALL.md) — instalación en Ubuntu con Podman
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) — estructura del proyecto
- [CHANGELOG.md](CHANGELOG.md) — historial de versiones

## Aviso legal / Uso responsable

SAFEX es una herramienta de pruebas de seguridad. Ejecútala únicamente contra sistemas, redes, aplicaciones y código fuente que poseas o para los que tengas autorización explícita por escrito. Escanear sistemas de terceros sin autorización puede ser ilegal. Los autores no se responsabilizan del uso indebido.

## Licencia

Licencia MIT — según lo indicado por el proyecto (consulta el repositorio para el archivo LICENSE).
