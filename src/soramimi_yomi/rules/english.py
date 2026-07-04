"""英単語をカナ読みに置き換えるルール。

pyopenjtalk は未知の英単語をスペル読み(NICE→エヌアイシーイー)してしまうため、
BEP英語辞書(約4.7万語、soramimic 由来)でカナに変換してから読み推定に渡す。
辞書にない語はそのまま残す(pyopenjtalkのスペル読みに任せる)。
"""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path

_DICT_PATH = Path(__file__).parent.parent / "data" / "bep-eng.json"
_ENGLISH_WORD = re.compile(r"[A-Za-z][A-Za-z']*")


@lru_cache(maxsize=1)
def _dictionary() -> dict[str, str]:
    return json.loads(_DICT_PATH.read_text(encoding="utf-8"))


def normalize(text: str) -> str:
    d = _dictionary()

    def repl(m: re.Match) -> str:
        return d.get(m.group(0).upper(), m.group(0))

    return _ENGLISH_WORD.sub(repl, text)
