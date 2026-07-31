# SAFEX

**Languages:** [English](README.md) | [Русский](README.ru.md) | [中文](README.zh-CN.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Português](README.pt-BR.md) | [العربية](README.ar.md) | [日本語](README.ja.md) | [हिन्दी](README.hi.md) | [한국어](README.ko.md)

**SAFEX(Security Audit Framework for Enhanced Protection)는 대상의 소유권을 검증한 뒤 구성, 소스 코드, 시스템, 메시징 봇을 취약점 점검용으로 스캔하고 수정 중심의 보고서를 생성하는 모듈형 Python 보안 도구입니다.**

> Python 3.9+ · Linux/Ubuntu 중심 · 사이버 보안 도구. SAFEX는 본인이 소유하거나 테스트할 명시적 권한이 있는 시스템, 코드, 인프라에만 사용하세요.

## 주요 기능

- **소유권 검증** — 모든 스캔 전에 2단계 인가 검사가 실행되며, 여러 검증 방법을 지원합니다.
- **플러그인 가능한 스캐너** — `config`, `code`, `system`, `vulnerability`, `network`, `web`, `bot` 및 Linux 서버 스캐너를 Factory/플러그인 아키텍처로 제공합니다.
- **봇 보안** — Telegram/Discord/Slack/VK 토큰 유출, `eval`/`exec`, 명령어 삽입, 안전하지 않은 역직렬화, 하드코딩된 시크릿, 안전하지 않은 웹훅을 탐지하고, 감사 체크리스트와 Podman 배포 템플릿을 생성합니다.
- **안전 수준** — `discovery`(읽기 전용), `safe`, `moderate`, `aggressive`가 모든 작업을 통제합니다.
- **자동 수정** — 백업 및 롤백과 함께 수정을 적용합니다.
- **보고서** — JSON, text, HTML, Markdown, CSV.
- **i18n** — 10개 이상의 언어로 인터페이스 제공.
- **인터페이스** — CLI, Python API, FastAPI REST API, TUI.
- **컨테이너** — Podman(rootless) 완벽 지원.

## 설치(Ubuntu)

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

Podman 컨테이너 이미지도 지원됩니다 — 아래 설치 가이드를 참조하세요.

## 빠른 시작

```bash
python safex.py --help
python safex.py validate /path/to/target
python safex.py scan /path/to/target --safety-level safe
python safex.py scan /path/to/target --scanner code
python safex.py report --format json --output report.json
python safex.py status
python safex.py list scanners
```

## 사용법

```bash
# 봇 보안
python safex.py bot-scan /path/to/bot --platform telegram
python safex.py bot-audit --platform telegram --text

# 기타 인터페이스
python src/tui/main.py                  # TUI
uvicorn src.api.app:app --port 8000     # REST API
```

전역 옵션: `--language en|ru|es|fr|de|zh|ja|ar|pt|it`, `--safety-level discovery|safe|moderate|aggressive`, `--verbose`.

## 문서

- [MANUAL.md](MANUAL.md) — 빠른 시작 매뉴얼
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — 아키텍처, 데이터 흐름, 확장 지점
- [docs/AI_AGENT_GUIDE.md](docs/AI_AGENT_GUIDE.md) — AI 코딩 에이전트용 빠른 참조
- [docs/INSTALLATION_UBUNTU.md](docs/INSTALLATION_UBUNTU.md) — Ubuntu 상세 설치
- [docs/UBUNTU_INSTALL.md](docs/UBUNTU_INSTALL.md) — Podman을 이용한 Ubuntu 설치
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) — 프로젝트 구조
- [CHANGELOG.md](CHANGELOG.md) — 버전 기록

## 법적 고지 / 책임 있는 사용

SAFEX는 보안 테스트 도구입니다. 본인이 소유하거나 명시적인 서면 권한이 있는 시스템, 네트워크, 애플리케이션, 소스 코드에만 실행하세요. 승인 없이 제3자 시스템을 스캔하는 것은 불법일 수 있습니다. 저자는 오용에 대해 어떠한 책임도 지지 않습니다.

## 라이선스

MIT 라이선스 — 프로젝트 표기에 따름(LICENSE 파일은 저장소 참조).
