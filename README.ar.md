# SAFEX

**Languages:** [English](README.md) | [Русский](README.ru.md) | [中文](README.zh-CN.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Português](README.pt-BR.md) | [العربية](README.ar.md) | [日本語](README.ja.md) | [हिन्दी](README.hi.md) | [한국어](README.ko.md)

**SAFEX (Security Audit Framework for Enhanced Protection) هي مجموعة أدوات أمنية مُجزّأة بلغة بايثون تتحقق من ملكية الهدف، ثم تفحص الإعدادات والشيفرة المصدرية والأنظمة وبوتات المراسلة بحثًا عن الثغرات وتُنشئ تقارير تركز على الإصلاح.**

> بايثون 3.9+ · مُركّزة على لينكس/أوبونتو · أداة أمن سيبراني. استخدم SAFEX فقط على الأنظمة والشيفرة والبنية التحتية التي تملكها أو المخوّل لك صراحةً باختبارها.

## الميزات

- **التحقق من الملكية** — يتم تشغيل فحص تخويل على مرحلتين قبل أي مسح، مع طرق تحقق متعددة.
- **فاحصات قابلة للإدراج** — `config` و`code` و`system` و`vulnerability` و`network` و`web` و`bot` بالإضافة إلى فاحص خوادم لينكس، مُدمجة عبر بنية Factory/إضافات.
- **أمان البوتات** — يكشف عن تسريب رموز Telegram/Discord/Slack/VK، و`eval`/`exec`، وحقن الأوامر، وإزالة التسلسل غير الآمن، والأسرار المُضمّنة، وخطافات الويب غير الآمنة؛ ويُنشئ قوائم تدقيق وقوالب نشر Podman.
- **مستويات الأمان** — `discovery` (للقراءة فقط) و`safe` و`moderate` و`aggressive` تتحكم في كل عملية.
- **الإصلاح التلقائي** — يطبّق الإصلاحات مع نسخ احتياطي وإمكانية التراجع.
- **التقارير** — JSON وtext وHTML وMarkdown وCSV.
- **تعدد اللغات (i18n)** — الواجهة متاحة بأكثر من 10 لغات.
- **الواجهات** — CLI وواجهة برمجية بلغة بايثون وREST API مبنية على FastAPI وواجهة TUI.
- **الحاويات** — دعم كامل لـ Podman (rootless).

## التثبيت (أوبونتو)

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

يُدعم أيضًا صورة حاوية Podman — راجع دليل التثبيت أدناه.

## البدء السريع

```bash
python safex.py --help
python safex.py validate /path/to/target
python safex.py scan /path/to/target --safety-level safe
python safex.py scan /path/to/target --scanner code
python safex.py report --format json --output report.json
python safex.py status
python safex.py list scanners
```

## الاستخدام

```bash
# أمان البوتات
python safex.py bot-scan /path/to/bot --platform telegram
python safex.py bot-audit --platform telegram --text

# واجهات أخرى
python src/tui/main.py                  # TUI
uvicorn src.api.app:app --port 8000     # REST API
```

الخيارات العامة: `--language en|ru|es|fr|de|zh|ja|ar|pt|it`، `--safety-level discovery|safe|moderate|aggressive`، `--verbose`.

## التوثيق

- [MANUAL.md](MANUAL.md) — دليل البدء السريع
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — البنية وتدفق البيانات ونقاط التوسعة
- [docs/AI_AGENT_GUIDE.md](docs/AI_AGENT_GUIDE.md) — مرجع سريع لوكلاء الذكاء الاصطناعي
- [docs/INSTALLATION_UBUNTU.md](docs/INSTALLATION_UBUNTU.md) — تثبيت مفصّل على أوبونتو
- [docs/UBUNTU_INSTALL.md](docs/UBUNTU_INSTALL.md) — التثبيت على أوبونتو باستخدام Podman
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) — بنية المشروع
- [CHANGELOG.md](CHANGELOG.md) — سجل الإصدارات

## قانوني / الاستخدام المسؤول

SAFEX أداة لاختبار الأمان. شغّلها فقط ضد الأنظمة والشبكات والتطبيقات والشيفرة المصدرية التي تملكها أو المخوّل لك صراحةً كتابيًا باختبارها. قد يكون مسح أنظمة الجهات الخارجية دون إذن أمرًا غير قانوني. لا يتحمل المؤلفون أي مسؤولية عن سوء الاستخدام.

## الترخيص

ترخيص MIT — كما هو موضح في المشروع (راجع المستودع لملف LICENSE).
