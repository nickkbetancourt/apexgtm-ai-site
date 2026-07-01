"""Lightweight website fetch used to ground the LLM's company research."""

import re
import urllib.error
import urllib.request
from typing import Optional


def fetch_website_text(url: str, timeout: float = 10.0, max_chars: int = 4000) -> Optional[str]:
    """Fetch a company's homepage and return plain text, or None on any failure.

    Best-effort only: this is context for the LLM prompt, not a hard
    dependency, so any network/parsing error just degrades to no context.
    """
    if not url or not url.strip():
        return None

    normalized = url.strip()
    if not normalized.startswith(("http://", "https://")):
        normalized = f"https://{normalized}"

    try:
        request = urllib.request.Request(
            normalized, headers={"User-Agent": "ApexGTM-Brain/1.0"}
        )
        with urllib.request.urlopen(request, timeout=timeout) as response:
            html = response.read().decode("utf-8", errors="ignore")
    except (urllib.error.URLError, TimeoutError, ValueError, OSError):
        return None

    text = _strip_html(html)
    return text[:max_chars] if text else None


def _strip_html(html: str) -> str:
    html = re.sub(r"(?is)<(script|style).*?>.*?</\1>", " ", html)
    text = re.sub(r"(?s)<[^>]+>", " ", html)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
