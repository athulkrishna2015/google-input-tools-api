"""Google Input Tools -> Indic script transliteration client.

Extracted from the network traffic of https://www.manglish.app/, which itself
delegates conversion to Google's (undocumented) Input Tools endpoint:

    GET https://inputtools.google.com/request
        ?text=<latin>&itc=<code>&num=5&cp=0&cs=1&ie=utf-8&oe=utf-8

No API key, no account.
"""

from __future__ import annotations

import json
import urllib.parse
import urllib.request
from dataclasses import dataclass, field
from typing import List, Optional

ENDPOINT = "https://inputtools.google.com/request"
DEFAULT_ITC = "ml-t-i0-und"  # Malayalam transliteration
DEFAULT_NUM = 5

# Google Input Tools transliteration codes (latin -> script).
LANGUAGES = {
    "amharic": "am-t-i0-und",
    "arabic": "ar-t-i0-und",
    "assamese": "as-t-i0-und",
    "bengali": "bn-t-i0-und",
    "belarusian": "be-t-i0-und",
    "bulgarian": "bg-t-i0-und",
    "chinese": "pinyin",
    "greek": "el-t-i0-und",
    "gujarati": "gu-t-i0-und",
    "hebrew": "he-t-i0-und",
    "hindi": "hi-t-i0-und",
    "kannada": "kn-t-i0-und",
    "malayalam": "ml-t-i0-und",
    "marathi": "mr-t-i0-und",
    "nepali": "ne-t-i0-und",
    "odia": "or-t-i0-und",
    "persian": "fa-t-i0-und",
    "punjabi": "pa-t-i0-und",
    "russian": "ru-t-i0-und",
    "sanskrit": "sa-t-i0-und",
    "serbian": "sr-t-i0-und",
    "sinhala": "si-t-i0-und",
    "tamil": "ta-t-i0-und",
    "telugu": "te-t-i0-und",
    "tigrinya": "ti-t-i0-und",
    "ukrainian": "uk-t-i0-und",
    "urdu": "ur-t-i0-und",
}

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/158.0.0.0 Safari/537.36"
)


def itc_for(lang: str) -> str:
    """Resolve a language name (or raw itc code) to an itc code."""
    lang = (lang or "").strip().lower()
    if lang in LANGUAGES:
        return LANGUAGES[lang]
    if lang in ("pinyin",) or "-t-i0-und" in lang:
        return lang
    raise ValueError("unknown language: %r; choices: %s" % (lang, ", ".join(LANGUAGES)))


@dataclass
class Conversion:
    input: str
    candidates: List[str] = field(default_factory=list)
    candidate_types: List[int] = field(default_factory=list)
    raw: object = None

    @property
    def top(self) -> Optional[str]:
        return self.candidates[0] if self.candidates else None


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
