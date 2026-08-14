"""Rate-limited, cached retrieval helpers for reproducible evidence updates."""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from urllib.request import Request, urlopen


def cached_get(url: str, cache_dir: str | Path = ".cache/http", delay: float = 0.5) -> bytes:
    """Return a URL response, caching by SHA-256; never synthesizes missing data."""
    cache = Path(cache_dir)
    cache.mkdir(parents=True, exist_ok=True)
    target = cache / hashlib.sha256(url.encode()).hexdigest()
    if target.exists():
        return target.read_bytes()
    time.sleep(delay)
    request = Request(url, headers={"User-Agent": "autoimmune-landscape/1.0 (research)"})
    with urlopen(request, timeout=30) as response:  # noqa: S310 - curated HTTPS URLs only
        payload = response.read()
    target.write_bytes(payload)
    (target.with_suffix(".json")).write_text(json.dumps({"url": url}), encoding="utf-8")
    return payload

