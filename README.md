<h1 align="center">📁 Onspot</h1>

<p align="center">
  <b>Drop files in a folder. An AI reads each one and files it into your structure — and never deletes anything.</b>
</p>

<p align="center">
  <img alt="Python 3.9+" src="https://img.shields.io/badge/python-3.9%2B-blue">
  <img alt="Dependencies: none" src="https://img.shields.io/badge/dependencies-none-brightgreen">
  <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-black">
</p>

<p align="center"><a href="README.ru.md">🇷🇺 Русская версия</a></p>

---

Onspot watches an **inbox** folder. For every file you drop in, it reads the
contents, decides which of **your** categories it belongs to, gives it a clean
name, and moves it into your **archive** — a tidy, topic-organized folder tree.

```
   inbox/                          archive/
   ├── scan_20250612.pdf   ──▶     ├── 01 Taxes/
   ├── some invoice.pdf            ├── 02 Bank/2025-06-12 · Statement.pdf
   └── passport photo.jpg          ├── 05 IDs & Personal/Passport.jpg
                                   ├── _Duplicates/     ← same content, kept safe
                                   └── _Review/         ← "not sure" — you decide
```

It has **no dependencies** — only the Python standard library — and a friendly
setup wizard. The AI is **optional and pluggable**: run a model on your own
computer (private, free), use a pay-as-you-go API, or skip it and sort by simple
keyword rules.

> 🧵 Onspot is the sibling of [Threadloom](https://github.com/mAia-bird/threadloom).

## The safety promise

This tool is built for documents you can't afford to lose (taxes, IDs, contracts).
So, by design:

- **It never deletes.** Files are *moved* from the inbox into the archive (or
  *copied*, if you choose). Your originals are never removed by Onspot.
- **It never overwrites.** A name clash with different content gets a ` (2)` suffix.
- **It de-duplicates by content, not by name.** An identical file (same checksum)
  is set aside in `_Duplicates/` instead of piling up.
- **When unsure, it asks — quietly.** Low-confidence files go to `_Review/`,
  never guessed into the wrong folder.
- **`--dry-run` shows the whole plan and changes nothing.** Always try it first.

## Features

- 📥 **Inbox → archive**, organized by *your* categories (defined in a simple file).
- 🧠 **Bring your own AI** — local, API, or none. See [below](#connecting-an-ai-model).
- ⚙️ **Rules layer** — keyword/filename rules sort common files instantly, for free,
  offline, before the AI is even asked.
- 🖼️ **Images & scans** — classified by a vision model, if you connect one.
- 🔁 **Watch mode** — keep it running and it sorts new files as they arrive.
- 🔔 **Optional Telegram ping** after each run.
- 🗂️ **Google Drive friendly** — see [Using Google Drive](#using-google-drive).

## Requirements

- Python **3.9 or newer**. Nothing else — no `pip install`.

## Quick start

```bash
git clone https://github.com/mAia-bird/onspot.git
cd onspot
python run.py
```

The first run launches the setup wizard. Then drop a few files into your inbox and
**always preview first**:

```bash
python run.py --dry-run   # shows what would happen, touches nothing
python run.py             # actually sorts
```

## The setup wizard

`python run.py` (first time) or `python run.py setup` walks you through:

1. **Language** — English or Russian.
2. **Folders** — your inbox and archive paths, and whether to *move* or *copy*.
3. **Categories** — start from a ready-made personal-documents template (Taxes,
   Bank, Insurance, Housing, IDs, Contracts, Medical, Invoices, Archive) or a
   minimal one. Edit them any time in `config.json`.
4. **The AI** — local / API / Anthropic / none (see next section).
5. **Notifications** — optional Telegram summary.

Everything is written to `config.json` (your categories & folders — no secrets)
and `.env` (API key, Telegram token — git-ignored).

## Connecting an AI model

Onspot works **with no AI at all** (keyword rules), but a model makes it much
smarter — it actually *reads* each document. You have three ways to connect one;
pick by your privacy needs and budget:

### 1. Local model — most private, free

A model that runs **on your own computer**, so your documents never leave the
machine. Ideal for taxes, IDs, and medical papers.

- Install [**Ollama**](https://ollama.com) (or [LM Studio](https://lmstudio.ai)).
- Pull a model, e.g. `ollama pull llama3.1` (or a vision model like `ollama pull llava`
  to read scans/photos).
- In the wizard choose **Local**; base URL `http://localhost:11434/v1`, no API key,
  model `llama3.1`.

### 2. API key — pay-as-you-go, most accurate

You get an **API key** from a provider and pay per use (usually a fraction of a
cent per document). Your file contents are sent to that provider.

- [OpenAI](https://platform.openai.com) — base `https://api.openai.com/v1`, model e.g. `gpt-4o-mini`.
- [Anthropic](https://console.anthropic.com) — choose **Anthropic** in the wizard, model e.g. `claude-haiku-4-5`.
- [OpenRouter](https://openrouter.ai) — base `https://openrouter.ai/api/v1`, one key for **many** models (some free).
- Any other OpenAI-compatible endpoint (Together, Groq, …).

### 3. "Subscription" — read this honestly

A **ChatGPT Plus** or **Claude Pro** subscription is for the chat apps and **does
not give you an API key** — it can't be used by a tool like this. For a
subscription-like feel (one flat-ish bill, many models), the closest option is
**OpenRouter** (credit-based, includes free models). Otherwise, use a **local
model** (free) or a **pay-as-you-go API key** as above.

> If the model is ever unreachable or returns something odd, Onspot falls back
> to the keyword rules and routes anything unclear to `_Review/` — it never
> crashes on one bad file.

### Reading scans and photos (vision)

Text files and "digital" PDFs are read directly. **Scanned** PDFs and image files
(`.jpg`, `.png`) have no text to extract, so they need a **multimodal** model:
choose a vision-capable model (e.g. `gpt-4o-mini`, `claude-haiku-4-5`, or local
`llava`) and answer **yes** to "is this model multimodal?" in the wizard. Without
one, images are filed by their file name or sent to `_Review/`.

## Using it

```bash
python run.py --dry-run       # safe preview — always start here
python run.py                 # sort the inbox once
python run.py --watch         # keep watching (add --interval 60 for 60s)
python run.py setup           # re-run the wizard
```

Each file prints a line: `📁 filed`, `🔎 to review`, or `♻️ duplicate`, then a
one-line summary (optionally sent to Telegram).

## Using Google Drive

Want your inbox and archive to live in Google Drive, reachable from every device?
Two ways.

### The easy, recommended way: Google Drive for Desktop

[Google Drive for Desktop](https://www.google.com/drive/download/) mounts your
Drive as a normal folder on your computer. Then Onspot needs **no Google
account access at all** — it just reads and writes local paths:

1. Install Google Drive for Desktop and sign in.
2. In the wizard (or `config.json`), point:
   - `inbox` at a folder inside the mounted Drive, e.g.
     `~/Library/CloudStorage/GoogleDrive-you@gmail.com/My Drive/Inbox` (macOS) or
     `G:\My Drive\Inbox` (Windows);
   - `archive` at another folder in the same Drive.
3. Run `python run.py` as usual. Sorted files sync to Drive automatically.

> **Note:** some systems restrict *background* processes from reading the mounted
> Drive. If a scheduled/background run can't see the folder, run Onspot as a
> normal foreground process (a terminal, or a login-time launch agent), not a
> locked-down system service.

This is the pragmatic choice, and it works with **any** cloud that offers a
desktop-sync folder (Dropbox, OneDrive, iCloud Drive) — Onspot doesn't care, it
just sees folders.

### The advanced way: the Google Drive API (not built in)

Talking to Drive directly through its API (no desktop mount) is possible but
heavier: it needs a Google Cloud project, OAuth consent, and — for anything beyond
your own account — Google's app verification. Unverified apps that request broad
Drive access get an *"app is blocked"* screen, which makes this awkward to hand to
other people. It's on the roadmap as an optional backend; for now, the
desktop-mount approach above is the supported route.

## How a file is matched

1. **Rules first.** If the file name or its text contains a keyword you listed for
   a category (`config.json` → `rules`), it's filed there immediately — free and
   instant.
2. **Then the AI** (if enabled) reads the preview (or the image) and picks a
   category + a clean name, with a confidence score.
3. **Confidence gate.** Below `min_confidence` (default 0.6), or a category the
   model made up, → `_Review/`.
4. **Duplicate check.** Same content as something already filed → `_Duplicates/`.

## Configuration reference

`config.json` (your folders & categories — safe to keep) and `.env` (secrets —
git-ignored). See [`config.example.json`](config.example.json).

| `config.json` key | What it is |
| --- | --- |
| `lang` | `en` or `ru`. |
| `inbox` / `archive` | Folder paths (`~` is expanded). |
| `mode` | `move` (default) or `copy` (leave originals in the inbox). |
| `min_confidence` | 0–1; below this the AI's guess goes to `_Review/`. |
| `duplicates_dir` / `review_dir` | Names of the special folders. |
| `categories[]` | `{ name, description, rules: { filename_any[], text_any[] } }`. |
| `notify_telegram` | `true` to send a summary DM. |

| `.env` key | What it is |
| --- | --- |
| `LLM_ENABLED` | `true` to use a model. |
| `LLM_PROVIDER` | `openai` (incl. local & OpenAI-compatible) or `anthropic`. |
| `LLM_API_BASE` | e.g. `http://localhost:11434/v1`, `https://api.openai.com/v1`. |
| `LLM_API_KEY` | API key (empty for a local server). |
| `LLM_MODEL` | e.g. `llama3.1`, `gpt-4o-mini`, `claude-haiku-4-5`. |
| `LLM_VISION` | `true` if the model can read images/scans. |
| `TELEGRAM_TOKEN` / `TELEGRAM_CHAT_ID` | For optional notifications. |

## Privacy

With a **local** model, documents never leave your computer — Onspot makes no
network calls except to `localhost`. With an **API** model, the text (or image) of
each file is sent to that provider for classification; nothing else is uploaded,
and files are never posted anywhere public.

## Troubleshooting

- **Everything lands in `_Review/`.** No rules matched and no AI is configured (or
  it couldn't be reached). Add keywords to your categories, or connect a model.
- **A scanned PDF wasn't understood.** Scans have no text layer — connect a vision
  model and enable `LLM_VISION`.
- **"Couldn't reach the model."** For a local model, make sure Ollama/LM Studio is
  running and the base URL/port match. For an API, check the key and model name.
- **I want to undo a run.** Nothing was deleted — files are in the archive (and
  duplicates in `_Duplicates/`). Move them back to the inbox and adjust your rules.

## How it works

Small and readable, all standard library:

| File | Role |
| --- | --- |
| `onspot/extract.py` | Best-effort text preview from a file (txt, pdf, …). |
| `onspot/classify.py` | Rules + LLM → category, name, confidence. |
| `onspot/llm.py` | The model client (local / API / Anthropic, incl. vision). |
| `onspot/organizer.py` | Dedup by checksum, safe move/copy, never delete. |
| `onspot/sorter.py` | The run loop over the inbox. |
| `onspot/setup_wizard.py` | The interactive first-run setup. |

## Contributing

Issues and PRs welcome — especially more file types (better PDF/OCR handling),
new taxonomy templates, and translations (`onspot/i18n.py`).

## License

[MIT](LICENSE) © 2026 Maya ([@mayamastra](https://github.com/mayamastra))
