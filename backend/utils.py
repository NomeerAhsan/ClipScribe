import hashlib
import json
import re
from pathlib import Path

from bs4 import BeautifulSoup


def normalize_text(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text(" ", strip=True)
    return re.sub(r"\s+", " ", text).strip().lower()


def duplicate_key(page_url: str, html: str) -> str:
    payload = f"{page_url}|{normalize_text(html)}"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def load_state(path: Path) -> dict:
    if not path.exists():
        return {"duplicate_keys": [], "article_counts": {}}
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def save_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(state, handle, indent=2)
