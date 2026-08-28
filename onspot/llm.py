"""Talk to a neural network — local, pay-as-you-go API, or Anthropic.

Standard library only. Two dialects:

  * OpenAI-compatible ``/chat/completions`` — covers OpenAI, OpenRouter,
    Together, and any LOCAL server (Ollama, LM Studio) that speaks the same API;
  * Anthropic ``/v1/messages``.

Vision (classifying an image/scan) works when the configured model is
multimodal and ``LLM_VISION=true``.

Any failure raises; the classifier catches it and routes the file to review, so
one bad call never stops the run.
"""
from __future__ import annotations

import base64
import json
import re
import urllib.error
import urllib.request
from pathlib import Path

from .extract import is_image

_SYSTEM = (
    "You are a meticulous document filer. Read the document and file it into "
    "exactly ONE of the given categories. If nothing fits, use the category "
    "\"unknown\". Also propose a short, human-readable file name (no extension, "
    "no slashes), in the document's own language. Reply with ONLY a JSON object: "
    '{"category": "<category name or unknown>", "filename": "<name>", '
    '"confidence": <0.0-1.0>}.'
)

_MEDIA = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png",
          ".gif": "image/gif", ".webp": "image/webp", ".bmp": "image/bmp"}


def _post(url: str, headers: dict, body: dict, timeout: int = 90) -> dict:
    data = json.dumps(body).encode()
    req = urllib.request.Request(url, data=data, headers={**headers, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"LLM HTTP {e.code}: {e.read().decode('utf-8', 'ignore')[:200]}")
    except urllib.error.URLError as e:
        raise RuntimeError(f"LLM network error: {e.reason}")


def _anthropic_url(base: str) -> str:
    base = base.rstrip("/")
    if base.endswith("/messages"):
        return base
    if base.endswith("/v1"):
        return f"{base}/messages"
    return f"{base}/v1/messages"


def _prompt(settings, path: Path, preview: str) -> str:
    cats = "\n".join(f"- {c['name']}: {c.get('description', '')}" for c in settings.categories)
    body = preview.strip() or "(no extractable text — rely on the file name and image)"
    return f"Categories:\n{cats}\n\nFile name: {path.name}\nDocument preview:\n{body}"


def _image_data_uri(path: Path) -> tuple[str, str]:
    media = _MEDIA.get(path.suffix.lower(), "image/jpeg")
    b64 = base64.b64encode(path.read_bytes()).decode("ascii")
    return media, b64


def _extract_json(content: str) -> dict:
    fence = re.search(r"```(?:json)?\s*(.+?)```", content, re.S)
    if fence:
        content = fence.group(1)
    start, end = content.find("{"), content.rfind("}")
    if start == -1 or end == -1:
        raise RuntimeError("model did not return JSON")
    return json.loads(content[start:end + 1])


def llm_classify(settings, path: Path, preview: str) -> dict:
    prompt = _prompt(settings, path, preview)
    use_vision = settings.llm_vision and is_image(path)
    base = settings.llm_base.rstrip("/")

    if settings.llm_provider == "anthropic":
        headers = {"x-api-key": settings.llm_key, "anthropic-version": "2023-06-01"}
        user_content: list | str
        if use_vision:
            media, b64 = _image_data_uri(path)
            user_content = [
                {"type": "text", "text": prompt},
                {"type": "image", "source": {"type": "base64", "media_type": media, "data": b64}},
            ]
        else:
            user_content = prompt
        body = {"model": settings.llm_model, "max_tokens": 512, "system": _SYSTEM,
                "messages": [{"role": "user", "content": user_content}]}
        res = _post(_anthropic_url(base), headers, body)
        content = "".join(b.get("text", "") for b in res.get("content", []) if b.get("type") == "text")
    else:  # openai-compatible (incl. local Ollama / LM Studio)
        headers = {"Authorization": f"Bearer {settings.llm_key}"} if settings.llm_key else {}
        if use_vision:
            media, b64 = _image_data_uri(path)
            user_content = [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:{media};base64,{b64}"}},
            ]
        else:
            user_content = prompt
        body = {"model": settings.llm_model, "temperature": 0.1,
                "messages": [{"role": "system", "content": _SYSTEM},
                             {"role": "user", "content": user_content}]}
        res = _post(f"{base}/chat/completions", headers, body)
        content = res["choices"][0]["message"]["content"]

    result = _extract_json(content)
    # Sanitize the suggested filename (defense in depth against odd model output).
    fn = str(result.get("filename", "")).strip().replace("/", "-").replace("\\", "-")
    result["filename"] = fn[:120] or path.stem
    return result


def quick_test(settings) -> str:
    """A tiny call to confirm the endpoint/model/key work. Returns 'ok' or raises."""
    base = settings.llm_base.rstrip("/")
    if settings.llm_provider == "anthropic":
        headers = {"x-api-key": settings.llm_key, "anthropic-version": "2023-06-01"}
        body = {"model": settings.llm_model, "max_tokens": 5,
                "messages": [{"role": "user", "content": "Reply with: ok"}]}
        _post(_anthropic_url(base), headers, body, timeout=30)
    else:
        headers = {"Authorization": f"Bearer {settings.llm_key}"} if settings.llm_key else {}
        body = {"model": settings.llm_model, "max_tokens": 5,
                "messages": [{"role": "user", "content": "Reply with: ok"}]}
        _post(f"{base}/chat/completions", headers, body, timeout=30)
    return "ok"
