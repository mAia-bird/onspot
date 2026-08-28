---
name: onspot
description: >-
  Sort documents from an inbox folder into a structured archive using your own
  judgment as the classifier. Use when the user wants to file, sort, tidy, or
  organize incoming documents/scans/PDFs/images with Onspot — you read each file,
  decide which of the user's categories it belongs to, give it a clean name, and
  file it safely (dedup by checksum, never delete, never overwrite). This is the
  "the AI agent is the neural net" mode of the Onspot project.
---

# Onspot — sort documents with your own judgment

Onspot files documents from an **inbox** folder into a topic-organized **archive**.
It runs two ways: as a standalone program that calls an external model, and — these
instructions — with **you, the AI agent, as the classifier**. You read each
document and decide where it goes; a small Python helper does the safe move (dedup,
no overwrite, never delete). No API key or extra model is needed here — the
intelligence is you.

> **Works with any AI agent.** These instructions are model-neutral. Any assistant
> that can read files and run shell commands can follow them — Claude Code, or any
> other capable coding/agent tool. Nothing here is specific to one provider. (The
> Onspot *program* covers the other neural nets — local via Ollama/LM Studio,
> pay-as-you-go APIs, or Anthropic — so between the program and this skill, every
> kind of model is supported.)

## Setup check

1. Find the Onspot project directory (it contains `run.py` and a `config.json`).
   If you don't know where it is, ask the user for the path.
2. Read `config.json`. It gives you:
   - `categories`: a list of `{ name, description }` — **these are the folders you
     may file into**, and each `description` tells you what belongs there;
   - `inbox`, `archive`, `mode` (`move` or `copy`).
   If `config.json` is missing, tell the user to run `python3 run.py setup` first.

## The loop

3. List the files waiting in the inbox:
   ```bash
   python3 run.py list-inbox
   ```
4. For **each** file, in order:
   1. **Read the actual file** to understand what it is — read PDFs, scans, images,
      and text directly. Don't classify by filename alone.
   2. **Pick the single best category** whose `description` fits the document. Match
      on meaning, not keywords.
   3. **Compose a clean, human-readable filename** (no extension, no slashes), in
      the document's own language. A dated style works well, e.g.
      `2025-06-12 · Bank statement — Maya`.
   4. **File it** with the helper (it does the safe move + dedup):
      ```bash
      python3 run.py place "<full path from list-inbox>" --category "<exact category name>" --name "<clean name>"
      ```
   5. **If nothing fits well**, do NOT force it. Send it to review by omitting
      `--category`, and remember what kind of document it was:
      ```bash
      python3 run.py place "<path>" --name "<clean name>"
      ```

## Safety rules (non-negotiable)

- **Never delete anything.** The helper only moves or copies.
- **Never overwrite.** The helper adds a ` (2)` suffix on name clashes automatically.
- **When unsure, send to review** (omit `--category`) rather than guessing wrong.
- **Duplicates are handled for you** — identical content (by checksum) is routed to
  the duplicates folder.
- To **preview without touching anything**, add `--dry-run` to any `place` call and
  show the user the plan first. Prefer this on the first run.

## Propose new categories (the useful part)

If several documents landed in review because no category fit, **propose new
categories** — this is where your judgment adds the most:

1. Group the review items by what they actually are (e.g. several car-related docs).
2. Suggest a new category for each group: a `name` (matching the user's existing
   naming style, e.g. numbered like `10 Vehicle`) and a one-line `description`.
3. **Ask the user** whether to add them. Only with their agreement, append each new
   category to the `categories` array in `config.json`:
   `{ "name": "...", "description": "...", "rules": {} }`.
4. After adding, you may re-run the loop so the review items get filed into the new
   folders.

Never invent folders silently — suggest, confirm, then add.

## Finishing

Give the user a short summary: how many were filed, to which categories, how many
went to review or duplicates, and any categories you proposed.
