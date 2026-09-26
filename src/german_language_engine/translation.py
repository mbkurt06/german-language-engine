from __future__ import annotations

import json
from functools import lru_cache
from typing import Protocol
from urllib.request import Request, urlopen


class TranslationProvider(Protocol):
    def translate(self, text: str) -> str | None: ...


class NullTranslationProvider:
    def translate(self, text: str) -> str | None:
        return None


class LibreTranslateProvider:
    """German -> Turkish provider for a LibreTranslate-compatible HTTP API."""

    def __init__(self, base_url: str, api_key: str | None = None, timeout: float = 5.0):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    @lru_cache(maxsize=4096)
    def translate(self, text: str) -> str | None:
        text = text.strip()
        if not text:
            return None
        payload = {"q": text, "source": "de", "target": "tr", "format": "text"}
        if self.api_key:
            payload["api_key"] = self.api_key
        request = Request(
            self.base_url + "/translate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=self.timeout) as response:
                result = json.loads(response.read().decode("utf-8"))
        except Exception:
            return None
        translated = result.get("translatedText")
        return translated.strip() if isinstance(translated, str) and translated.strip() else None
