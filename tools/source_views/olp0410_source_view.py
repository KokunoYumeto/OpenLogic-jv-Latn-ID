"""Bounded OLP-0410 comparison view for the conditional abbreviation typo."""
from __future__ import annotations


def repaired_olp0410_source(text: str) -> str:
    old = r"\iftag{prvOr}{$\lnot !A \lor !B)$}"
    new = r"\iftag{prvOr}{$\lnot !A \lor !B$}"
    assert text.count(old) == 1, (old, text.count(old))
    return text.replace(old, new)
