"""Manglish -> Malayalam typing via the (undocumented) Google Input Tools endpoint.

The endpoint is the same one https://www.manglish.app/ drives in the browser:

    GET https://inputtools.google.com/request
        ?text=<manglish>&itc=ml-t-i0-und&num=5&cp=0&cs=1&ie=utf-8&oe=utf-8

``itc=ml-t-i0-und`` selects Malayalam transliteration. Other Indic languages use
their own codes, e.g. ``hi-t-i0-und`` (Hindi), ``ta-t-i0-und`` (Tamil).

Response shape::

    ["SUCCESS", [[input, [candidates...], [], {"candidate_type": [...]}]]]

This module exposes a small, dependency-free (stdlib only) client.
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from typing import List, Optional

ENDPOINT = "https://inputtools.google.com/request"
DEFAULT_ITC = "ml-t-i0-und"
DEFAULT_NUM = 5

# Google Input Tools codes for Indic transliteration (manglish-style typing).
LANGUAGES = {
    "malayalam": "ml-t-i0-und",
    "hindi": "hi-t-i0-und",
    "tamil": "ta-t-i0-und",
    "kannada": "kn-t-i0-und",
    "telugu": "te-t-i0-und",
    "bengali": "bn-t-i0-und",
    "gujarati": "gu-t-i0-und",
    "marathi": "mr-t-i0-und",
    "punjabi": "pa-t-i0-und",
    "odia": "or-t-i0-und",
}

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/158.0.0.0 Safari/537.36"
)


@dataclass
class Conversion:
    input: str
    candidates: List[str] = field(default_factory=list)
    candidate_types: List[int] = field(default_factory=list)
    raw: object = None

    @property
    def top(self) -> Optional[str]:
        return self.candidates[0] if self.candidates else None


def itc_for(lang: str) -> str:
    """Resolve a language name (or raw itc code) to an itc code."""
    lang = (lang or "").strip().lower()
    if lang in LANGUAGES:
        return LANGUAGES[lang]
    if "-t-i0-und" in lang:
        return lang
    raise ValueError(f"unknown language: {lang!r}; choices: {', '.join(LANGUAGES)}")


def convert(
    text: str,
    *,
    itc: str = DEFAULT_ITC,
    num: int = DEFAULT_NUM,
    cp: Optional[int] = None,
    cs: int = 1,
    timeout: float = 30.0,
) -> Conversion:
    if cp is None:
        cp = len(text)
    params = {
        "text": text,
        "itc": itc,
        "num": num,
        "cp": cp,
        "cs": cs,
        "ie": "utf-8",
        "oe": "utf-8",
    }
    url = ENDPOINT + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://www.manglish.app/",
            "Origin": "https://www.manglish.app",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = json.loads(resp.read().decode("utf-8"))

    conv = Conversion(input=text, raw=data)
    try:
        block = data[1][0]
        conv.input = block[0]
        conv.candidates = list(block[1] or [])
        meta = block[3] if len(block) > 3 and isinstance(block[3], dict) else {}
        conv.candidate_types = list(meta.get("candidate_type", []))
    except (IndexError, TypeError, KeyError):
        pass
    return conv


def top(text: str, **kwargs) -> Optional[str]:
    return convert(text, **kwargs).top


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else sys.stdin.read().strip()
    c = convert(text)
    print(c.top if c.top is not None else "")
