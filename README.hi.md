# SAFEX

**Languages:** [English](README.md) | [Русский](README.ru.md) | [中文](README.zh-CN.md) | [Español](README.es.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Português](README.pt-BR.md) | [العربية](README.ar.md) | [日本語](README.ja.md) | [हिन्दी](README.hi.md) | [한국어](README.ko.md)

**SAFEX (Security Audit Framework for Enhanced Protection) एक मॉड्यूलर Python सुरक्षा टूलकिट है जो किसी लक्ष्य की स्वामित्व सत्यापित करता है, फिर कॉन्फ़िगरेशन, सोर्स कोड, सिस्टम और मैसेजिंग बॉट को भेद्यताओं के लिए स्कैन करता है और सुधार-केंद्रित रिपोर्ट तैयार करता है।**

> Python 3.9+ · Linux/Ubuntu केंद्रित · साइबर सुरक्षा उपकरण। SAFEX का उपयोक केवल उन सिस्टम, कोड और इंफ्रास्ट्रक्चर पर करें जिनके आप स्वामी हैं या जिनके परीक्षण की स्पष्ट अनुमति आपके पास है।

## विशेषताएँ

- **स्वामित्व सत्यापन** — किसी भी स्कैन से पहले दो-चरण वाला प्राधिकरण जाँच चलती है, जिसमें कई सत्यापन विधियाँ होती हैं।
- **प्लग-इन योग्य स्कैनर** — `config`, `code`, `system`, `vulnerability`, `network`, `web`, `bot` और एक Linux सर्वर स्कैनर, Factory/प्लग-इन आर्किटेक्चर के माध्यम से जुड़े हुए।
- **बॉट सुरक्षा** — लीक हुए Telegram/Discord/Slack/VK टोकन, `eval`/`exec`, कमांड इंजेक्शन, असुरक्षित डिसिरियलाइज़ेशन, हार्डकोडेड रहस्य और असुरक्षित वेबहुक का पता लगाता है; ऑडिट चेकलिस्ट और Podman परिनियोजन टेम्पलेट बनाता है।
- **सुरक्षा स्तर** — `discovery` (केवल पढ़ने योग्य), `safe`, `moderate` और `aggressive` हर ऑपरेशन को नियंत्रित करते हैं।
- **ऑटो-फिक्स** — बैकअप और रॉलबैक के साथ सुधार लागू करता है।
- **रिपोर्टिंग** — JSON, text, HTML, Markdown और CSV।
- **i18n** — 10+ भाषाओं में इंटरफ़ेस उपलब्ध।
- **इंटरफ़ेस** — CLI, Python API, FastAPI REST API और TUI।
- **कंटेनर** — Podman (rootless) का पूर्ण समर्थन।

## स्थापना (Ubuntu)

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

Podman कंटेनर इमेज का भी समर्थन है — नीचे दिए गए स्थापना गाइड देखें।

## त्वरित आरंभ

```bash
python safex.py --help
python safex.py validate /path/to/target
python safex.py scan /path/to/target --safety-level safe
python safex.py scan /path/to/target --scanner code
python safex.py report --format json --output report.json
python safex.py status
python safex.py list scanners
```

## उपयोग

```bash
# बॉट सुरक्षा
python safex.py bot-scan /path/to/bot --platform telegram
python safex.py bot-audit --platform telegram --text

# अन्य इंटरफ़ेस
python src/tui/main.py                  # TUI
uvicorn src.api.app:app --port 8000     # REST API
```

वैश्विक विकल्प: `--language en|ru|es|fr|de|zh|ja|ar|pt|it`, `--safety-level discovery|safe|moderate|aggressive`, `--verbose`।

## दस्तावेज़ीकरण

- [MANUAL.md](MANUAL.md) — त्वरित-आरंभ मैन्युअल
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — आर्किटेक्चर, डेटा प्रवाह, विस्तार बिंदु
- [docs/AI_AGENT_GUIDE.md](docs/AI_AGENT_GUIDE.md) — AI कोडिंग एजेंटों के लिए त्वरित संदर्भ
- [docs/INSTALLATION_UBUNTU.md](docs/INSTALLATION_UBUNTU.md) — Ubuntu पर विस्तृत स्थापना
- [docs/UBUNTU_INSTALL.md](docs/UBUNTU_INSTALL.md) — Podman के साथ Ubuntu स्थापना
- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) — परियोजना संरचना
- [CHANGELOG.md](CHANGELOG.md) — संस्करण इतिहास

## कानूनी / ज़िम्मेदार उपयोग

SAFEX एक सुरक्षा परीक्षण उपकरण है। इसे केवल उन सिस्टम, नेटवर्क, अनुप्रयोगों और सोर्स कोड पर चलाएँ जिनके आप स्वामी हैं या जिनके लिए आपके पास स्पष्ट लिखित प्राधिकरण है। बिना अनुमति के तृतीय-पक्ष सिस्टम को स्कैन करना गैरकानूनी हो सकता है। लेखक दुरुपयोग के लिए कोई दायित्व स्वीकार नहीं करते।

## लाइसेंस

MIT लाइसेंस — परियोजना के अनुसार (LICENSE फ़ाइल के लिए रिपॉज़िटरी देखें)।
