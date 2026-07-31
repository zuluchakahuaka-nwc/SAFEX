# SAFEX

**Languages:** [English](README.md) | [Русский](README.ru.md) | [中文](README.zh-CN.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Português](README.pt-BR.md) | [العربية](README.ar.md) | [日本語](README.ja.md) | [हिन्दी](README.hi.md) | [한국어](README.ko.md)

**SAFEX (Security Audit Framework for Enhanced Protection) ist ein modulares Python-Sicherheits-Toolkit, das die Eigentümerschaft eines Ziels validiert und dann Konfigurationen, Quellcode, Systeme und Messaging-Bots auf Schwachstellen prüft und behebungsorientierte Berichte erstellt.**

> Python 3.9+ · auf Linux/Ubuntu ausgerichtet · Cybersicherheitstool. Verwenden Sie SAFEX nur für Systeme, Code und Infrastruktur, die Sie besitzen oder deren Test ausdrücklich autorisiert ist.

## Funktionen

- **Eigentumsvalidierung** — vor jedem Scan läuft eine zweiphasige Autorisierungsprüfung mit mehreren Validierungsmethoden.
- **Steckbare Scanner** — `config`, `code`, `system`, `vulnerability`, `network`, `web`, `bot` und ein Linux-Server-Scanner, eingebunden über eine Factory-/Plugin-Architektur.
- **Bot-Sicherheit** — erkennt geleakte Telegram-/Discord-/Slack-/VK-Tokens, `eval`/`exec`, Command Injection, unsichere Deserialisierung, fest codierte Secrets und unsichere Webhooks; erstellt Audit-Checklisten und Podman-Deployment-Vorlagen.
- **Sicherheitsstufen** — `discovery` (nur Lesezugriff), `safe`, `moderate` und `aggressive` steuern jede Operation.
- **Auto-Fix** — wendet Fixes mit Backups und Rollback an.
- **Berichte** — JSON, text, HTML, Markdown und CSV.
- **i18n** — Oberfläche in über 10 Sprachen verfügbar.
- **Schnittstellen** — CLI, Python-API, FastAPI-REST-API und TUI.
- **Container** — volle Podman-Unterstützung (rootless).

## Installation (Ubuntu)

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

Außerdem wird ein Podman-Container-Image unterstützt — siehe die Installationsanleitung unten.

## Schnellstart

```bash
python safex.py --help
python safex.py validate /path/to/target
python safex.py scan /path/to/target --safety-level safe
python safex.py scan /path/to/target --scanner code
python safex.py report --format json --output report.json
python safex.py status
python safex.py list scanners
```

## Verwendung

```bash
# Bot-Sicherheit
python safex.py bot-scan /path/to/bot --platform telegram
python safex.py bot-audit --platform telegram --text

# Weitere Schnittstellen
python src/tui/main.py                  # TUI
uvicorn src.api.app:app --port 8000     # REST API
```

Globale Optionen: `--language en|ru|es|fr|de|zh|ja|ar|pt|it`, `--safety-level discovery|safe|moderate|aggressive`, `--verbose`.

## Dokumentation

- [MANUAL.md](MANUAL.md) — Schnellstart-Handbuch
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — Architektur, Datenfluss, Erweiterungspunkte
- [docs/AI_AGENT_GUIDE.md](docs/AI_AGENT_GUIDE.md) — Kurzreferenz für KI-Agenten
- [docs/INSTALLATION_UBUNTU.md](docs/INSTALLATION_UBUNTU.md) — detaillierte Ubuntu-Installation
- [docs/UBUNTU_INSTALL.md](docs/UBUNTU_INSTALL.md) — Ubuntu-Installation mit Podman
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) — Projektaufbau
- [CHANGELOG.md](CHANGELOG.md) — Versionsverlauf

## Rechtliches / Verantwortungsvolle Nutzung

SAFEX ist ein Sicherheits-Testwerkzeug. Setzen Sie es nur gegen Systeme, Netzwerke, Anwendungen und Quellcode ein, die Sie besitzen oder für die Sie eine ausdrückliche schriftliche Genehmigung haben. Das unbefugte Scannen von Drittsystemen kann illegal sein. Die Autoren übernehmen keine Haftung für missbräuchliche Verwendung.

## Lizenz

MIT-Lizenz — laut Projektangabe (siehe Repository für die LICENSE-Datei).
