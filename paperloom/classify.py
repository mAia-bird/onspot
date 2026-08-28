"""Decide which category a file belongs to, and a clean name for it.

Two layers, cheapest first:

  1. Rules — deterministic keyword/filename matches from ``config.json``. Free,
     offline, instant. This layer alone (no LLM at all) already sorts a lot.
  2. LLM — if enabled, an AI model reads the preview (or the image, with a vision
     model) and picks a category + suggests a filename.

A result below ``min_confidence``, or a category the model invented, is treated
as "unsure" so the file goes to the review folder instead of the wrong place.
"""
from __future__ import annotations

from pathlib import Path


def _rule_match(settings, path: Path, preview: str) -> dict | None:
    name = path.name.lower()
    text = preview.lower()
    for cat in settings.categories:
        rules = cat.get("rules") or {}
        for kw in rules.get("filename_any", []):
            if kw.lower() in name:
                return {"category": cat["name"], "filename": path.stem,
                        "confidence": 1.0, "via": "rule"}
        for kw in rules.get("text_any", []):
            if kw.lower() in text:
                return {"category": cat["name"], "filename": path.stem,
                        "confidence": 1.0, "via": "rule"}
    return None


def classify(settings, path: Path, preview: str) -> dict:
    """Return {category, filename, confidence, via}. ``category`` is None when
    the file should go to the review folder."""
    hit = _rule_match(settings, path, preview)
    if hit:
        return hit

    if settings.llm_enabled and settings.llm_model:
        try:
            from .llm import llm_classify
            result = llm_classify(settings, path, preview)
        except Exception as e:  # noqa: BLE001 - never crash the run over one file
            return {"category": None, "filename": path.stem, "confidence": 0.0,
                    "via": f"llm-error: {e}"}
        category = result.get("category")
        if category not in settings.category_names():
            category = None  # invented / "unknown" -> review
        confidence = float(result.get("confidence", 0.0) or 0.0)
        if category is None or confidence < settings.min_confidence:
            return {"category": None, "filename": result.get("filename") or path.stem,
                    "confidence": confidence, "via": "llm-unsure"}
        return {"category": category, "filename": result.get("filename") or path.stem,
                "confidence": confidence, "via": "llm"}

    # No rule matched and no LLM configured.
    return {"category": None, "filename": path.stem, "confidence": 0.0, "via": "no-match"}
