# SAFEX

**Languages:** [English](README.md) | [Русский](README.ru.md) | [中文](README.zh-CN.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Português](README.pt-BR.md) | [العربية](README.ar.md) | [日本語](README.ja.md) | [हिन्दी](README.hi.md) | [한국어](README.ko.md)

**SAFEX（Security Audit Framework for Enhanced Protection）是一个模块化的 Python 安全工具包：先验证对目标的拥有权，然后扫描配置、源代码、系统和聊天机器人以发现漏洞，并生成以修复为导向的报告。**

> Python 3.9+ · 面向 Linux/Ubuntu · 网络安全工具。请仅在你拥有或获得明确授权测试的系统、代码和基础设施上使用 SAFEX。

## 功能特性

- **拥有权验证** — 在任何扫描之前运行两阶段授权检查，支持多种验证方式。
- **可插拔扫描器** — `config`、`code`、`system`、`vulnerability`、`network`、`web`、`bot` 以及 Linux 服务器扫描器，通过工厂/插件架构接入。
- **机器人安全** — 检测泄露的 Telegram/Discord/Slack/VK 令牌、`eval`/`exec`、命令注入、不安全的反序列化、硬编码密钥和不安全的 webhook；生成审计清单和 Podman 部署模板。
- **安全等级** — `discovery`（只读）、`safe`、`moderate` 和 `aggressive` 对每项操作进行约束。
- **自动修复** — 在备份和可回滚的前提下应用修复。
- **报告** — JSON、text、HTML、Markdown 和 CSV。
- **国际化** — 界面支持 10+ 种语言。
- **接口** — CLI、Python API、FastAPI REST API 和 TUI。
- **容器** — 完整支持 Podman（rootless）。

## 安装（Ubuntu）

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

也支持 Podman 容器镜像 — 详见下方的安装指南。

## 快速开始

```bash
python safex.py --help
python safex.py validate /path/to/target
python safex.py scan /path/to/target --safety-level safe
python safex.py scan /path/to/target --scanner code
python safex.py report --format json --output report.json
python safex.py status
python safex.py list scanners
```

## 用法

```bash
# 机器人安全
python safex.py bot-scan /path/to/bot --platform telegram
python safex.py bot-audit --platform telegram --text

# 其他接口
python src/tui/main.py                  # TUI
uvicorn src.api.app:app --port 8000     # REST API
```

全局选项：`--language en|ru|es|fr|de|zh|ja|ar|pt|it`、`--safety-level discovery|safe|moderate|aggressive`、`--verbose`。

## 文档

- [MANUAL.md](MANUAL.md) — 快速入门手册
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — 架构、数据流、扩展点
- [docs/AI_AGENT_GUIDE.md](docs/AI_AGENT_GUIDE.md) — AI 编程代理快速参考
- [docs/INSTALLATION_UBUNTU.md](docs/INSTALLATION_UBUNTU.md) — Ubuntu 详细安装
- [docs/UBUNTU_INSTALL.md](docs/UBUNTU_INSTALL.md) — 使用 Podman 在 Ubuntu 上安装
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) — 项目结构
- [CHANGELOG.md](CHANGELOG.md) — 版本历史

## 法律 / 负责任地使用

SAFEX 是一款安全测试工具。请仅对你拥有或获得明确书面授权的系统、网络、应用和源代码运行该工具。未经授权扫描第三方系统可能违法。作者对滥用不承担任何责任。

## 许可证

MIT 许可证 — 依据项目声明（许可证文件见仓库）。
