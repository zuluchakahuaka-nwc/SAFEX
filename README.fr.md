# SAFEX

**Languages:** [English](README.md) | [Русский](README.ru.md) | [中文](README.zh-CN.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Português](README.pt-BR.md) | [العربية](README.ar.md) | [日本語](README.ja.md) | [हिन्दी](README.hi.md) | [한국어](README.ko.md)

**SAFEX (Security Audit Framework for Enhanced Protection) est une boîte à outils de sécurité modulaire en Python qui valide la propriété d'une cible, puis analyse les configurations, le code source, les systèmes et les bots de messagerie à la recherche de vulnérabilités et génère des rapports orientés correction.**

> Python 3.9+ · orienté Linux/Ubuntu · outil de cybersécurité. N'utilisez SAFEX que sur des systèmes, du code et des infrastructures que vous possédez ou que vous êtes explicitement autorisé à tester.

## Fonctionnalités

- **Validation de propriété** — une vérification d'autorisation en deux phases s'exécute avant tout scan, avec plusieurs méthodes de validation.
- **Scanners plug-and-play** — `config`, `code`, `system`, `vulnerability`, `network`, `web`, `bot` et un scanner de serveurs Linux, intégrés via une architecture Factory/plugin.
- **Sécurité des bots** — détecte les fuites de jetons Telegram/Discord/Slack/VK, `eval`/`exec`, l'injection de commandes, la désérialisation non sécurisée, les secrets codés en dur et les webhooks non sécurisés ; produit des listes d'audit et des modèles de déploiement Podman.
- **Niveaux de sécurité** — `discovery` (lecture seule), `safe`, `moderate` et `aggressive` contrôlent chaque opération.
- **Auto-fix** — applique des corrections avec sauvegardes et restauration.
- **Rapports** — JSON, text, HTML, Markdown et CSV.
- **i18n** — interface disponible dans plus de 10 langues.
- **Interfaces** — CLI, API Python, API REST FastAPI et TUI.
- **Conteneurs** — prise en charge complète de Podman (rootless).

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

Une image conteneur Podman est également prise en charge — voir le guide d'installation ci-dessous.

## Démarrage rapide

```bash
python safex.py --help
python safex.py validate /path/to/target
python safex.py scan /path/to/target --safety-level safe
python safex.py scan /path/to/target --scanner code
python safex.py report --format json --output report.json
python safex.py status
python safex.py list scanners
```

## Utilisation

```bash
# Sécurité des bots
python safex.py bot-scan /path/to/bot --platform telegram
python safex.py bot-audit --platform telegram --text

# Autres interfaces
python src/tui/main.py                  # TUI
uvicorn src.api.app:app --port 8000     # REST API
```

Options globales : `--language en|ru|es|fr|de|zh|ja|ar|pt|it`, `--safety-level discovery|safe|moderate|aggressive`, `--verbose`.

## Documentation

- [MANUAL.md](MANUAL.md) — manuel de démarrage rapide
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — architecture, flux de données, points d'extension
- [docs/AI_AGENT_GUIDE.md](docs/AI_AGENT_GUIDE.md) — référence rapide pour les agents IA
- [docs/INSTALLATION_UBUNTU.md](docs/INSTALLATION_UBUNTU.md) — installation détaillée sur Ubuntu
- [docs/UBUNTU_INSTALL.md](docs/UBUNTU_INSTALL.md) — installation sur Ubuntu avec Podman
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) — structure du projet
- [CHANGELOG.md](CHANGELOG.md) — historique des versions

## Légal / Usage responsable

SAFEX est un outil de test de sécurité. Ne l'exécutez que sur des systèmes, réseaux, applications et code source que vous possédez ou pour lesquels vous disposez d'une autorisation écrite explicite. L'analyse non autorisée de systèmes tiers peut être illégale. Les auteurs déclinent toute responsabilité en cas d'usage abusif.

## Licence

Licence MIT — telle qu'indiquée par le projet (voir le dépôt pour le fichier LICENSE).
