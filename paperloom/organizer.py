"""Place a file into the archive — safely.

Guarantees, in order of importance (these encode the project's "lose nothing"
promise):

  * never deletes anything the user didn't ask to move; ``copy`` mode leaves the
    original untouched;
  * never overwrites — a name clash with *different* content gets a " (2)" suffix;
  * de-duplicates by CONTENT (sha256), not by name — an identical file already in
    the archive is routed to the duplicates folder instead of piling up;
  * ``dry_run`` computes the whole plan and touches nothing.
"""
from __future__ import annotations

import hashlib
import json
import re
import shutil
from pathlib import Path

_INDEX_DIR = ".paperloom"
_MAX_SEED_BYTES = 200 * 1024 * 1024  # don't hash giant files when seeding the index


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def sanitize(name: str) -> str:
    name = re.sub(r"[\x00-\x1f/\\:*?\"<>|]", " ", name)
    name = re.sub(r"\s+", " ", name).strip(" .")
    return name[:120] or "document"


class Organizer:
    def __init__(self, settings) -> None:
        self.settings = settings
        self.archive = settings.archive
        self.index_path = self.archive / _INDEX_DIR / "seen.json"
        self.index: dict[str, str] = {}
        self._load_or_seed_index()

    def _load_or_seed_index(self) -> None:
        if self.index_path.exists():
            try:
                self.index = json.loads(self.index_path.read_text(encoding="utf-8"))
                return
            except (OSError, ValueError):
                self.index = {}
        # First run: hash what's already in the archive so we dedupe against it.
        if self.archive.exists():
            for p in self.archive.rglob("*"):
                if p.is_file() and _INDEX_DIR not in p.parts and p.stat().st_size <= _MAX_SEED_BYTES:
                    try:
                        self.index[sha256(p)] = str(p.relative_to(self.archive))
                    except OSError:
                        continue
        self._save_index(force=True)

    def _save_index(self, force: bool = False) -> None:
        try:
            self.index_path.parent.mkdir(parents=True, exist_ok=True)
            self.index_path.write_text(json.dumps(self.index, ensure_ascii=False, indent=2),
                                       encoding="utf-8")
        except OSError:
            if force:
                pass

    def _unique_target(self, folder: Path, filename: str) -> Path:
        target = folder / filename
        if not target.exists():
            return target
        stem, suffix = target.stem, target.suffix
        i = 2
        while (folder / f"{stem} ({i}){suffix}").exists():
            i += 1
        return folder / f"{stem} ({i}){suffix}"

    def place(self, path: Path, decision: dict, dry_run: bool = False) -> dict:
        """Move/copy ``path`` into the archive per ``decision``. Returns a record."""
        digest = sha256(path)
        rec = {"src": str(path), "category": decision.get("category"),
               "via": decision.get("via"), "confidence": decision.get("confidence", 0.0)}

        # Duplicate of something already filed?
        if digest in self.index:
            folder = self.archive / self.settings.duplicates_dir
            rec["action"] = "duplicate"
            rec["note"] = f"same content as {self.index[digest]}"
        else:
            category = decision.get("category")
            folder = self.archive / (category if category else self.settings.review_dir)
            rec["action"] = "filed" if category else "review"

        clean = sanitize(decision.get("filename") or path.stem) + path.suffix.lower()
        target = self._unique_target(folder, clean)
        rec["dest"] = str(target)

        if dry_run:
            return rec

        folder.mkdir(parents=True, exist_ok=True)
        if self.settings.mode == "copy":
            shutil.copy2(path, target)
        else:
            shutil.move(str(path), str(target))
        # Record the checksum only for files that actually landed in the archive
        # proper (not duplicates), so future runs dedupe against them.
        if rec["action"] != "duplicate":
            self.index[digest] = str(target.relative_to(self.archive))
            self._save_index()
        self._log(rec)
        return rec

    def _log(self, rec: dict) -> None:
        try:
            logp = self.archive / _INDEX_DIR / "log.txt"
            logp.parent.mkdir(parents=True, exist_ok=True)
            with logp.open("a", encoding="utf-8") as f:
                f.write(f"{rec['action']}\t{rec.get('category') or '-'}\t"
                        f"{rec['src']}\t->\t{rec['dest']}\t({rec.get('via')})\n")
        except OSError:
            pass
