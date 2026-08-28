"""Bilingual strings (English / Russian) for Onspot's wizard and run output."""

S = {
    # ---- wizard framing ----
    "banner": {
        "en": "📁  Onspot — first-time setup\n"
              "Drop files in a folder; an AI files them into your structure. Nothing is deleted.",
        "ru": "📁  Onspot — первичная настройка\n"
              "Кидаешь файлы в папку — ИИ раскладывает их по твоей структуре. Ничего не удаляется.",
    },
    "choose_lang": {
        "en": "Choose a language / Выберите язык:\n  [1] English\n  [2] Русский\n> ",
        "ru": "Choose a language / Выберите язык:\n  [1] English\n  [2] Русский\n> ",
    },
    "intro": {
        "en": "\nHow it works: you have an INBOX folder and an ARCHIVE folder. Onspot reads\n"
              "each file in the inbox, decides which category it belongs to, gives it a clean\n"
              "name, and moves it into the archive. Duplicates (by content, not name) go to a\n"
              "duplicates folder; anything it's unsure about goes to a review folder.\n"
              "Safety first: it NEVER deletes, and never overwrites.\n",
        "ru": "\nКак это работает: есть папка INBOX (входящие) и папка ARCHIVE (архив). Onspot\n"
              "читает каждый файл из входящих, решает, к какой категории он относится, даёт ему\n"
              "аккуратное имя и перемещает в архив. Дубликаты (по содержимому, не по имени)\n"
              "уходят в папку дубликатов; всё сомнительное — в папку «на разбор».\n"
              "Безопасность прежде всего: НИКОГДА не удаляет и не перезаписывает.\n",
    },

    # ---- folders ----
    "folders_intro": {
        "en": "\n── Folders ────────────────────────────────────────────────",
        "ru": "\n── Папки ──────────────────────────────────────────────────",
    },
    "prompt_inbox": {
        "en": "Inbox folder — where you drop files [default: ./inbox]: ",
        "ru": "Папка входящих — куда кидаешь файлы [по умолчанию: ./inbox]: ",
    },
    "prompt_archive": {
        "en": "Archive folder — where the sorted structure lives [default: ./archive]: ",
        "ru": "Папка архива — где живёт разобранная структура [по умолчанию: ./archive]: ",
    },
    "prompt_mode": {
        "en": "Move files out of the inbox, or copy them (leave originals)? [move/copy, default move]: ",
        "ru": "Перемещать файлы из входящих или копировать (оставлять оригиналы)? [move/copy, по умолчанию move]: ",
    },

    # ---- taxonomy ----
    "taxonomy_intro": {
        "en": "\n── Your categories ────────────────────────────────────────\n"
              "These are the folders files get sorted into. You can start from a ready-made\n"
              "template for personal/household documents and edit it later in config.json.",
        "ru": "\n── Твои категории ─────────────────────────────────────────\n"
              "Это папки, по которым раскладываются файлы. Можно начать с готового шаблона\n"
              "для личных/бытовых документов и потом отредактировать в config.json.",
    },
    "taxonomy_choose": {
        "en": "  [1] Personal documents template (Taxes, Bank, Insurance, Housing, IDs, …)\n"
              "  [2] Minimal (just a couple of folders — you'll edit config.json)\n"
              "Choose [default 1]: ",
        "ru": "  [1] Шаблон личных документов (Налоги, Банк, Страховки, Жильё, Документы, …)\n"
              "  [2] Минимум (пара папок — дальше правишь config.json)\n"
              "Выбор [по умолчанию 1]: ",
    },
    "taxonomy_saved": {
        "en": "✓ {n} categories saved. Edit them any time in config.json.\n",
        "ru": "✓ Сохранено категорий: {n}. Правь их в любой момент в config.json.\n",
    },

    # ---- LLM ----
    "llm_intro": {
        "en": "\n── The AI that reads your files ───────────────────────────\n"
              "You have three ways to connect a model — pick what fits your privacy and budget:\n\n"
              "  • LOCAL (recommended for private documents): a model that runs on YOUR\n"
              "    computer via Ollama or LM Studio. Free, offline, nothing leaves your machine.\n"
              "    Great for taxes, IDs, medical papers.\n\n"
              "  • API key (pay-as-you-go): OpenAI, Anthropic, OpenRouter, Together… You get an\n"
              "    API key and pay per use (usually cents). Most accurate, but your file\n"
              "    contents are sent to that provider.\n\n"
              "  • \"Subscription\" (ChatGPT Plus / Claude Pro): honestly — a chat subscription\n"
              "    is NOT an API key and can't be used for automation. For a subscription-like\n"
              "    feel, OpenRouter gives one key for many models (some free). Otherwise use\n"
              "    a local model or a pay-as-you-go API key above.\n\n"
              "  • None: skip the AI entirely and sort by keyword rules only (still useful).\n",
        "ru": "\n── Нейросеть, которая читает файлы ────────────────────────\n"
              "Подключить модель можно тремя способами — выбирай по приватности и бюджету:\n\n"
              "  • ЛОКАЛЬНАЯ (рекомендуется для личных документов): модель работает на твоём\n"
              "    компьютере через Ollama или LM Studio. Бесплатно, офлайн, ничего не уходит\n"
              "    с машины. Идеально для налогов, документов, медицины.\n\n"
              "  • По API-ключу (оплата за использование): OpenAI, Anthropic, OpenRouter,\n"
              "    Together… Получаешь API-ключ и платишь за использование (обычно копейки).\n"
              "    Точнее всего, но содержимое файлов уходит этому провайдеру.\n\n"
              "  • «Подписка» (ChatGPT Plus / Claude Pro): честно — подписка на чат это НЕ\n"
              "    API-ключ, для автоматизации не годится. Ближе всего к «по подписке» —\n"
              "    OpenRouter: один ключ на много моделей (есть бесплатные). Иначе бери\n"
              "    локальную модель или API-ключ выше.\n\n"
              "  • Никакой: пропустить ИИ и сортировать только по ключевым словам (тоже полезно).\n",
    },
    "llm_choose": {
        "en": "Connect: [1] Local (Ollama/LM Studio)  [2] API key (OpenAI-compatible)  "
              "[3] Anthropic  [4] None (rules only)\nChoose [default 1]: ",
        "ru": "Подключить: [1] Локальная (Ollama/LM Studio)  [2] API-ключ (OpenAI-совместимый)  "
              "[3] Anthropic  [4] Никакой (только правила)\nВыбор [по умолчанию 1]: ",
    },
    "llm_base": {
        "en": "API base URL [{default}]: ",
        "ru": "Base URL API [{default}]: ",
    },
    "llm_key": {
        "en": "API key (empty for a local server): ",
        "ru": "API-ключ (пусто для локального сервера): ",
    },
    "llm_model": {
        "en": "Model name (e.g. {example}): ",
        "ru": "Название модели (например {example}): ",
    },
    "llm_vision": {
        "en": "Is this model multimodal (can read images/scans)? [y/N]: ",
        "ru": "Модель мультимодальная (умеет читать картинки/сканы)? [y/N]: ",
    },
    "llm_testing": {
        "en": "Testing the connection…",
        "ru": "Проверяю подключение…",
    },
    "llm_ok": {
        "en": "✓ Model responded. AI sorting is on.\n",
        "ru": "✓ Модель ответила. Умная сортировка включена.\n",
    },
    "llm_fail": {
        "en": "✗ Couldn't reach the model: {err}\n  Saved anyway — fix it in .env later, or it "
              "falls back to keyword rules.\n",
        "ru": "✗ Не достучался до модели: {err}\n  Всё равно сохранил — поправишь в .env позже, "
              "иначе сработают правила по ключевым словам.\n",
    },
    "llm_none": {
        "en": "○ No AI — sorting by keyword rules only. You can enable a model later in .env.\n",
        "ru": "○ Без ИИ — сортировка по правилам. Модель можно включить позже в .env.\n",
    },

    # ---- notify ----
    "notify_intro": {
        "en": "\n── Notifications (optional) ───────────────────────────────\n"
              "Onspot can send you one short Telegram message after each run. Skip to just "
              "print to the console.",
        "ru": "\n── Уведомления (по желанию) ───────────────────────────────\n"
              "Onspot может слать тебе одно короткое сообщение в Telegram после каждого "
              "прогона. Пропусти, если хватает вывода в консоль.",
    },
    "notify_enable": {
        "en": "Set up Telegram notifications? [y/N]: ",
        "ru": "Настроить уведомления в Telegram? [y/N]: ",
    },
    "notify_token": {
        "en": "Bot token from @BotFather (/newbot): ",
        "ru": "Токен бота от @BotFather (/newbot): ",
    },
    "notify_capture": {
        "en": "Now message your bot @{username} anything, so I can grab your chat ID…",
        "ru": "Теперь напиши своему боту @{username} что угодно, чтобы я поймал твой chat ID…",
    },
    "notify_ok": {
        "en": "✓ Notifications on — {name} (chat {chat}).\n",
        "ru": "✓ Уведомления включены — {name} (chat {chat}).\n",
    },
    "notify_skip": {
        "en": "○ No notifications. Results print to the console.\n",
        "ru": "○ Без уведомлений. Результаты выводятся в консоль.\n",
    },

    # ---- done ----
    "done": {
        "en": "\n✓ All set.\n  Settings:  {config}\n  Secrets:   {env}  (git-ignored)\n\n"
              "Drop some files into:\n    {inbox}\n"
              "Then run a safe preview first:\n    python run.py --dry-run\n"
              "and when it looks right:\n    python run.py\n",
        "ru": "\n✓ Готово.\n  Настройки: {config}\n  Секреты:   {env}  (в .gitignore)\n\n"
              "Закинь файлы в:\n    {inbox}\n"
              "Сначала безопасный предпросмотр:\n    python run.py --dry-run\n"
              "а когда всё верно:\n    python run.py\n",
    },

    # ---- run output ----
    "run_header": {
        "en": "📁 Onspot · inbox: {inbox} → archive: {archive} · engine: {engine}",
        "ru": "📁 Onspot · входящие: {inbox} → архив: {archive} · движок: {engine}",
    },
    "inbox_empty": {
        "en": "  Inbox is empty — nothing to sort.",
        "ru": "  Входящие пусты — сортировать нечего.",
    },
    "watching": {
        "en": "  Watching the inbox every {interval}s. Press Ctrl+C to stop.",
        "ru": "  Слежу за входящими каждые {interval}с. Ctrl+C — остановить.",
    },
    "summary": {
        "en": "  ── {total} file(s){dry}: 📁 {filed} filed · 🔎 {review} to review · ♻️ {dups} duplicate(s)",
        "ru": "  ── файлов: {total}{dry}: 📁 {filed} разложено · 🔎 {review} на разбор · ♻️ {dups} дублей",
    },
}


def t(key: str, lang: str = "en", **kw) -> str:
    entry = S.get(key, {})
    text = entry.get(lang) or entry.get("en") or key
    if kw:
        try:
            text = text.format(**kw)
        except (KeyError, IndexError, ValueError):
            pass
    return text
