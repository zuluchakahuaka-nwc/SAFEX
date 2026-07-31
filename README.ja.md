# SAFEX

**Languages:** [English](README.md) | [Русский](README.ru.md) | [中文](README.zh-CN.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Português](README.pt-BR.md) | [العربية](README.ar.md) | [日本語](README.ja.md) | [हिन्दी](README.hi.md) | [한국어](README.ko.md)

**SAFEX（Security Audit Framework for Enhanced Protection）は、ターゲットの所有権を検証した上で、設定・ソースコード・システム・メッセージングボットの脆弱性をスキャンし、修正志向のレポートを生成する、モジュラー式の Python セキュリティツールキットです。**

> Python 3.9+ · Linux/Ubuntu 向け · サイバーセキュリティツール。SAFEX は、あなたが所有している、またはテストの明示的な許可を得ているシステム・コード・インフラに対してのみ使用してください。

## 主な機能

- **所有権の検証** — いかなるスキャンの前にも、複数の検証方法を用いた 2 段階の認可チェックが実行されます。
- **プラグイン可能なスキャナー** — `config`、`code`、`system`、`vulnerability`、`network`、`web`、`bot`、および Linux サーバースキャナーを、Factory/プラグインアーキテクチャで提供します。
- **ボットセキュリティ** — Telegram/Discord/Slack/VK のトークン漏洩、`eval`/`exec`、コマンドインジェクション、安全でないデシリアライズ、ハードコードされたシークレット、安全でない Webhook を検出し、監査チェックリストと Podman デプロイテンプレートを生成します。
- **安全レベル** — `discovery`（読み取り専用）、`safe`、`moderate`、`aggressive` がすべての操作を制御します。
- **自動修正** — バックアップとロールバック付きで修正を適用します。
- **レポート** — JSON、text、HTML、Markdown、CSV。
- **i18n** — 10 以上の言語でインターフェイスを利用可能。
- **インターフェイス** — CLI、Python API、FastAPI の REST API、TUI。
- **コンテナ** — Podman（rootless）に完全対応。

## インストール（Ubuntu）

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

Podman コンテナイメージにも対応しています — 下記のインストールガイドを参照してください。

## クイックスタート

```bash
python safex.py --help
python safex.py validate /path/to/target
python safex.py scan /path/to/target --safety-level safe
python safex.py scan /path/to/target --scanner code
python safex.py report --format json --output report.json
python safex.py status
python safex.py list scanners
```

## 使用方法

```bash
# ボットセキュリティ
python safex.py bot-scan /path/to/bot --platform telegram
python safex.py bot-audit --platform telegram --text

# その他のインターフェイス
python src/tui/main.py                  # TUI
uvicorn src.api.app:app --port 8000     # REST API
```

グローバルオプション：`--language en|ru|es|fr|de|zh|ja|ar|pt|it`、`--safety-level discovery|safe|moderate|aggressive`、`--verbose`。

## ドキュメント

- [MANUAL.md](MANUAL.md) — クイックスタートマニュアル
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — アーキテクチャ、データフロー、拡張ポイント
- [docs/AI_AGENT_GUIDE.md](docs/AI_AGENT_GUIDE.md) — AI コーディングエージェント向けクイックリファレンス
- [docs/INSTALLATION_UBUNTU.md](docs/INSTALLATION_UBUNTU.md) — Ubuntu の詳細インストール
- [docs/UBUNTU_INSTALL.md](docs/UBUNTU_INSTALL.md) — Podman を使った Ubuntu インストール
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) — プロジェクト構成
- [CHANGELOG.md](CHANGELOG.md) — バージョン履歴

## 法的事項 / 責任ある利用

SAFEX はセキュリティテストツールです。あなたが所有している、または明示的な書面による許可を得ているシステム・ネットワーク・アプリケーション・ソースコードに対してのみ実行してください。許可なく第三者のシステムをスキャンすると違法となる場合があります。著者は悪用について一切の責任を負いません。

## ライセンス

MIT ライセンス — プロジェクトの表明による（LICENSE ファイルはリポジトリを参照）。
