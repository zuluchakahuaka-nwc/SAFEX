# SAFEX

**Languages:** [English](README.md) | [Русский](README.ru.md) | [中文](README.zh-CN.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Português](README.pt-BR.md) | [العربية](README.ar.md) | [日本語](README.ja.md) | [हिन्दी](README.hi.md) | [한국어](README.ko.md)

**SAFEX (Security Audit Framework for Enhanced Protection) é um kit de ferramentas de segurança modular em Python que valida a propriedade de um alvo e, em seguida, analisa configurações, código-fonte, sistemas e bots de mensageria em busca de vulnerabilidades, gerando relatórios orientados à correção.**

> Python 3.9+ · focado em Linux/Ubuntu · ferramenta de cibersegurança. Use o SAFEX apenas em sistemas, código e infraestrutura que você possui ou está explicitamente autorizado a testar.

## Recursos

- **Validação de propriedade** — uma verificação de autorização em duas fases é executada antes de qualquer análise, com vários métodos de validação.
- **Scanners conectáveis** — `config`, `code`, `system`, `vulnerability`, `network`, `web`, `bot` e um scanner de servidores Linux, integrados por meio de uma arquitetura Factory/plugin.
- **Segurança de bots** — detecta vazamento de tokens do Telegram/Discord/Slack/VK, `eval`/`exec`, injeção de comandos, desserialização insegura, segredos codificados e webhooks inseguros; gera listas de auditoria e modelos de implantação Podman.
- **Níveis de segurança** — `discovery` (somente leitura), `safe`, `moderate` e `aggressive` controlam cada operação.
- **Auto-fix** — aplica correções com backups e reversão.
- **Relatórios** — JSON, text, HTML, Markdown e CSV.
- **i18n** — interface disponível em mais de 10 idiomas.
- **Interfaces** — CLI, API Python, API REST com FastAPI e TUI.
- **Contêineres** — suporte completo a Podman (rootless).

## Instalação (Ubuntu)

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

Também há suporte a uma imagem de contêiner Podman — veja o guia de instalação abaixo.

## Início rápido

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
# Segurança de bots
python safex.py bot-scan /path/to/bot --platform telegram
python safex.py bot-audit --platform telegram --text

# Outras interfaces
python src/tui/main.py                  # TUI
uvicorn src.api.app:app --port 8000     # REST API
```

Opções globais: `--language en|ru|es|fr|de|zh|ja|ar|pt|it`, `--safety-level discovery|safe|moderate|aggressive`, `--verbose`.

## Documentação

- [MANUAL.md](MANUAL.md) — manual de início rápido
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — arquitetura, fluxo de dados, pontos de extensão
- [docs/AI_AGENT_GUIDE.md](docs/AI_AGENT_GUIDE.md) — referência rápida para agentes de IA
- [docs/INSTALLATION_UBUNTU.md](docs/INSTALLATION_UBUNTU.md) — instalação detalhada no Ubuntu
- [docs/UBUNTU_INSTALL.md](docs/UBUNTU_INSTALL.md) — instalação no Ubuntu com Podman
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) — estrutura do projeto
- [CHANGELOG.md](CHANGELOG.md) — histórico de versões

## Legal / Uso responsável

O SAFEX é uma ferramenta de teste de segurança. Execute-a apenas contra sistemas, redes, aplicativos e código-fonte que você possui ou para os quais tenha autorização explícita por escrito. A análise não autorizada de sistemas de terceiros pode ser ilegal. Os autores não se responsabilizam pelo uso indevido.

## Licença

Licença MIT — conforme declarado pelo projeto (veja o repositório para o arquivo LICENSE).
