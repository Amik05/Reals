# Reals

Print your Instagram Reels feed. Put down your phone. Read instead.

Instead of doomscrolling before bed, Reals captures your feed, runs it through AI, and generates a printable PDF zine you can read offline.

---

## How it works

A Playwright browser scrolls through your Instagram Reels, screenshotting each one. A vision AI model extracts the username, caption, and writes a one-line summary of the video content. Everything gets laid out into a two-up printable PDF.

---

## Setup

Requirements: Python 3.9+, an API key for Claude or Gemini.

```bash
git clone https://github.com/yourusername/reals
cd reals
pip install playwright anthropic google-generativeai fpdf2 pillow python-dotenv PyQt5
playwright install chromium
```

Copy `.env.example` to `.env` and fill in your key:

```
# Use Claude (Anthropic)
ANTHROPIC_API_KEY=your_key_here
AI_PROVIDER=claude

# Or use Gemini (Google)
GEMINI_API_KEY=your_key_here
AI_PROVIDER=gemini
```

---

## Usage

**Desktop app**

```bash
python app.py
```

**CLI**

```bash
python main.py                  # standard run
python main.py --count 12       # capture 12 reels
python main.py --dry-run        # skip AI calls, free, good for testing layout
```

On first run a browser window opens — log into Instagram, press Enter in the terminal. Your session is saved so you won't need to log in again. `reals.pdf` will appear in the project folder when done.

---

## Cost

Roughly $0.08 per run (8 reels) with Claude Sonnet. Gemini 2.0 Flash is cheaper still. $5 in credits gets you plenty of runs.

---

## Privacy

Everything runs locally. Your Instagram session and screenshots never leave your machine. The only external calls are to the AI API you configure.

Never commit `.env` or `session.json` — both are in `.gitignore` by default.

---

## Project structure

```
reals/
├── app.py            # desktop GUI (PyQt5)
├── main.py           # CLI entrypoint
├── scraper.py        # Playwright browser automation
├── ai_processor.py   # Claude / Gemini vision
├── pdf_builder.py    # PDF layout and export
├── .env.example
└── .gitignore
```

---

## Limitations

- Reels are captured as a still frame + AI summary — you can't print a video
- Instagram's UI changes occasionally and may need selector updates
- Intended for personal use — running at scale violates Instagram's ToS

---

## Why

The average person spends 2+ hours a day scrolling. Reals doesn't stop you from consuming your feed — it just moves it off your phone and onto paper.
---

MIT License
