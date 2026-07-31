# SAFEX

**Languages:** [English](README.md) | [Русский](README.ru.md) | [中文](README.zh-CN.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Português](README.pt-BR.md) | [العربية](README.ar.md) | [日本語](README.ja.md) | [हिन्दी](README.hi.md) | [한국어](README.ko.md)

**SAFEX (Security Audit Framework for Enhanced Protection) is a modular Python security toolkit that validates ownership of a target, then scans configurations, source code, systems, and messaging bots for vulnerabilities and generates fix-oriented reports.**

> Python 3.9+ · Linux/Ubuntu focused · Cybersecurity tool. Use SAFEX only on systems, code, and infrastructure that you own or are explicitly authorized to test.

## Features

- **Ownership validation** — a two-phase authorization check runs before any scan, with multiple validation methods.
- **Pluggable scanners** — `config`, `code`, `system`, `vulnerability`, `network`, `web`, `bot`, and a Linux server scanner, wired through a Factory/plugin architecture.
- **Bot security** — detects leaked Telegram/Discord/Slack/VK tokens, `eval`/`exec`, command injection, unsafe deserialization, hardcoded secrets, and insecure webhooks; produces audit checklists and Podman deployment templates.
- **Safety levels** — `discovery` (read-only), `safe`, `moderate`, and `aggressive` gate every operation.
- **Auto-fix** — applies fixes with backups and rollback.
- **Reporting** — JSON, text, HTML, Markdown, and CSV.
- **i18n** — interface available in 10+ languages.
- **Interfaces** — CLI, Python API, FastAPI REST API, and a TUI.
- **Containers** — full Podman (rootless) support.

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

A Podman container image is also supported — see the Installation guide below.

## Quick Start

```bash
python safex.py --help
python safex.py validate /path/to/target
python safex.py scan /path/to/target --safety-level safe
python safex.py scan /path/to/target --scanner code
python safex.py report --format json --output report.json
python safex.py status
python safex.py list scanners
```

## Usage

```bash
# Bot security
python safex.py bot-scan /path/to/bot --platform telegram
python safex.py bot-audit --platform telegram --text

# Other interfaces
python src/tui/main.py                  # TUI
uvicorn src.api.app:app --port 8000     # REST API
```

Global options: `--language en|ru|es|fr|de|zh|ja|ar|pt|it`, `--safety-level discovery|safe|moderate|aggressive`, `--verbose`.

## Documentation

- [MANUAL.md](MANUAL.md) — quick-start manual
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — architecture, data flow, extension points
- [docs/AI_AGENT_GUIDE.md](docs/AI_AGENT_GUIDE.md) — quick reference for AI coding agents
- [docs/INSTALLATION_UBUNTU.md](docs/INSTALLATION_UBUNTU.md) — detailed Ubuntu installation
- [docs/UBUNTU_INSTALL.md](docs/UBUNTU_INSTALL.md) — Ubuntu installation with Podman
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) — project layout
- [CHANGELOG.md](CHANGELOG.md) — version history

## Legal / Responsible Use

SAFEX is a security testing tool. Run it only against systems, networks, applications, and source code that you own or for which you have explicit written authorization. Unauthorized scanning of third-party systems may be illegal. The authors accept no liability for misuse.

## License

MIT License — as stated by the project (see repository for the LICENSE file).
